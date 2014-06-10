import os
import sys
from Tkinter import *
from PIL import Image, ImageTk
import random
global canvas
global ball
global openBall
global index
global exiting

def startGame(number):
	global canvas
	global im
	global ball
	global openBall
	global exiting
	tkObj = Tk()
	canvas = Canvas(tkObj, width = 1200, height = 400)
	canvas.pack()
	background = ImageTk.PhotoImage(master = canvas,file="../resource/background.jpg")
	canvas.create_image(600,100,image=background)
	x0 = 10
	dx = 2
	image = []
	im = []
	ball = []
	openBall = False
	exiting =False
	count = 0
	for i in range(number):
		image.append(Image.open("../resource/ball"+str(i)+".png"))
		image[i] = image[i].resize((100,100),Image.BICUBIC)
		im.append(ImageTk.PhotoImage(image[i],master = canvas))
	while True:
		if openBall == True :
			x0 = 10
			y0 = (400/number)*index+50
			ball.append(canvas.create_image(x0,y0,image=im[index]))
			openBall = False
		if exiting == True :
			count+=1
		if count == 300 :
			tkObj.destroy()
		goBalls()
	tkObj.mainloop()

def createBall(_index):
	global openBall
	global index
	openBall = True
	index = _index

def goBalls():
	global canvas
	global ball
	dx = 2
	for i in ball :
		canvas.move(i, dx, 0)
	canvas.after(10)
	canvas.update()
def exitGame():
	global exiting
	exiting = True

if __name__ == "__main__":
	startGame(4)