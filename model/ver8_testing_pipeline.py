import whisper
import torch

import os
from typing import Iterator, TextIO

from transformers import pipeline

import argparse


# 나중에 util로 빼기
def write_txt(transcript: Iterator[dict], file: TextIO):
    for segment in transcript:
        print(segment['text'].strip(), file=file, flush=True)
        
#
def summarization_test():
    # setting
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="large", help="name of the Whisper model to use")
    parser.add_argument("--input_audio_path",default="/opt/ml/input/final_test/dataset/")
    parser.add_argument("--input_file",default="test02.mp4")
    parser.add_argument("--output_dir",default="/opt/ml/input/final_test/result")
    args = parser.parse_args().__dict__
    
    # 수정할 부분 : ok
    model_name: str = args.pop("model")
    input_path: str = args.pop("input_audio_path")
    input_file: str = args.pop("input_file")
    output_dir: str = args.pop("output_dir")
    
    # 1-1. stt 실행
    model = whisper.load_model(model_name)  # model_name : large
    model = model.to(torch.device("cuda"))
    result = model.transcribe(input_path+input_file,fp16=False,language='English') 
    
    # 1-2. 전처리
    input_txt=''
    for line in result["segments"]:
        input_txt+=line['text']+'\n'
        
    # 2. summary 실행 : print
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary_output = summarizer(input_txt, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
    
    # 3. 저장하기
    # audio_basename = input_file[:-4]    # .wav 빼고 파일명만
    # with open(os.path.join(output_dir, audio_basename + ".txt"), "w", encoding="utf-8") as txt:
    #         txt.write(summary_output)
    print(summary_output)
    
if __name__ == '__main__':
    summarization_test()
