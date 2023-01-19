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
    parser.add_argument("--model_dir", type=str, default=None, help="the path to save model files; uses ~/.cache/whisper by default")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu", help="device to use for PyTorch inference")
    parser.add_argument("--output_dir", "-o", type=str, default=".", help="directory to save the outputs")
    parser.add_argument("--file",default="/opt/ml/input/final_test/dataset/test02.wav")
    args = parser.parse_args()
    
    # 수정할 부분
    model_name: str = args.pop("model")
    input_file: str = args.pop("file")
    
    # 1-1. stt 실행
    model = whisper.load_model(model_name)  # model_name : large
    model = model.to(torch.device("cuda"))
    result = model.transcribe(input_file,fp16=False,language='English') 
    
    # 1-2. 전처리
    input_txt=''
    for line in result["segments"]:
        input_txt+=line['text']+'\n'
        
    # 2. summary 실행 : print
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    r = summarizer(input_txt, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
    
    print(r)

if __name__ == '__main__':
    summarization_test()
