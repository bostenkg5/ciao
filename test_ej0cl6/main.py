import os
import sys
from Tkinter import *

def tt():
	print 'tt'


def main():
	print 'main start'
	
	tkObj = Tk()
	
	button = Button(tkObj)
	button["text"] = 'kkkkk'
	button.grid(columnspan=10, sticky="nwse")
	button["command"] = tt
	
	tkObj.mainloop()
	
if __name__ == "__main__":
	main()