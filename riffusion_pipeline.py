import torch
from transformers import pipeline
import sys
sys.path.append('/opt/ml/input/code/final-project-level3-nlp-12/riffusion')
from _interpolation import Riffusion_interpolation
from utils import *
import argparse
import numpy as np
from riffusion.cli import audio_to_image
import pickle
import pydub

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--code", default="1", help="code used to verify request") 
    parser.add_argument("--output_dir",default="/opt/ml/input/code/final-project-level3-nlp-12/tmp")  
    args, _ = parser.parse_known_args()
    with open(os.path.join(args.output_dir, f'sentiments_{args.code}.pickle'), 'rb') as fw:
        sentiments = pickle.load(fw)
    for i, s in enumerate(sentiments):
        prompt, seed_audio = sent2prompt(s[2], 1) # s[2]는 감정(sadness, joy 등)이고, prompt와 seed image(둘다 리스트 4개) 반환
        width = int((s[1]-s[0]) // 5 + 1) # interpolation step으로 1당 5초로 계산
        duration_ms = s[1]-s[0]
        segment = pydub.AudioSegment.from_file(seed_audio[i])
        output_dir_path = f'/opt/ml/input/code/final-project-level3-nlp-12/riffusion/seed_images/{s[2]}'
        extension = 'wav'
        print(s, duration_ms)
        segment_duration_ms = int(segment.duration_seconds * 1000)
        clip_start_ms = np.random.randint(0, segment_duration_ms - duration_ms)
        clip = segment[clip_start_ms : clip_start_ms + 5000]
        clip_path = os.path.join(output_dir_path, 'test'+str(i)+'.wav')
        clip.export(clip_path, format=extension)
        audio_to_image(audio=clip_path, image=f'/opt/ml/input/code/final-project-level3-nlp-12/riffusion/seed_images/{s[2]}.png')
        seed_image = f'/opt/ml/input/code/final-project-level3-nlp-12/riffusion/seed_images/{s[2]}.png'
        riffusion = Riffusion_interpolation(prompt[i], prompt[i], seed_image,num_inference_steps=50, num_interpolation_steps= width) # prompt와 seed image로 bgm 생성하고, 저장까지 진행
        riffusion.run(i)
        torch.cuda.empty_cache()
if __name__ == '__main__':
    main()