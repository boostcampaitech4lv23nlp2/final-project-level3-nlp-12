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
    
    # 2. summary 실행 : print
    input_txt=''
    for line in result["segments"]:
        input_txt+=line['text']+'\n'
    sentiment = SentimentModel(input_txt)
    summarized_content = sentiment.run()
    print(summarized_content)
    #TODO 감정 분류해주는 classifier 추가
    #sentiment = None
    #prompt_a = sen2prompt(sentiment1)
    #prompt_b = sen2prompt(sentiment2)
    #music = Riffusion_interpolation(prompt_a, prompt_b, num_inference_steps, num_interpolation_steps)


if __name__ == '__main__':
    main()
