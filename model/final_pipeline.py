import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'riffusion'))
from _interpolation import Riffusion_interpolation
from utils_final import *
import argparse
import numpy as np
from riffusion.cli import audio_to_image
import pydub
from pydub import AudioSegment
import GPUtil
import torch
import gc

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--code", default="1", help="code used to verify request") 
    parser.add_argument("--output_dir", default=os.path.join(BASE_DIR, 'tmp'))
    parser.add_argument("--input_video_path", default='/opt/ml/final/serving/input/honeybee.mp4')
    parser.add_argument("--audio_dir_path", default='/opt/ml/final/bgm_removed_audio')
    parser.add_argument("--extract_audio_path", default='/opt/ml/final/extract_audio/audio.mp3')
    parser.add_argument("--model_size", default='large')
    
    #parser.add_argument("--sentiment_string",default="0 0 None 0 9 joy 9 19 disgust 19 23 None 23 35 sadness 35 45 surprise 45 48 None 48 51 None 51 54 None")
    args, _ = parser.parse_known_args()
    sentiment_result, vocal_file_path = pre_to_stt(args.input_video_path, args.audio_dir_path, args.extract_audio_path, args.model_size)
    new_bgm = stt_to_rif(args.output_dir, args.code, sentiment_result)
    
    final_path = f'{args.output_dir}/final'
    if not os.path.exists(final_path):
        os.makedirs(final_path)
    merged_music_path = f'{final_path}/merged_music.mp3' #merged_music / format 'mp3'
    merge_music(new_bgm, vocal_file_path, merged_music_path)
    final_music_path = f'{final_path}/resampled_merged_music.mp3'
    sample_rate_convert(merged_music_path, final_music_path, origin_sr=8000, resample_sr=22050)
    video_music_merge(args.input_video_path, final_music_path, final_path, args.code)
    print(f'final video file created in {final_path} directory')

def pre_to_stt(input_video_path, output_dir_path, extract_audio_path, model_size):
    vocal_file_path = convert_video_to_audio(input_video_path, output_dir_path, extract_audio_path)
    sentiment_result = audio_to_sentiment(model_size, vocal_file_path)
    return sentiment_result, vocal_file_path

def stt_to_rif(output_dir, code, sentiment_result):
    output_audio_path = os.path.join(output_dir, f'audio_{code}.mp3')
    sentiments = [sentiment_result[i: i+3] for i in range(0, len(sentiment_result), 3)] # [[6, 12, 'surprise']]
    #print(sentiments)
    audio_seg = None

    for i, s in enumerate(sentiments):
        print(i, s)
        s[0] = int(s[0])
        s[1] = int(s[1])
        if s[2] == None:
            if audio_seg == None:
                audio_seg = AudioSegment.silent(duration=int(s[1]-s[0])* 1000)
            else:
                audio_seg += AudioSegment.silent(duration=int(s[1]-s[0])* 1000)
            continue
        prompt, seed_audio = sent2prompt(s[2], 1) # s[2]는 감정(sadness, joy 등)이고, prompt와 seed image(둘다 리스트 4개) 반환
        width = int((s[1]-s[0]) // 10 + 1) # interpolation step으로 1당 5초로 계산
        duration_ms = s[1]-s[0]
        segment = pydub.AudioSegment.from_file(seed_audio)
        output_dir_path = os.path.join(BASE_DIR, f'riffusion/seed_images/{s[2]}')
        extension = 'wav'
        segment_duration_ms = int(segment.duration_seconds * 1000)
        clip_start_ms = np.random.randint(0, segment_duration_ms - duration_ms)
        clip = segment[clip_start_ms : clip_start_ms + 10000]
        clip_path = os.path.join(output_dir_path, 'test'+str(i)+'.wav')
        clip.export(clip_path, format=extension)
        audio_to_image(audio=clip_path, image=os.path.join(BASE_DIR, f'riffusion/seed_images/{s[2]}.png'))
        seed_image = os.path.join(BASE_DIR, f'riffusion/seed_images/{s[2]}.png')
        riffusion = Riffusion_interpolation(prompt, prompt, seed_image,num_inference_steps=50, num_interpolation_steps= width) # prompt와 seed image로 bgm 생성하고, 저장까지 진행
        concat_seg = riffusion.run(i, code)
        if audio_seg == None:
            audio_seg = concat_seg
        else:
            audio_seg += concat_seg
        
        del segment, riffusion, seed_audio, seed_image, clip

        gc.collect()
        torch.cuda.empty_cache()
        GPUtil.showUtilization()
    audio_seg.export(output_audio_path, format="mp3")
    # TODO 모델팀 최종 output에 따라 파일 이름 규칙 정하기
    print(output_audio_path)
    return output_audio_path

if __name__ == '__main__':
    main()

