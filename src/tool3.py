# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16
import wave
from tool2 import *
import threading

CHUNK = 1024

def play():
	
	wavName = 'test.wav'
	print "play %s" % (wavName)
	wf = wave.open(wavName, 'rb')

	pa = PyAudio()

	stream = pa.open(format=pa.get_format_from_width(wf.getsampwidth()),
					channels=wf.getnchannels(),
					rate=wf.getframerate(),
					output=True)

	data = wf.readframes(CHUNK)
	td = threading.Thread(target=startGame)
	td.start()
	while data != '':
		stream.write(data)
		data = wf.readframes(CHUNK)

	stream.stop_stream()
	stream.close()

	pa.terminate()