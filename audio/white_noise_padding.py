from pydub import AudioSegment
import wave
import sys
import os

def wav_length(fname):
    wav = wave.open(fname,'r')
    frames = wav.getnframes()
    rate = wav.getframerate()
    duration = frames / float(rate)
    return(duration)

# take in wav file and calculate duration, n
fname = sys.argv[1]
n = wav_length(fname)
#print("Length of wav file: " + str(n) + "seconds")
#float(n)

# generate wav file that covers duration, 10-n
n_milli = n * 1000 # convert n to milliseconds 
duration_whitenoise = 10000 - n_milli
wn = AudioSegment.silent(duration=duration_whitenoise) 
wn.export(fname+"_whitenoise.wav",format="wav", parameters=["-ar", "16000"])
wn_length = wav_length(fname+"_whitenoise.wav")
#print("Length of white noise wav file: " + str(wn_length) + "seconds")
#float(wn_length)

# join the wav files
padded_fname = fname.split('.')[-2]
new_wav = AudioSegment.from_wav(sys.argv[1]) + AudioSegment.from_wav(fname+"_whitenoise.wav")
new_wav.export(padded_fname+"_padded.wav", format="wav", parameters=["-ar", "16000"])

# remove white noise wav file
fname+"_whitenoise.wav"
os.remove(fname+"_whitenoise.wav")