import os
import sys
from Tkinter import *
from tool1 import *
from tool3 import *

def main():
	print 'main start'
	
	tkObj = Tk()
	
	# record button
	recordButton = Button(tkObj)
	recordButton["text"] = 'record'
	recordButton.grid(columnspan=10, sticky="nwse")
	recordButton["command"] = lambda: record("tmp.wav")
	
	# play button
	playButton = Button(tkObj)
	playButton["text"] = 'play'
	playButton.grid(columnspan=10, sticky="nwse")
	playButton["command"] = lambda: play("tmp.wav")
	
	tkObj.mainloop()
	
if __name__ == "__main__":
	main()