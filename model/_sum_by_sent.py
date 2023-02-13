import re

from transformers import pipeline

class SentimentModel:
    def __init__(self, text, timeline):
        self.time = timeline
        self.text = self.preprocessing(text)
        # gself.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.classifier = pipeline(
            "text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True
        )

    def preprocessing(self, text):
        text = re.sub(r"\[.+\]", "", text).split("\n")
        text = [t.strip() for t in text if t]
        return text

    def run(self):
        sentiments = []
        text = self.text
        for t in text:
            result = self.classifier(t)[0]
            result.sort(key=lambda x: x["score"], reverse=True)
            sentiments.append(result[0]["label"])
        sentiment = None
        contents = []
        min_sec = 5
        # max = 20 #delete max
        start = 0
        for idx, (x, y) in enumerate(zip(sentiments, self.time)):
            # if pre-sentiment is None
            if sentiment == None:
                if x != "neutral":
                    # add empty sentiment until new sentiment emerge
                    contents.append([start, int(y[0]), None])
                    sentiment = x
                    start = int(y[0])
            # if pre-sentiment is sth
            else:
                if x != sentiment and x != "neutral":
                    # if int(y[0]) - start > min and int(y[0]) - start < max:
                    if int(y[0]) - start > min_sec:
                        contents.append([start, int(y[0]), sentiment])
                    else:
                        contents.append([start, int(y[0]), None])
                    sentiment = x
                    start = int(y[0])

            if idx == len(sentiments) - 1:
                if int(y[1] - y[0]) > min_sec:
                    contents.append([int(y[0]), int(y[1]), sentiment])
                else:
                    contents.append([int(y[0]), int(y[1]), None])

        # add rule for None sentiment between two same sentiments
        for cont in range(1, len(contents) - 1):
            if contents[cont][2] == None and contents[cont][1] - contents[cont][0] <= min_sec:
                if contents[cont - 1][2] == contents[cont + 1][2]:
                    contents[cont][2] = contents[cont + 1][2]

        return contents
