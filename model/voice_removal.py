#!pip install spleeter
import os
import moviepy.editor as mp
import argparse

class voice_removal:
    def __init__(self, video_path, audio_path, output_path):
        self.video_path = video_path
        self.audio_path = audio_path
        self.output_path = output_path

    def run(self):
        #video_path = '/opt/ml/final/sample_video.mp4'
        #audio_path = '/opt/ml/final/make_example1.mp3'
        #output_path = 'output'
        
        my_clip = mp.VideoFileClip(f"{self.video_path}")
        my_clip.audio.write_audiofile(f"{self.audio_path}")
        os.system(f"spleeter separate -p spleeter:2stems -o {self.output_path} {self.audio_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path", default='/opt/ml/final/sample_video.mp4') 
    parser.add_argument("--audio_path", default='/opt/ml/final/make_example1.mp3') 
    parser.add_argument("--output_path",default='output')        # input 파일명
    args, _ = parser.parse_known_args()
    voice_removal(args.video_path, args.audio_path, args.output_path).run()