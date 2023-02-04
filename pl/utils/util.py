import logging

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from datasets import load_metric
from tqdm.auto import tqdm
import sklearn
from sklearn.metrics import accuracy_score
import pandas as pd
import whisper
import pickle

logger = logging.getLogger(__name__)

def preprocessing_dataset(dataset):
    """처음 불러온 csv 파일을 원하는 형태의 DataFrame으로 변경 시켜줍니다."""
    emo = ['neu', 'hap', 'sad', 'ang', 'fea']
    emo_selected = dataset.loc[dataset.emotion.isin(emo)]
    with open('/opt/ml/final/pl/utils/audio_redataset.pickle', 'rb') as fw:
        dic = pickle.load(fw)
    audio_list = []
    for path in emo_selected['path']:
        audio_list.append(dic[path])
    out_dataset = pd.DataFrame(
        {
            "audio" : audio_list,
            "label": emo_selected['emotion'],
        }
    )
    return out_dataset

def klue_re_micro_f1(preds, labels):
    """KLUE-RE micro f1 (except no_relation)"""
    label_list = [
        'neu', 'sad', 'ang', 'hap', 'fea'
    ]
    neu_label_idx = label_list.index("neu")
    label_indices = list(range(len(label_list)))
    label_indices.remove(neu_label_idx)
    return sklearn.metrics.f1_score(labels, preds, average="micro", labels=label_indices) * 100.0

def klue_re_auprc(probs, labels):
    """KLUE-RE AUPRC (with no_relation)"""
    labels = np.eye(30)[labels]
    score = np.zeros((30,))
    for c in range(30):
        targets_c = labels.take([c], axis=1).ravel()
        preds_c = probs.take([c], axis=1).ravel()
        precision, recall, _ = sklearn.metrics.precision_recall_curve(targets_c, preds_c)
        score[c] = sklearn.metrics.auc(recall, precision)
    return np.average(score) * 100.0

def compute_metrics(pred, label):
    """validation을 위한 metrics function"""
    labels = label
    preds = pred.argmax(-1)

    # calculate accuracy using sklearn's function
    f1 = klue_re_micro_f1(preds, labels)
    acc = accuracy_score(labels, preds)  # 리더보드 평가에는 포함되지 않습니다.

    return {
        "micro f1 score": f1,
        "accuracy": acc,
    }
def label_to_num(label):
    num_label = []
    # dict_label_to_num = {
    #     'neu' : [1, 0, 0, 0, 0], 
    #     'sad' : [0, 1, 0, 0, 0],
    #     'ang' : [0, 0, 1, 0, 0], 
    #     'hap' : [0, 0, 0, 1, 0],  
    #     'fea' : [0, 0, 0, 0, 1],
    # }
    dict_label_to_num = {
        'neu' : 0, 
        'sad' : 1,
        'ang' : 2, 
        'hap' : 3,  
        'fea' : 4,
    }
    for v in label:
        num_label.append(dict_label_to_num[v])

    return num_label

def load_data(dataset_dir):
    """csv 파일을 경로에 맡게 불러 옵니다."""
    pd_dataset = pd.read_csv(dataset_dir)
    dataset = preprocessing_dataset(pd_dataset)

    return dataset

class FocalLoss(nn.Module):
    def __init__(self, weight=None, gamma=0.5, reduction="mean"):
        nn.Module.__init__(self)
        self.weight = weight
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, input_tensor, target_tensor):
        log_prob = F.log_softmax(input_tensor, dim=-1)
        prob = torch.exp(log_prob)
        return F.nll_loss(
            ((1 - prob) ** self.gamma) * log_prob,
            target_tensor,
            weight=self.weight,
            reduction=self.reduction,
        )


class LabelSmoothingLoss(nn.Module):
    def __init__(self, classes=3, smoothing=0.0, dim=-1):
        super(LabelSmoothingLoss, self).__init__()
        self.confidence = 1.0 - smoothing
        self.smoothing = smoothing
        self.cls = classes
        self.dim = dim

    def forward(self, pred, target):
        pred = pred.log_softmax(dim=self.dim)
        with torch.no_grad():
            true_dist = torch.zeros_like(pred)
            true_dist.fill_(self.smoothing / (self.cls - 1))
            true_dist.scatter_(1, target.data.unsqueeze(1), self.confidence)
        return torch.mean(torch.sum(-true_dist * pred, dim=self.dim))


# https://gist.github.com/SuperShinyEyes/dcc68a08ff8b615442e3bc6a9b55a354
class F1Loss(nn.Module):
    def __init__(self, classes=30, epsilon=1e-7):
        super().__init__()
        self.classes = classes
        self.epsilon = epsilon

    def forward(self, y_pred, y_true):
        assert y_pred.ndim == 2
        assert y_true.ndim == 1
        y_true = F.one_hot(y_true, self.classes).to(torch.float32)
        y_pred = F.softmax(y_pred, dim=1)

        tp = (y_true * y_pred).sum(dim=0).to(torch.float32)
        tn = ((1 - y_true) * (1 - y_pred)).sum(dim=0).to(torch.float32)
        fp = ((1 - y_true) * y_pred).sum(dim=0).to(torch.float32)
        fn = (y_true * (1 - y_pred)).sum(dim=0).to(torch.float32)

        precision = tp / (tp + fp + self.epsilon)
        recall = tp / (tp + fn + self.epsilon)

        f1 = 2 * (precision * recall) / (precision + recall + self.epsilon)
        f1 = f1.clamp(min=self.epsilon, max=1 - self.epsilon)
        return 1 - f1.mean()


_criterion_entrypoints = {
    "CrossEntropy": nn.CrossEntropyLoss(),
    "focal": FocalLoss(),
    "label_smoothing": LabelSmoothingLoss(),
    "f1": F1Loss(),
}


def criterion_entrypoint(criterion_name):
    return _criterion_entrypoints[criterion_name]
