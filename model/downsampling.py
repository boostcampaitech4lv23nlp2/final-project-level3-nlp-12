import librosa
import soundfile as sf

import argparse

def down_sample(input_file, output_file, origin_sr, resample_sr):
    y, sr = librosa.load(input_file, sr=origin_sr)
    resampled = librosa.resample(y, orig_sr=sr, target_sr=resample_sr)
    print(y.shape, sr, '===>' ,resampled.shape)
    sf.write(output_file, resampled, resample_sr, format='WAV', endian='LITTLE', subtype='PCM_16')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file")
    parser.add_argument("-o", "--output_file")
    parser.add_argument("-or", "--origin_sr", type=int, default=22050)
    parser.add_argument("-re", "--resample_sr", type=int, default=8000)
    args = parser.parse_args()
    down_sample(args.input_file, args.output_file, args.origin_sr, args.resample_sr)
