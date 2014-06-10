import os
import sys
import threading
from Tkinter import *
from tool1 import *
from tool3 import *
from Wav import *

DBpath = '../beatData'
wav1 = None
wav2 = None
db = []


def init():
	global wav1
	global wav2
	wav1 = Wav('1.wav')
	wav2 = Wav('2.wav')

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
			beat = beat[1:]
		stream.write(data)
		data = wf.readframes(BUFFER_SIZE)
		sampleSum = sampleSum + BUFFER_SIZE

	stream.stop_stream()
	stream.close()
	pa.terminate()
	print 'end database %d' % (n)
	
def startPlay():
	global wav1
	td = threading.Thread(target=playMusic, args=[0]);
	td.start()
	# playMusic(0)
	
	
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
	recordButton = Button(tkObj)
	recordButton["text"] = 'record1'
	recordButton.grid(columnspan=10, sticky="nwse")
	# recordButton["command"] = lambda: record(wav1)
	recordButton["command"] = lambda: wav1.record()
	
	# record button2
	recordButton = Button(tkObj)
	recordButton["text"] = 'record2'
	recordButton.grid(columnspan=10, sticky="nwse")
	recordButton["command"] = lambda: wav2.record()
	
	# play button1
	playButton = Button(tkObj)
	playButton["text"] = 'play1'
	playButton.grid(columnspan=10, sticky="nwse")
	playButton["command"] = lambda: wav1.play()
	
	# play button2
	playButton = Button(tkObj)
	playButton["text"] = 'play2'
	playButton.grid(columnspan=10, sticky="nwse")
	playButton["command"] = lambda: wav2.play()
	
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
	
	
	tkObj.mainloop()
	
if __name__ == "__main__":
	main()