from transformers import pipeline
import re

class SentimentModel():
    def __init__(self, text, timeline):
        self.time = timeline
        self.text = self.preprocessing(text)
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)
    
    def preprocessing(self, text):
        text = re.sub(r'\[.+\]', '', text).split('\n')
        text = [t.strip() for t in text if t]
        return text
    
    def run(self):
        sentiments = []
        text = self.text
        for t in text:
            result = self.classifier(t)[0]
            result.sort(key = lambda x: x['score'], reverse = True)
            sentiments.append(result[0]['label'])
        sentiment = None
        contents = []
        min = 5
        max = 20
        start = 0
        for idx, (x, y) in enumerate(zip(sentiments, self.time)):
            if sentiment == None:
                if x != 'neutral':
                    contents.append([start, int(y[0]), None])
                    sentiment = x
                    start = int(y[0])
            else:
                if x != sentiment and x != 'neutral':
                    if int(y[0]) - start > min and int(y[0]) - start < max:
                        contents.append([start, int(y[0]), sentiment])
                    else:
                        contents.append([start, int(y[0]), None])
                    sentiment = x
                    start = int(y[0])
            if idx == len(sentiments)-1:
                if min < int(y[1]-y[0]) < max:
                    contents.append([int(y[0]), int(y[1]), sentiment])
                else:
                    contents.append([int(y[0]), int(y[1]), None])
        return contents