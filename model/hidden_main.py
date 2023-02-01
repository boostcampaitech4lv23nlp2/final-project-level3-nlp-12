import whisper
import torch
import os
from transformers import pipeline
from sum_by_sent import SentimentModel
from hidden_split_audio import *
import argparse
import numpy as np
import pickle


def main():
    '''
    < process >
    1. 입력된 음성파일에 stt 실행(whisper)하여 대사의 start-end 시간을 추출(전처리하기)
    2. 1번에서 구한 start-end 시간 데이터로 입력된 음성파일을 split(tmp_hidden 폴더에 저장)
    3. split된 음성을 각각 whisper encodeer -> sent classifier 실행하여 감정 추출
    '''
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # setting
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="large", help="name of the Whisper model to use")    # whisper model
    parser.add_argument("--code", default="1", help="code used to verify request") 
    parser.add_argument("--input_file",default=os.path.join(BASE_DIR, "honeybee.wav"))        # input 파일명
    parser.add_argument("--output_dir",default=os.path.join(BASE_DIR, 'tmp_hidden'))           # split한 음성 파일 저장 경로 : tmp_hidden
    args, _ = parser.parse_known_args()

    # 1-1. stt 실행
    model = whisper.load_model(args.model)  # model_name : large(default)
    model = model.to(torch.device("cuda"))
    result = model.transcribe(args.input_file,fp16=False,language='English')
    # 1-2. 전처리
    timeline = []
    for line in result["segments"]:
        timeline.append([line['start'], line['end'],line['text']])          # [ start :str ,end :str ,text :str ] 
    # 2. split
    audios = split_run(args.input_file, timeline)   # audios :list ->  [array([~], dtype=float32),,,]
    # 3. TODO
    

if __name__ == '__main__':
    main()
