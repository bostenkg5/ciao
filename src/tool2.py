import os
import sys
from Tkinter import *
from PIL import Image, ImageTk
import random
global canvas
global im

def startGame(number):
	global canvas
	global im
	tkObj = Tk()
	canvas = Canvas(tkObj, width = 1200, height = 400)
	canvas.pack()
	background = ImageTk.PhotoImage(master = canvas,file="../resource/background.jpg")
	canvas.create_image(600,100,image=background)
	x0 = 10
	dx = 2
	noBall = True
	image = []
	im = []
	ball = []
	for i in range(number):
		image.append(Image.open("../resource/ball"+str(i)+".png"))
		image[i] = image[i].resize((100,100),Image.BICUBIC)
		im.append(ImageTk.PhotoImage(image[i],master = canvas))
	
	 # while True:
		# if noBall == True :
			# index = random.randint(0,number-1)
			# print index
			# x0 = 10
			# ball.append(createBall(index,number))
			# noBall = False
		# if x0 >= 500:
			# #canvas.delete(which)
			# noBall = True
		# else :
			# x0 += dx
			# goBalls(ball)
	tkObj.mainloop()

def createBall(index,number):
	global im
	global canvas
	x0 = 10
	y0 = (400/number)*index+50
	ball = canvas.create_image(x0,y0,image=im[index])
	return ball
def goBalls(ball):
	global canvas
	dx = 2
	for i in ball :
		canvas.move(i, dx, 0)
	canvas.after(10)
	canvas.update()

if __name__ == "__main__":
	startGame(4)