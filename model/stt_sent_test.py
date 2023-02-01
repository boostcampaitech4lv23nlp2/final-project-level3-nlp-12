import whisper
import torch
import os
from transformers import pipeline
from sum_by_sent import SentimentModel
import argparse
import numpy as np
import pickle
from itertools import chain


def main():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # setting
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="large", help="name of the Whisper model to use") 
    parser.add_argument("--code", default="1", help="code used to verify request") 
    # parser.add_argument("--input_file",default=os.path.join(BASE_DIR, "serving/input/honeybee.wav"))        # input 파일명
    parser.add_argument("--input_file")        # input 파일명
    parser.add_argument("--output_dir",default=os.path.join(BASE_DIR, 'serving/output'))           # 결과 저장 경로
    args, _ = parser.parse_known_args()
    # 1-1. stt 실행
    model = whisper.load_model(args.model)  # model_name : large(default)
    model = model.to(torch.device("cuda"))
    result = model.transcribe(args.input_file,fp16=False,language='English') 
    # 1-2. 전처리
    input_txt=''
    timeline = []
    for line in result["segments"]:
        input_txt+=line['text']+'\n'
        timeline.append([line['start'], line['end']])
    print(input_txt)
    sentiment_task = SentimentModel(input_txt, timeline)
    sentiments = sentiment_task.run() # 전체 텍스트 전처리 및 line by line 감정 분석 후 List[List] 형태로 반환, [[시작 시간, 끝나는 시간, 감정], [], ...]
    # with open(os.path.join(args.output_dir, f'sentiments_{args.code}.pickle'), 'wb') as fw:
    #     pickle.dump(sentiments, fw)

    print(*list(chain(*sentiments))) # 80 94 fear 118 124 surprise

if __name__ == '__main__':
    main()
