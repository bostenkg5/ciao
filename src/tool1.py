# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16
from datetime import datetime 

import numpy as np
import wave
import sys
from Wav import *
from scipy.spatial import distance
from MFCC import extract


BUFFER_SIZE = 1024
SAMPLING_RATE = 44032   # about 22050 * 2
SAVE_LENGTH = 40



def record():

	pa = PyAudio()
	in_stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True, frames_per_buffer=BUFFER_SIZE)
	out_stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE,output=True)
	save_count = 0
	save_buffer = []
	save_data   = []

	save_count = SAVE_LENGTH
	
	print 'start recording'

	while save_count>0:
		string_audio_data = in_stream.read(BUFFER_SIZE)
		audio_data = np.fromstring(string_audio_data, dtype=np.short)
		
		print type(audio_data)
		save_buffer.append( string_audio_data )
		save_data.append( audio_data )

		save_count = save_count - 1

#print 'save %s' % (wav.fileName)
#save_wave_file(wav.fileName, save_buffer)
		save_wave_file("test.wav", save_buffer)
		pa.terminate()



def save_wave_file(filename, data):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLING_RATE)
    wf.writeframes("".join(data))
    wf.close()
					   
					   
def pitch_tracking():
	pitches = [];
	pa = PyAudio()
	in_stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True, frames_per_buffer=BUFFER_SIZE)
	out_stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE,output=True)
		
	while True:
		
		string_data = in_stream.read(BUFFER_SIZE)
		audio_data  = np.fromstring(string_data, dtype=np.short)
		
		xs = audio_data[:BUFFER_SIZE]
		print xs
		xf = np.fft.rfft(xs)/BUFFER_SIZE
	
		freqs = np.linspace(0, SAMPLING_RATE/2, BUFFER_SIZE/2+1)
		xfp = 20*np.log10(np.clip(np.abs(xf), 1e-20, 1e100))
		
		idx = np.argmax(xfp)
		pitches.append(idx)
		
		print freqs[idx]

		# if pitches.count(idx)>40:
			# break

def get_pitch(audio_data):
	freq = np.fft.rfft(audio_data)
	idx  = np.argmax(freq)
	
	#freqs = np.linspace(0, SAMPLING_RATE/2, BUFFER_SIZE/2+1)
	#	print freqs[idx]
	
	return idx


def decide():
	wav1=Wav('1.wav')
	wav1.load()
	
	wav2=Wav('2.wav')
	wav2.load()
	
	wav3=Wav('3.wav')
	wav3.load()
	
	dist13 = calc_MFCC_dist(wav1.feature, wav3.feature)
	#dist13 +=calc_pitch_dist(s1,s3)

	dist23 = calc_MFCC_dist(wav2.feature, wav3.feature)
	#dist23 +=calc_pitch_dist(s2, s3)
	
	print "dist13",dist13
	#print "pitch13",calc_pitch_dist(s1, s3)
	
	print "dist23",dist23
	#print "pitch23",calc_pitch_dist(s2, s3)

	if dist13 < dist23:
		print 1
		return 1
	else:
		print 2
		return 2

def calc_MFCC_dist(m1,m2):

	return distance.euclidean(m1.flatten(), m2.flatten())
#	return distance.cosine(f1.flatten(), f2.flatten())

def calc_pitch_dist(m1,m2):
	p1 = get_pitch(m1)
	p2 = get_pitch(m2)

	return np.abs(p1 - p2)
