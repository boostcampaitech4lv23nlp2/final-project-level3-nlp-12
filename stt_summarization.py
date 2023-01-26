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
from riffusion.cli import audio_to_image
import io

def main():
    # setting
    parser = argparse.ArgumentParser()
    parser.add_argument("--code", default="1", help="code of the request, used to identify which audio/text to use")
    parser.add_argument("--output_dir",default="/opt/ml/input/final_test/result")           # 결과 저장 경로
    args, _ = parser.parse_known_args()
    # 1-1. stt 실행
    with open(os.path.join(args.output_dir, f''),"wb") as fw:
        pickle.LOAD(my_list, fw)
    sentiment_task = SentimentModel(input_txt, timeline)
    sentiments = sentiment_task.run() # 전체 텍스트 전처리 및 line by line 감정 분석 후 List[List] 형태로 반환

    for s in sentiments:
        prompt, seed_audio = sent2prompt(s[2], 4) # s[2]는 감정(sadness, joy 등)이고, prompt와 seed image(둘다 리스트 4개) 반환
        width = (s[1]-s[0]) // 5 + 1 # interpolation step으로 1당 5초로 계산
        for i in range(2):
            duration_ms = s[1]-s[0]
            segment = pydub.AudioSegment.from_file(seed_audio[i])
            output_dir_path = f'/opt/ml/input/code/final-project-level3-nlp-12/riffusion/seed_images/{s[2]}'
            extension = 'wav'

            segment_duration_ms = int(segment.duration_seconds * 1000)
            clip_start_ms = np.random.randint(0, segment_duration_ms - duration_ms)
            clip = segment[clip_start_ms : clip_start_ms + segment_duration_ms]
            clip_path = os.path.join(output_dir_path, 'test'+str(i)+'.wav')
            clip.export(clip_path, format=extension)
            seed_image = audio_to_image(audio=clip_path, image=f'/opt/ml/input/code/final-project-level3-nlp-12/riffusion/seed_images/{s[2]}.png')
            
            riffusion = Riffusion_interpolation(prompt[i], prompt[i], seed_image, width) # prompt와 seed image로 bgm 생성하고, 저장까지 진행
            riffusion.run(i)
        break



if __name__ == '__main__':
    main()
