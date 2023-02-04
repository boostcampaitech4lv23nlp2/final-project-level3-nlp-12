import os
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import moviepy.editor as mp
import random
import whisper
import torch
from sum_by_sent import SentimentModel
from itertools import chain
from pydub import AudioSegment

def convert_video_to_audio(video_path, output_dir_path, audio_path):
    """Converts video to audio using MoviePy library
    that uses `ffmpeg` under the hood"""
    # os.system(f'pip install spleeter')
    my_clip = mp.VideoFileClip(f"{video_path}")
    my_clip.audio.write_audiofile(f"{audio_path}")
    os.system(f"spleeter separate -p spleeter:2stems -o {output_dir_path} {audio_path}")
    audio_folder = audio_path.split('/')[-1][:-4]
    vocal_file_path = f'{output_dir_path}/{audio_folder}/vocals.wav'
    return vocal_file_path

def audio_to_sentiment(model_size, input_file):
    model = whisper.load_model(model_size)
    model = model.to(torch.device("cuda"))
    result = model.transcribe(input_file,fp16=False,language='English') 
    
    input_txt=''
    timeline = []
    for line in result["segments"]:
        input_txt+=line['text']+'\n'
        timeline.append([line['start'], line['end']])

    sentiment_task = SentimentModel(input_txt, timeline)
    sentiments = sentiment_task.run()
    print(*list(chain(*sentiments)))
    sentiment_output = list(chain(*sentiments))
    # with open(os.path.join(args.output_dir, f'sentiments_{args.code}.pickle'), 'wb') as fw:
    #     pickle.dump(sentiments, fw)
    return sentiment_output

def sent2prompt(sentiment, n_seg):
    prompt_seg = {
        'anger' : ['aggressive','wu-tang track', 'angry rap', 'Daft Punk', '150-180 BPM'],
        'disgust': ['radio active', 'distorted bass guitar', 'low-tuned synthesizer', '60-80 BPM'],
        'sadness' : ['tinny', 'hollow', 'treble', 'crackles', 'pops', 'echo', 'cave'],
        'fear' : ['gospel', 'break','Plastic noises','white noise','screaming'],
        'joy' : ['breakcore','mozart', 'the best song','freemasonry','funky vibe'],
        'surprise' : ['EDM','daft','!!!!!!!!!!','a sine wave'],
    }
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt = ' '.join(random.sample(prompt_seg[sentiment], n_seg))
    seed_audio = os.path.join(BASE_DIR, f'riffusion/seed_images/{sentiment}/'+ random.choice([i for i in os.listdir(os.path.join(BASE_DIR, f'riffusion/seed_images/{sentiment}')) if 're' in i]))
    return prompt, seed_audio

def merge_music(file1, file2, merged_music_path):
    # load the audio files
    audio1 = AudioSegment.from_file(file1)
    audio2 = AudioSegment.from_file(file2)

    # merge the audio files
    #merged_audio = audio1.overlay(audio2)
    if audio1.duration_seconds == audio2.duration_seconds:
        merged_audio = audio1.overlay(audio2)
    else:
        print("Both files must have the same duration")
        print("Result file will have the same duration with audio2")
        merged_audio = audio1[:audio2.duration_seconds*1000].overlay(audio2)
    merged_audio.export(f"{merged_music_path}", format="mp3")

def video_music_merge(video, audio, output_dir):
    start, end, composite = 0, 100, False
    # load the video
    video_clip = VideoFileClip(video).subclip(start, end)
    # load the audio
    audio_clip = AudioFileClip(audio)
    # use the volume factor to increase/decrease volume
    #audio_clip = audio_clip.volumex(volume_factor)
    # if end is not set, use video clip's end
    # if not end:
    #     end = audio_clip.end
    # make sure audio clip is less than video clip in duration
    # setting the start & end of the audio clip to `start` and `end` paramters
    #audio_clip = audio_clip.subclip(start, end)
    # composite with the existing audio in the video if composite parameter is set
    if composite:
        final_audio = CompositeAudioClip([video_clip.audio, audio_clip])
    else:
        final_audio = audio_clip
    # add the final audio to the video
    final_clip = video_clip.set_audio(final_audio)
    # save the final clip
    final_clip.write_videofile(f'{output_dir}/final_video.mp4', codec='libx264')
