import os
import pickle as pickle
# import sys
# sys.path.append('/opt/ml/final/pl')
import pandas as pd
import pytorch_lightning as pl
import torch
import transformers
from tqdm.auto import tqdm
from utils.util import *

class Dataset(torch.utils.data.Dataset):
    """Dataset 구성을 위한 Class"""

    def __init__(self, audio, labels):
        self.audio = audio
        self.labels = labels

    def __getitem__(self, idx):
        item = {}
        item['audio'] = self.audio[idx]
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)


class Dataloader(pl.LightningDataModule):
    def __init__(self, model_name, batch_size, shuffle, train_path, test_path, split_seed=42):
        super().__init__()
        self.model_name = model_name
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.split_seed = split_seed

        self.train_path = train_path
        self.test_path = test_path

        self.train_dataset = None
        self.val_dataset = None
        self.test_dataset = None
        self.predict_dataset = None
        total_data = load_data(self.train_path)
        tmp_data = total_data.sample(frac=0.9, random_state=self.split_seed)
        self.test_data = total_data.drop(tmp_data.index)
        self.test_data.reset_index(inplace=True, drop=True)
        self.train_data = tmp_data.sample(frac=0.9, random_state=self.split_seed)
        self.val_data = tmp_data.drop(self.train_data.index)
        self.train_data.reset_index(inplace=True, drop=True)
        self.val_data.reset_index(inplace=True, drop=True)

    def setup(self, stage="fit"):
        if stage == "fit":
            # 학습 데이터을 호출
            train_label = label_to_num(self.train_data["label"].values)
            val_label = label_to_num(self.val_data["label"].values)

            self.train_dataset = Dataset(self.train_data['audio'], train_label)
            self.val_dataset = Dataset(self.val_data['audio'], val_label)

        if stage == "test":
            val_label = label_to_num(self.val_data["label"].values)
            self.test_dataset = Dataset(self.val_data['audio'], val_label)

        if stage == "predict":
            predict_label = label_to_num(self.test_data["label"].values)
            self.predict_dataset = Dataset(self.test_data['audio'], predict_label)

    def train_dataloader(self):
        return torch.utils.data.DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            shuffle=self.shuffle,
            num_workers=4,
        )

    def val_dataloader(self):
        return torch.utils.data.DataLoader(self.val_dataset, batch_size=self.batch_size, num_workers=4)

    def test_dataloader(self):
        return torch.utils.data.DataLoader(self.test_dataset, batch_size=self.batch_size, num_workers=4)

    def predict_dataloader(self):
        return torch.utils.data.DataLoader(self.predict_dataset, batch_size=self.batch_size, num_workers=4)
