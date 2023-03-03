import sys
sys.path.append('/opt/ml/final/riffusion')
sys.path.append('/opt/ml/final/')

import os
from riffusion.cli import audio_to_image
from pydub import AudioSegment
from utils import *
import numpy as np
import pathlib

ori_path = '/opt/ml/final/mp3_original_folder'
output_dir_path = ''
sent_list =['funny',  'quirky', 'happy', 'angry',  'fear', 'sad',  'weird']
for sent in sent_list:
    sent_dir = os.path.join(ori_path, f'{sent}')
    if sent != 'funny':
        n_sent_dir = sent[0]
    else:
        n_sent_dir = sent[:2]

    for file in pathlib.Path(sent_dir).iterdir():
        sample_rate_converter(file, os.path.join(ori_path, f'{n_sent_dir}/{file.name}'), 22050, 8000)
        audio_segment = AudioSegment.from_file(os.path.join(ori_path, f'{n_sent_dir}/{file.name}'))
        duration_ms = 10 * 1000
        segment_duration_ms = int(audio_segment.duration_seconds * 1000)
        for i in range(1, 11):
            start_ms = np.random.randint(0, segment_duration_ms - duration_ms)
            trimmed_segement = audio_segment[start_ms:start_ms+duration_ms]

            clip_path = os.path.join(output_dir_path, 'part_'+str(i)+'.wav')
            trimmed_segement.export(clip_path, format='wav')
            audio_to_image(audio=clip_path, image=f'/opt/ml/final/spectrogram_folder/{sent}/{i}_{file.name[:-4]}.png')
