import whisper

def split_wav(data, sample_rate, start, end):   
    start *= sample_rate
    end *= sample_rate
    return data[start:end]

def split_run(input_file,time_list):
    audio = whisper.load_audio(input_file)  # 원본 wav 파일
    edited_audio = []
    
    for start,end,text in time_list :
        # start초 end초 까지의 데이터 추출  : array([0., 0., 0., ..., 0., 0., 0.], dtype=float32) 형태
        edited_audio.append(split_wav(audio, 16000, int(start), int(end)))
    return edited_audio