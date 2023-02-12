import sys
sys.path.append('/opt/ml/final/riffusion')
sys.path.append('/opt/ml/final/')

from datasets import load_dataset
import pandas as pd
import os
from urllib import request
from pydub import AudioSegment
from model import downsampling
import numpy as np
import time
import random
import requests

ori_path = '/opt/ml/final/mp3_original_folder'
dataset = load_dataset("Chr0my/Epidemic_music")

sent_list =['angry',  'fear', 'sad',  'weird',  'funny',  'quirky']

opener = request.URLopener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]


# opener = request.build_opener()
# opener.addheaders = [('[Windows64,Win64][Chrome,58.0.3029.110][KOS] \
#     Mozilla/5.0 Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)', 'Chrome/58.0.3029.110 Safari/537.36')]
# request.install_opener(opener)
_df = pd.DataFrame(dataset['train'])
df= _df.sort_index(ascending=False)
#print(df.head())

for i in df.iterrows(): #df.iterrows()
    inter_section = list(set(i[1]['moods']) & set(sent_list))
    idx = i[0]
    # if idx < 5153:
    #     continue

    if idx % 500 == 0:
        time.sleep(random.randint(2,4))
    
    if inter_section:
        print(idx)
        print(inter_section)
        genres = i[1]['genres']
        new_path = os.path.join(ori_path, f'{inter_section[0]}/{idx}.mp3')
        content = requests.get(i[1]['url'])
        with open(new_path, "wb") as file:
            file.write(content.content)
        time.sleep(0.3)
        

# for idx, i in enumerate(dataset['train']):
#     #moods = ' '.join(i['moods'])
#     if idx < 5062:
#         continue
#     if idx % 30 == 0:
#         time.sleep(3)
#     inter_section = list(set(i['moods']) & set(sent_list))
#     if inter_section:
#         print(idx)
#         print(inter_section)
#         genres = i['genres']
#         new_path = os.path.join(ori_path, f'{inter_section[0]}/{idx}.mp3')
#         request.urlretrieve(i['url'], os.path.join(ori_path, new_path))

print(3) 
#     #audio_to_image(audio=new_path, image=os.path.join(base_path, f'{idx}_{genres}_{moods}.png'))


# ori_path = '/opt/ml/final/mp3_original_folder'
# new_path = os.path.join(ori_path, f'{inter_section[0]}/{idx}.mp3')
# #audio_segment = AudioSegment.from_file(new_path)
#duration_ms = 10 * 1000
#segment_duration_ms = int(audio_segment.duration_seconds * 1000)
#start_ms = np.random.randint(0, segment_duration_ms - duration_ms)
#audio_segment[start_ms:start_ms+duration_ms]
#downsampling.down_sample(new_path, f're_{new_path[:-4]}.mp3')
#print(dataset)