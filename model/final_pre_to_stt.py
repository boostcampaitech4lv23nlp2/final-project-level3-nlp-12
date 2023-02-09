import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'riffusion'))
from utils_final import *
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--code", default="1", help="code used to verify request") 
    parser.add_argument("--output_dir", default=os.path.join(BASE_DIR, 'serving/output'))
    parser.add_argument("--input_video_path", default='/opt/ml/final/serving/input/sample_honeybee.mp4')
    parser.add_argument("--audio_dir_path", default='/opt/ml/final/bgm_removed_audio')
    parser.add_argument("--extract_audio_path", default='/opt/ml/final/extract_audio/audio.mp3')
    parser.add_argument("--model_size", default='large')
    args, _ = parser.parse_known_args()

    sentiment_result, _ = pre_to_stt(args.input_video_path, args.audio_dir_path, args.extract_audio_path, args.model_size)
    #print(sentiment_result)
    print(' '.join(map(str, sentiment_result)))

#current_output : [0 25 None 25 67 None 67 72 None 72 80 surprise 80 87 fear 87 93 anger 93 100 fear]

def pre_to_stt(input_video_path, output_dir_path, extract_audio_path, model_size):
    vocal_file_path = convert_video_to_audio(input_video_path, output_dir_path, extract_audio_path)
    sentiment_result = audio_to_sentiment(model_size, vocal_file_path)
    return sentiment_result, vocal_file_path

if __name__ == '__main__':
    main()

