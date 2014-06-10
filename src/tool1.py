# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16
from datetime import datetime 

import matplotlib.pyplot as plt
import numpy as np
import wave
import sys

BUFFER_SIZE = 1024
SAMPLING_RATE = 44000   # about 22050 * 2
SAVE_LENGTH = 40



def record(filename="tmp.wav"):

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
		
		save_buffer.append( string_audio_data )
		save_data.append( audio_data )

		save_count = save_count - 1

	print 'save %s' % (filename)
	save_wave_file(filename, save_buffer)
	
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
		xf = np.fft.rfft(xs)/BUFFER_SIZE
	
		freqs = np.linspace(0, SAMPLING_RATE/2, BUFFER_SIZE/2+1)
		xfp = 20*np.log10(np.clip(np.abs(xf), 1e-20, 1e100))
		
		idx = np.argmax(xfp)
		pitches.append(idx)
		
		print freqs[idx]

		# if pitches.count(idx)>40:
			# break



