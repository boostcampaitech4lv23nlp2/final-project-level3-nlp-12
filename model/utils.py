import os
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
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
        'sadness' : ['tinny', 'hollow', 'treble', 'crackles', 'pops', 'echo', 'cave'],
        'fear' : ['gospel', 'break','Plastic noises','white noise','screaming'],
        'joy' : ['breakcore','mozart', 'the best song','freemasonry','funky vibe'],
        'surprise' : ['EDM','daft','!!!!!!!!!!','a sine wave'],
    }
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt = ' '.join(random.sample(prompt_seg[sentiment], n_seg))
    seed_audio = os.path.join(BASE_DIR, f'riffusion/seed_images/{sentiment}/'+ random.choice(os.listdir(os.path.join(BASE_DIR, f'riffusion/seed_images/{sentiment}'))))
    return prompt, seed_audio

def video_music_merge(video, audio, output_dir):
    start, end, composite = 0, len(video), False
    # load the video
    video_clip = VideoFileClip(video)
    # load the audio
    audio_clip = AudioFileClip(audio)
    # use the volume factor to increase/decrease volume
    #audio_clip = audio_clip.volumex(volume_factor)
    # if end is not set, use video clip's end
    if not end:
        end = audio_clip.end
    # make sure audio clip is less than video clip in duration
    # setting the start & end of the audio clip to `start` and `end` paramters
    audio_clip = audio_clip.subclip(start, end)
    # composite with the existing audio in the video if composite parameter is set
    if composite:
        final_audio = CompositeAudioClip([video_clip.audio, audio_clip])
    else:
        final_audio = audio_clip
    # add the final audio to the video
    final_clip = video_clip.set_audio(final_audio)
    # save the final clip
    final_clip.write_videofile(output_dir, codec='libx264')


