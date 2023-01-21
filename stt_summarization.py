import whisper
import torch
import os
from transformers import pipeline
import argparse

def test():
    # setting
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="large", help="name of the Whisper model to use") 
    parser.add_argument("--input_audio_path",default="/opt/ml/input/final_test/dataset/")   # input 파일이 있는 경로(폴더)
    parser.add_argument("--input_file",default="test02.wav")                                # input 파일명
    parser.add_argument("--output_dir",default="/opt/ml/input/final_test/result")           # 결과 저장 경로
    args = parser.parse_args().__dict__ # args를 딕셔너리 형태로 -> args.pop(key)

    model_name: str = args.pop("model")
    input_path: str = args.pop("input_audio_path")
    input_file: str = args.pop("input_file")
    output_dir: str = args.pop("output_dir")
   
    # 1-1. stt 실행
    model = whisper.load_model(model_name)  # model_name : large(default)
    model = model.to(torch.device("cuda"))
    result = model.transcribe(input_path+input_file,fp16=False,language='English') 
        
    # 2-1. summary 실행 : print
    input_txt=''
    for line in result["segments"]:
        input_txt+=line['text']+'\n'
        
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary_output = summarizer(input_txt, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
    
    # 4. 감성분석 모델 붙이기
    
    
    # 5. 저장하기 : txt파일
    audio_basename = input_file[:-4]    # .wav 빼고 파일명만
    with open(os.path.join(output_dir, audio_basename + ".txt"), "w", encoding="utf-8") as txt:
            txt.write(summary_output)

if __name__ == '__main__':
    test()
