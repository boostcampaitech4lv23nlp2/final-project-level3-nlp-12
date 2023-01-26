import os
import sys
from moviepy.editor import VideoFileClip
import random

def convert_video_to_audio_moviepy(video_file, output_ext="mp3"):
    """Converts video to audio using MoviePy library
    that uses `ffmpeg` under the hood"""
    filename, ext = os.path.splitext(video_file)
    clip = VideoFileClip(video_file)
    clip.audio.write_audiofile(f"{filename}.{output_ext}")


def sent2prompt(sentiment, n_seg):
    prompt_seg = {
        'anger' : ['aggressive','wu-tang track', 'angry rap', 'Daft Punk', '150-180 BPM'],
        'disgust': ['radio active', 'distorted bass guitar', 'low-tuned synthesizer', '60-80 BPM'],
        'sad' : ['tinny', 'hollow', 'treble', 'crackles', 'pops', 'echo', 'cave'],
        'fear' : ['gospel', 'break','Plastic noises','white noise','screaming'],
        'joy' : ['breakcore','mozart', 'the best song','freemasonry','funky vibe'],
        'surprise' : ['EDM','daft','!!!!!!!!!!','a sine wave']
    }
    prompt = [' '.join(random.sample(prompt_seg[sentiment], n_seg)) for _ in range(4)]
    ran_idx = random.sample(range(3), 2)
    seed_audio = [f'/opt/ml/input/code/final-project-level3-nlp-12/riffusion/seed_images/{sentiment}/{idx}.mp3' for idx in ran_idx]
    return prompt, seed_audio