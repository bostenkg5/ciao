import os
import sys
from Tkinter import *
from PIL import Image, ImageTk
import random

def startGame(number):

	tkObj = Tk()
	canvas = Canvas(tkObj, width = 1200, height = 400)
	canvas.pack()
	background = ImageTk.PhotoImage(master = canvas,file="background.jpg")
	canvas.create_image(600,100,image=background)
	x0 = 10
	y0 = []
	dx = 2
	noBall = True
	image = []
	im = []
	for i in range(number):
		image.append(Image.open("ball"+str(i)+".png"))
		image[i] = image[i].resize((100,100),Image.BICUBIC)
		im.append(ImageTk.PhotoImage(image[i],master = canvas))
		y0.append ((400/number)*i+50 )
	
	while True:
		if noBall == True :
			index = random.randint(0,number-1)
			print index
			x0 = 10
			which = canvas.create_image(x0,y0[index],image=im[index],tag='ball1')
			noBall = False
		if x0 >= 1000:
			canvas.delete(which)
			noBall = True
		else :
			x0 += dx
			canvas.move('ball1', dx, 0)
			canvas.after(10)
			canvas.update()

	tkObj.mainloop()
if __name__ == "__main__":
	startGame(4)