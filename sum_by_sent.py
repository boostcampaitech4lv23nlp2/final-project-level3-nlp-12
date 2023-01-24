import whisper
import torch
import sys
sys.path.append('/opt/ml/input/code/final-project-level3-nlp-12/riffusion')
import os
from typing import Iterator, TextIO
from transformers import pipeline
from interpolation import Riffusion_interpolation
import re

class SentimentModel():
    def __init__(self, text):
        self.text = self.preprocessing(text)
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.sentiment = pipeline("sentiment-analysis", model='cardiffnlp/twitter-roberta-base-sentiment-latest', tokenizer='cardiffnlp/twitter-roberta-base-sentiment-latest')
    
    def preprocessing(self, text):
        text = re.sub(r'\[.+\]', '', text).split('\n')
        text = [t.strip() for t in text if t]
        return text
    
    def run(self):
        sentiments = []
        text = self.text
        print(text)
        for t in text:
            sentiments.append(self.sentiment(t))
        flag = None
        contents = []
        for x,y in zip(text, sentiments):
            if flag == None:
                if y[0]['label'] == 'positive':
                    flag = True
                    contents.append([x])
                elif y[0]['label'] == 'negative':
                    flag = False
                    contents.append([x])
            else:
                if flag == False:
                    if y[0]['label'] == 'positive':
                        flag = True
                        contents.append([x])
                    else:
                        contents[-1] += [x]
                else:
                    if y[0]['label'] == 'negative':
                        flag = False
                        contents.append([x])
                    else:
                        contents[-1] += [x]
        contents = list(map(''.join, contents))
        summarized = []
        for x in contents:
            summarized.append(self.summarizer(x))
        return summarized
