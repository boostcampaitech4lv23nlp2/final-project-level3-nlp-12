import whisper
import torch
import sys
sys.path.append('/opt/ml/input/code/final-project-level3-nlp-12/riffusion')
import os
from typing import Iterator, TextIO
from transformers import pipeline
from interpolation import Riffusion_interpolation
from sum_by_sent import SentimentModel
import argparse
from utils import *
import pydub
import numpy as np

def main():
    # setting
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="large", help="name of the Whisper model to use") 
    parser.add_argument("--input_audio_path",default="/opt/ml/input/final_test/dataset/")   # input 파일이 있는 경로(폴더)
    parser.add_argument("--input_file",default="/opt/ml/input/code/final-project-level3-nlp-12/test01.wav")        # input 파일명
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
    for line in result["segments"]:
        input_txt+=line['text']+'\n'
    sentiment_task = SentimentModel(input_txt)
    sentiments = sentiment_task.run()

    for s in sentiments:
        prompt, seed_images = sent2prompt(s[2])
        width = (s[1]-s[0]) // 5 + 1
        for i in range(4):
            duration_ms = s[1]-s[0]
            segment = pydub.AudioSegment.from_file(audio)
            output_dir_path = '#path'
            extension = 'wav'

            segment_duration_ms = int(segment.duration_seconds * 1000)
            clip_start_ms = np.random.randint(0, segment_duration_ms - duration_ms)
            clip = segment[clip_start_ms : clip_start_ms + duration_ms]
            idx = 1
            clip_path = os.path.join(output_dir_path, idx)
            clip.export(clip_path, format=extension)
            Riffusion_interpolation(prompt[i], prompt[i], seed_images[i], width)
        break



if __name__ == '__main__':
    main()
