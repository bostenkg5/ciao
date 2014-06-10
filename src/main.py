import os
import sys
import threading
import time
import random
from Tkinter import *
from tool1 import *
from tool3 import *
from Wav import *


global dbNum
DBpath = '../beatData'
wav = []
db = []

def init():
	global wav
	w = Wav('1.wav')
	wav.append(w)
	w = Wav('2.wav')
	wav.append(w)
	w = Wav('3.wav')
	wav.append(w)

def playMusic(n):
	global db
	print 'play database %d' % (n)
	wav = db[n]
	print "play %s" % (wav.fileName)
	wf = wave.open(wav.fileName, 'rb')
	pa = PyAudio()
	stream = pa.open(format=pa.get_format_from_width(wf.getsampwidth()),
					channels=wf.getnchannels(),
					rate=wf.getframerate(),
					output=True)
	
	sampleSum = 0
	beat = wav.beat
	data = wf.readframes(BUFFER_SIZE)
	sampleSum = sampleSum + BUFFER_SIZE
	while data != '':
		if len(beat)>0 and sampleSum>=beat[0]:
			print '%d !!!!' % (sampleSum)
			createBall(random.randrange(0,4))
			beat = beat[1:]
		stream.write(data)
		data = wf.readframes(BUFFER_SIZE)
		sampleSum = sampleSum + BUFFER_SIZE

	stream.stop_stream()
	stream.close()
	pa.terminate()
	print 'end database %d' % (n)

	
def startPlay():
	global dbNum
	index = int(dbNum.get())
	print 'index:', index
	td = threading.Thread(target=startGame, args=[4]);
	td.start()
	# td = threading.Thread(target=startGame, args=[4]);
	# td.start()
	# td = threading.Thread(target=playMusic, args=[0]);
	# td.start()
	playMusic(index)
	
	
def matchDB():
	global db
	print 'database path:', DBpath
	fp = open(DBpath+'/list.txt', 'r')
	for line in fp:
		fm = DBpath + '/' + line[:-1] + '.wav'
		tm = DBpath + '/' + line[:-1] + '.txt'
		print 'processing', fm
		wav = Wav(fm)
		wav.load()
		# wav.play()
		wav.loadTxt(tm)
		db = db + [wav]
		print db
	
	

def main():
	print 'main start'
	
	init()
	tkObj = Tk()
	
	# record button1
	recordButton1 = Button(tkObj)
	recordButton1["text"] = 'record1'
	recordButton1.grid(columnspan=10, sticky="nwse")
	recordButton1["command"] = lambda: wav[0].record()
	
	# record button2
	recordButton2 = Button(tkObj)
	recordButton2["text"] = 'record2'
	recordButton2.grid(columnspan=10, sticky="nwse")
	recordButton2["command"] = lambda: wav[1].record()
	
	# record button3
	recordButton3 = Button(tkObj)
	recordButton3["text"] = 'record3'
	recordButton3.grid(columnspan=10, sticky="nwse")
	recordButton3["command"] = lambda: wav[2].record()
	
	# play button1
	playButton1 = Button(tkObj)
	playButton1["text"] = 'play1'
	playButton1.grid(columnspan=10, sticky="nwse")
	playButton1["command"] = lambda: wav[0].play()
	
	# play button2
	playButton2 = Button(tkObj)
	playButton2["text"] = 'play2'
	playButton2.grid(columnspan=10, sticky="nwse")
	playButton2["command"] = lambda: wav[1].play()
	
	# tmp button
	tmpButton = Button(tkObj)
	tmpButton["text"] = 'tmp'
	tmpButton.grid(columnspan=10, sticky="nwse")
	tmpButton["command"] = lambda: decide()
	
	# match button
	matchButton = Button(tkObj)
	matchButton["text"] = 'match database'
	matchButton.grid(columnspan=10, sticky="nwse")
	matchButton["command"] = lambda: matchDB()
	
	# start game button
	startButton = Button(tkObj)
	startButton["text"] = 'start game'
	startButton.grid(columnspan=10, sticky="nwse")
	startButton["command"] = lambda: startPlay()
	
	global dbNum
	dbNum = Entry(tkObj, bd=10)
	dbNum.grid(columnspan=10, sticky="nwse")
	
	tkObj.mainloop()
	
if __name__ == "__main__":
	main()