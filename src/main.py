import os
import sys
import threading
import time
import random
from Tkinter import *
from tool1 import *
from tool3 import *
from Wav import *
from MFCC import extract
from scipy.spatial import distance

DBpath = '../beatData'
wav = []
db = []
dbName = []

global score

def init():
	global wav
	w = Wav('1.wav')
	wav.append(w)
	w = Wav('2.wav')
	wav.append(w)
	w = Wav('3.wav')
	wav.append(w)
	
	global dbName
	fp = open(DBpath+'/list.txt', 'r')
	dbName = [line[:-1] for line in fp]
	fp.close()

def howGood(audio_data, ans, pos, sampleSum):
	f1 = extract( np.asarray(audio_data))
	f1 = f1.flatten()
	f2 = extract( np.asarray(ans))
	f2 = f2.flatten()
	d = distance.cosine(f1, f2)
	print pos, d, sampleSum
	
	if d<0.925:
		a = 2
	elif d<1:
		a = 1
	else:
		a = 0
	judgeComment(a,pos)
	
	global score
	score = score + a
	print score
	
# def howGood(audio_data, ans, pos):
	# d = calc_pitch_dist(audio_data, pos)
	# print d
	# judgeComment(0,pos)

def playMusic(n):
	global db
	print 'play database %d' % (n)
	wav = db[n]
	print "play %s" % (wav.fileName)
	wf = wave.open(wav.fileName, 'rb')
	pa = PyAudio()
	i_stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True, frames_per_buffer=BUFFER_SIZE)
	o_stream = pa.open(format=pa.get_format_from_width(wf.getsampwidth()),
					channels=wf.getnchannels(),
					rate=wf.getframerate(),
					output=True)
	
	
	save_buffer = []
	sampleSum = 0
	beat = wav.beat
	beatAudio = wav.beatAudio
	ans = wav.ans
	ans2 = wav.ans
	data = wf.readframes(BUFFER_SIZE)
	sampleSum = sampleSum + BUFFER_SIZE
	while data != '':
		if len(beat)>1 and sampleSum>=beat[0] - 5.0*44032 and sampleSum<=beat[1] - 5.0*44032:
			createBall(ans[0])
			beat = beat[1:]
			ans = ans[1:]
		elif len(beat)>0 and sampleSum>=beat[0] - 5.0*44032:
			# print '%d !!!!' % (sampleSum)
			createBall(ans[0])
			beat = beat[1:]
			ans = ans[1:]

		string_audio_data = i_stream.read(BUFFER_SIZE)	
		if len(beatAudio)>0 and sampleSum>=beatAudio[0][1]:
			# print 's'
			wf2 = wave.open('tmp/%d.wav' % (sampleSum), 'wb')
			wf2.setnchannels(1)
			wf2.setsampwidth(2)
			wf2.setframerate(SAMPLING_RATE)
			wf2.writeframes("".join(save_buffer))
			wf2.close()
			
			audio_data = np.fromstring("".join(save_buffer), dtype=np.short)
			audio_data = audio_data[:9216*2]

			td = threading.Thread(target=howGood, args=[audio_data, wav.audioData[beatAudio[0][0]:beatAudio[0][1]], ans2[0], sampleSum]);
			td.start()

			save_buffer = []
			beatAudio = beatAudio[1:]
			ans2 = ans2[1:]
		elif len(beatAudio)>0 and sampleSum>=beatAudio[0][0]:
			# print 'w'
			save_buffer.append( string_audio_data )
		
		o_stream.write(data)
		data = wf.readframes(BUFFER_SIZE)
		
		sampleSum = sampleSum + BUFFER_SIZE
		
	
	o_stream.stop_stream()
	o_stream.close()
	pa.terminate()
	print 'end database %d' % (n)
	
def startPlay():
	global score
	score = 0
	global listbox
	re = listbox.curselection()
	index = int(re[0])
	print 'index:', index
	td = threading.Thread(target=startGame, args=[4]);
	td.start()
	# td = threading.Thread(target=startGame, args=[4]);
	# td.start()
	# td = threading.Thread(target=playMusic, args=[0]);
	# td.start()
	playMusic(index)
	exitGame()
	
def matchDB():
	global db
	global wav
	print 'database path:', DBpath
	fp = open(DBpath+'/list.txt', 'r')
	for line in fp:
		fm = DBpath + '/' + line[:-1] + '.wav'
		tm = DBpath + '/' + line[:-1] + '.txt'
		print 'processing', fm
		wavd = Wav(fm)
		wavd.loaddb()
		wavd.loadTxt(tm)
		wavd.match(wav)
		db = db + [wavd]
	fp.close()

def loadRecord():
	global wav
	for w in wav:
		w.load()

def main():
	print 'main start'
	global wav
	init()
	tkObj = Tk()
	
	
	# record button0
	recordButton0 = Button(tkObj)
	recordButton0["text"] = 'load record'
	recordButton0.grid(columnspan=10, sticky="nwse")
	recordButton0["command"] = lambda: loadRecord()
	
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
	
	# play button3
	playButton3 = Button(tkObj)
	playButton3["text"] = 'play3'
	playButton3.grid(columnspan=10, sticky="nwse")
	playButton3["command"] = lambda: wav[2].play()
	
	# tmp button
	tmpButton = Button(tkObj)
	tmpButton["text"] = 'recognize'
	tmpButton.grid(columnspan=10, sticky="nwse")
	tmpButton["command"] = lambda: decide(wav)
	
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
	
	global listbox
	listbox = Listbox(tkObj)
	listbox.grid(columnspan=10, sticky="nwse")
	
	global dbName
	for d in dbName:
		listbox.insert(END, d)
		
	# end button
	endButton = Button(tkObj)
	endButton["text"] = 'end'
	endButton.grid(columnspan=10, sticky="nwse")
	endButton["command"] = lambda: tkObj.destroy()
	
	tkObj.mainloop()
	
if __name__ == "__main__":
	main()