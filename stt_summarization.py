import whisper
import torch
import sys
sys.path.append('/opt/ml/input/final-project-level3-nlp-12/riffusion')
import os
from typing import Iterator, TextIO
from transformers import pipeline
from _interpolation import Riffusion_interpolation
from sum_by_sent import SentimentModel
import argparse
from utils import *
import pydub
import numpy as np
from riffusion.cli import audio_to_image
import io

def main():
    # setting
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="large", help="name of the Whisper model to use") 
    parser.add_argument("--input_audio_path",default="/opt/ml/input/final_test/dataset/")   # input 파일이 있는 경로(폴더)
    parser.add_argument("--input_file",default="/opt/ml/input/final-project-level3-nlp-12/test01.wav")        # input 파일명
    parser.add_argument("--output_dir",default="/opt/ml/input/final_test/result")           # 결과 저장 경로
    args = parser.parse_args().__dict__ # args를 딕셔너리 형태로 -> args.pop(key)

    model_name: str = args.pop("model")
    input_path: str = args.pop("input_audio_path")
    input_file: str = args.pop("input_file")
    output_dir: str = args.pop("output_dir")
   
    # 1-1. stt 실행
    model = whisper.load_model(model_name)  # model_name : large(default)
    model = model.to(torch.device("cuda"))
    result = model.transcribe(input_file,fp16=False,language='English') 
    # 1-2. 전처리
    input_txt=''
    timeline = []
    for line in result["segments"]:
        input_txt+=line['text']+'\n'
        timeline.append([line['start'], line['end']])
    sentiment_task = SentimentModel(input_txt, timeline)
    sentiments = sentiment_task.run() # 전체 텍스트 전처리 및 line by line 감정 분석 후 List[List] 형태로 반환

    for s in sentiments:
        prompt, seed_audio = sent2prompt(s[2], 4) # s[2]는 감정(sadness, joy 등)이고, prompt와 seed image(둘다 리스트 4개) 반환
        width = (s[1]-s[0]) // 5 + 1 # interpolation step으로 1당 5초로 계산
        for i in range(2):
            duration_ms = s[1]-s[0]
            segment = pydub.AudioSegment.from_file(seed_audio[i])
            output_dir_path = f'/opt/ml/input/final-project-level3-nlp-12/riffusion/seed_audios/{s[2]}'
            extension = 'wav'

            segment_duration_ms = int(segment.duration_seconds * 1000)
            clip_start_ms = np.random.randint(0, segment_duration_ms - duration_ms)
            clip = segment[clip_start_ms : clip_start_ms + segment_duration_ms]
            clip_path = os.path.join(output_dir_path, 'test'+str(i)+'.wav')
            clip.export(clip_path, format=extension)
            audio_to_image(audio=clip_path, image=f'/opt/ml/input/final-project-level3-nlp-12/riffusion/seed_images/{s[2]}.png')
            seed_image = f'/opt/ml/input/final-project-level3-nlp-12/riffusion/seed_images/{s[2]}.png'
            riffusion = Riffusion_interpolation(prompt[i], prompt[i], seed_image, width) # prompt와 seed image로 bgm 생성하고, 저장까지 진행
            riffusion.run(i)
        break



if __name__ == '__main__':
    main()
