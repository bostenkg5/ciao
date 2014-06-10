import os
import sys
from Tkinter import *
from tool1 import *
from tool3 import *
from Wav import *

wav1 = None
wav2 = None


def init():
	global wav1
	global wav2
	wav1 = Wav('1.wav')
	wav2 = Wav('2.wav')

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
	
	# play button
	playButton = Button(tkObj)
	playButton["text"] = 'play1'
	playButton.grid(columnspan=10, sticky="nwse")
	playButton["command"] = lambda: wav1.play()
	
	# play button
	playButton = Button(tkObj)
	playButton["text"] = 'play2'
	playButton.grid(columnspan=10, sticky="nwse")
	playButton["command"] = lambda: wav2.play()
	
	
	tkObj.mainloop()
	
if __name__ == "__main__":
	main()