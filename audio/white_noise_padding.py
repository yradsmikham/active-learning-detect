from pydub import AudioSegment
import wave
import sys
import os
import math
import numpy as np

def wav_length(fname):
    wav = wave.open(fname,'r')
    frames = wav.getnframes()
    rate = wav.getframerate()
    duration = frames / float(rate)
    return(duration)

def combinations(lst, target, with_replacement=False):
    def _a(idx, l, r, t, w):
        if t == sum(l): r.append(l)
        elif t < sum(l): return
        for u in range(idx, len(lst)):
            _a(u if w else (u + 1), l + [lst[u]], r, t, w)
        return r
    return _a(0, [], [], target, with_replacement)

def sliding_window(fname, duration):
    # padding
    print("padding")

    # padding reverse
    print("reverse padding")

def white_noise_generator(wav, white_noise_duration):
    for x in white_noise_duration:
        if x == 0:
            wn_duration = max(white_noise_duration)
            # white noise duration should be a list e.g [0,1]
            # generate white noise wav file
            wn = AudioSegment.silent(duration=wn_duration * 1000) 
            wn.export(wav+"_whitenoise.wav",format="wav", parameters=["-ar", "16000"])

            # stitch white noise wav file to specific audio wav file
            #before
            padded_fname = wav.split('.')[-2]
            new_wav = AudioSegment.from_wav(wav+"_whitenoise.wav") + AudioSegment.from_wav(wav)
            new_wav.export(padded_fname+"_padded.wav", format="wav", parameters=["-ar", "16000"])

            #after
            padded_fname = wav.split('.')[-2]
            new_wav = AudioSegment.from_wav(wav) + AudioSegment.from_wav(wav+"_whitenoise.wav")
            new_wav.export(padded_fname+"_padded2.wav", format="wav", parameters=["-ar", "16000"])

            # remove white noise wav file
            os.remove(wav+"_whitenoise.wav")
            break
        else:
            # white noise duration should be a list e.g [0,1]
            # generate white noise wav file
            wn_0 = AudioSegment.silent(duration=white_noise_duration[0] * 1000) 
            wn_0.export(wav+"_whitenoise_0.wav",format="wav", parameters=["-ar", "16000"])

            wn_1 = AudioSegment.silent(duration=white_noise_duration[1] * 1000) 
            wn_1.export(wav+"_whitenoise_1.wav",format="wav", parameters=["-ar", "16000"])

            # stitch white noise wav file to specific audio wav file
            padded_fname = wav.split('.')[-2]
            new_wav = AudioSegment.from_wav(wav+"_whitenoise_1.wav") + AudioSegment.from_wav(wav) + AudioSegment.from_wav(wav+"_whitenoise_1.wav")
            new_wav.export(padded_fname+"_padded.wav", format="wav", parameters=["-ar", "16000"])

            # remove white noise wav file
            os.remove(wav+"_whitenoise_0.wav")
            os.remove(wav+"_whitenoise_1.wav")

            return(padded_fname+"_padded.wav")
    return(padded_fname+"_padded.wav")

# take in wav file and calculate duration, n
fname = sys.argv[1]
n = wav_length(fname)
print("Length of wav file: " + str(n) + " seconds")
float(n)

# round the wav up to the nearest integer
integ = math.ceil(n)
wn_remain = integ - n
print("White Noise Remainder: " + str(wn_remain) + " seconds")
float(wn_remain)

# pad audio file
rounded_wav = white_noise_generator(sys.argv[1], [0,wn_remain])
print(rounded_wav)
rounded_wav_length = wav_length(rounded_wav)
print("Length of rounded wav file: " + str(rounded_wav_length) + " seconds")
float(rounded_wav_length)

# determine all combinations of a + b = remainder
remainder = 10 - round(rounded_wav_length)
print("Remainder value: " + str(remainder))
int(remainder)
lst = list(range(0, 10))
comb = combinations(lst, remainder)
comb_new = []
for i in comb:
    if len(i) == 2:
        comb_new.append(i)
print(comb_new)

for combination in comb_new:
    # 10 second padding
    print("hey!")
    #sliding_window(rounded_wav, combination)

# generate wav file that covers duration, 10-n
# n_milli = n * 1000 # convert n to milliseconds 
# duration_whitenoise = 10000 - n_milli
# wn = AudioSegment.silent(duration=duration_whitenoise) 
# wn.export(fname+"_whitenoise.wav",format="wav", parameters=["-ar", "16000"])
# wn_length = wav_length(fname+"_whitenoise.wav")
# print("Length of white noise wav file: " + str(wn_length) + " seconds")
# float(wn_length)

# # join the wav files
# padded_fname = fname.split('.')[-2]
# new_wav = AudioSegment.from_wav(sys.argv[1]) + AudioSegment.from_wav(fname+"_whitenoise.wav")
# new_wav.export(padded_fname+"_padded.wav", format="wav", parameters=["-ar", "16000"])

# # remove white noise wav file
# fname+"_whitenoise.wav"
# os.remove(fname+"_whitenoise.wav")