from pydub import AudioSegment

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



