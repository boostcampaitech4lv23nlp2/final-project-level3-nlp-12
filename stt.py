import whisper
import torch
import pickle
import argparse
import os

def main():
    # setting
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="large", help="name of the Whisper model to use") 
    parser.add_argument("--code", default="1", help="code of the request, used to identify which audio/text to use")
    parser.add_argument("--input_file",default="/opt/ml/input/code/final-project-level3-nlp-12/test01.wav")        # input 파일명
    parser.add_argument("--output_dir",default="/opt/ml/input/final_test/result")           # 결과 저장 경로
    args, _ = parser.parse_known_args()
    model = whisper.load_model(args.model)  # model_name : large(default)
    model = model.to(torch.device("cuda"))
    result = model.transcribe(args.input_file,fp16=False,language='English') 
    # 1-2. 전처리
    input_txt=''
    timeline = []
    for line in result["segments"]:
        input_txt+=line['text']+'\n'
        timeline.append([line['start'], line['end']])
    path = os.path.join(args.output_dir, f'text_{args.code}.pickle')
    with open(path,"wb") as fw:
        pickle.dump(input_txt, fw)
    path = os.path.join(args.output_dir, f'timeline_{args.code}.pickle')
    with open(path,"wb") as fw:
        pickle.dump(timeline, fw)
if __name__ == '__main__':
    main()