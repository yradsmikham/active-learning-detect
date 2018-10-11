from pydub import AudioSegment
import wave
import sys
import os
import math
import numpy as np
import shutil

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
            wav_files = []
            padded_fname = wav.split('.')[-2]
            wn_duration = max(white_noise_duration)

            # white noise duration should be a list e.g [0,1]
            # generate white noise wav file
            wn = AudioSegment.silent(duration=wn_duration * 1000) 
            wn.export(wav+"_whitenoise.wav",format="wav", parameters=["-ar", "16000"])

            # stitch white noise wav file to specific audio wav file
            # before
            new_wav_before = AudioSegment.from_wav(wav+"_whitenoise.wav") + AudioSegment.from_wav(wav)
            new_wav_before.export(padded_fname+"_padded"+"_"+str(white_noise_duration[1])+"_"+str(white_noise_duration[0])+".wav", format="wav", parameters=["-ar", "16000"])

            # after
            new_wav_after = AudioSegment.from_wav(wav) + AudioSegment.from_wav(wav+"_whitenoise.wav")
            new_wav_after.export(padded_fname+"_padded"+"_"+str(white_noise_duration[0])+"_"+str(white_noise_duration[1])+".wav", format="wav", parameters=["-ar", "16000"])

            # remove white noise wav file
            os.remove(wav+"_whitenoise.wav")
            wav_files.append(padded_fname+"_padded"+"_"+str(white_noise_duration[1])+"_"+str(white_noise_duration[0])+".wav")
            wav_files.append(padded_fname+"_padded"+"_"+str(white_noise_duration[0])+"_"+str(white_noise_duration[1])+".wav")
            break
        else:
            wav_files = []
            padded_fname = wav.split('.')[-2]

            # white noise duration should be a list e.g [0,1]
            # generate white noise wav file
            wn_0 = AudioSegment.silent(duration=white_noise_duration[0] * 1000) 
            wn_0.export(wav+"_whitenoise_0.wav",format="wav", parameters=["-ar", "16000"])

            wn_1 = AudioSegment.silent(duration=white_noise_duration[1] * 1000) 
            wn_1.export(wav+"_whitenoise_1.wav",format="wav", parameters=["-ar", "16000"])

            # stitch white noise wav file to specific audio wav file
            new_wav = AudioSegment.from_wav(wav+"_whitenoise_0.wav") + AudioSegment.from_wav(wav) + AudioSegment.from_wav(wav+"_whitenoise_1.wav")
            new_wav.export(padded_fname+"_padded.wav"+"_"+str(white_noise_duration[0])+"_"+str(white_noise_duration[1])+".wav", format="wav", parameters=["-ar", "16000"])

            # after
            new_wav_reverse = AudioSegment.from_wav(wav+"_whitenoise_1.wav") + AudioSegment.from_wav(wav) + AudioSegment.from_wav(wav+"_whitenoise_0.wav")
            new_wav_reverse.export(padded_fname+"_padded"+"_"+str(white_noise_duration[1])+"_"+str(white_noise_duration[0])+".wav", format="wav", parameters=["-ar", "16000"])

            # remove white noise wav file
            os.remove(wav+"_whitenoise_0.wav")
            os.remove(wav+"_whitenoise_1.wav")
            
            wav_files.append(padded_fname+"_padded.wav"+"_"+str(white_noise_duration[0])+"_"+str(white_noise_duration[1])+".wav")
            wav_files.append(padded_fname+"_padded.wav"+"_"+str(white_noise_duration[1])+"_"+str(white_noise_duration[0])+".wav")
            break
    return wav_files

# make directory for output files
newpath = r'output' 
if not os.path.exists(newpath):
    os.makedirs(newpath)

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
rounded_wav = white_noise_generator(sys.argv[1], [0, wn_remain])
print(rounded_wav)
rounded_wav_length_0 = wav_length(rounded_wav[0])
print("Length of rounded wav file: " + str(rounded_wav_length_0) + " seconds")
float(rounded_wav_length_0)

rounded_wav_length_1 = wav_length(rounded_wav[1])
print("Length of rounded wav file: " + str(rounded_wav_length_1) + " seconds")
float(rounded_wav_length_1)


# determine all combinations of a + b = remainder
remainder = 10 - round(rounded_wav_length_1)
print("Remainder value: " + str(remainder))
int(remainder)
lst = list(range(0, 10))
comb = combinations(lst, remainder)
comb_new = []
for i in comb:
    if len(i) == 2:
        comb_new.append(i)
print(comb_new)

# rename padded wav file
# copy padded wav file in output folder as new file
folder_name = (rounded_wav[1].split("_")[0]).split("/")[-1]
path = "output/"+folder_name
if not os.path.exists(path): 
    os.mkdir(path)

shutil.copy(rounded_wav[1], path)
destination = path+"/"+ folder_name+".wav"
os.rename(path+"/"+rounded_wav[1].split("/")[-1], destination)

for combination in comb_new:
    # 10 second padding
    print("Creating padded wav files...")
    white_noise_generator(destination,combination)

# remove in wav folder
for file in rounded_wav:
    os.remove(file)