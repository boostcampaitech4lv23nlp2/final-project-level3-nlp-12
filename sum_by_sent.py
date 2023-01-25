import sys
sys.path.append('/opt/ml/input/code/final-project-level3-nlp-12/riffusion')
from transformers import pipeline
import re

class SentimentModel():
    def __init__(self, text, timeline):
        self.time = timeline
        self.text = self.preprocessing(text)
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        #self.sentiment = pipeline("sentiment-analysis", model='cardiffnlp/twitter-roberta-base-sentiment-latest', tokenizer='cardiffnlp/twitter-roberta-base-sentiment-latest')
        self.classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)
    
    def preprocessing(self, text):
        text = re.sub(r'\[.+\]', '', text).split('\n')
        text = [t.strip() for t in text if t]
        return text
    
    # def run(self):
    #     sentiments = []
    #     text = self.text
    #     for t in text:
    #         sentiments.append(self.sentiment(t))
    #     flag = None
    #     contents = []
    #     for x,y in zip(text, sentiments):
    #         if flag == None:
    #             if y[0]['label'] == 'positive':
    #                 flag = True
    #                 contents.append([x])
    #             elif y[0]['label'] == 'negative':
    #                 flag = False
    #                 contents.append([x])
    #         else:
    #             if flag == False:
    #                 if y[0]['label'] == 'positive':
    #                     flag = True
    #                     contents.append([x])
    #                 else:
    #                     contents[-1] += [x]
    #             else:
    #                 if y[0]['label'] == 'negative':
    #                     flag = False
    #                     contents.append([x])
    #                 else:
    #                     contents[-1] += [x]
    #     contents = list(map(''.join, contents))
    #     summarized = []
    #     for x in contents:
    #         summarized.append(self.summarizer(x))
    #     return summarized
    def run(self):
        sentiments = []
        text = self.text
        for t in text:
            result = self.classifier(t)[0]
            result.sort(key = lambda x: x['score'], reverse = True)
            sentiments.append(result[0]['label'])
        sentiment = None
        contents = []
        threshold = 5
        start = 0
        for x, y in zip(sentiments, self.time):
            if sentiment == None:
                if x != 'neutral':
                    sentiment = x
                    start = y[0]
            else:
                if x != sentiment and x != 'neutral':
                    if int(y[0]) - start >= threshold:
                        contents.append([start, int(y[0]), sentiment])
                    sentiment = x
                    start = int(y[0])
        return contents