import os
import sys
from Tkinter import *
import tool1

def tt():
	print 'tt'


def main():
	print 'main start'
	
	tkObj = Tk()
	
	# record button
	recordButton = Button(tkObj)
	recordButton["text"] = 'record'
	recordButton.grid(columnspan=10, sticky="nwse")
	recordButton["command"] = record
	
	tkObj.mainloop()
	
if __name__ == "__main__":
	main()