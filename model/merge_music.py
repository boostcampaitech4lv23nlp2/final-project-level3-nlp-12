from pydub import AudioSegment

# specify the audio files to be merged
file1 = "/opt/ml/final/ex1.mp3"
file2 = "/opt/ml/final/make_example1.mp3"

# load the audio files
audio1 = AudioSegment.from_file(file1)
audio2 = AudioSegment.from_file(file2)

# merge the audio files
#merged_audio = audio1.overlay(audio2)

if audio1.duration_seconds == audio2.duration_seconds:
    merged_audio = audio1.overlay(audio2)
    merged_audio.export("/opt/ml/final/merged_sample_file.mp3", format="mp3")
else:
    print("Both files must have the same duration")
    print("Result file will have the same duration with audio2")
    merged_audio = audio1[:audio2.duration_seconds*1000].overlay(audio2)
    merged_audio.export("/opt/ml/final/merged_sample_file.mp3", format="mp3")



