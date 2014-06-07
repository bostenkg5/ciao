import os
import sys
from Tkinter import *

def tt():
	print 'tt'


def main():
	print 'main start'
	
	tkObj = Tk()
	
	# record button
	recordButton = Button(tkObj)
	recordButton["text"] = 'record'
	recordButton.grid(columnspan=10, sticky="nwse")
	recordButton["command"] = tt
	
	tkObj.mainloop()
	
if __name__ == "__main__":
	main()