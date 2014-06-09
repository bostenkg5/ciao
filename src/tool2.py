import os
import sys
from Tkinter import *
from PIL import Image, ImageTk

def startGame():
	print 'main start'
	
	tkObj = Tk()

	canvas = Canvas(tkObj, width = 800, height = 400)
	canvas.pack()
	background = ImageTk.PhotoImage(file="background.jpg")
	canvas.create_image(400,100,image=background)
	x0 = 10		# initial left-most edge of ball
	y0 = 180		# initial top-most edge of ball
	x1 = 60		# inital right-most edge of ball
	y1 = 230	# you've probably got the idea by now.
	dx = 2
	noBall = True
	# create ball:
	while True:
		if noBall == True :
			#which = canvas.create_oval(x0,y0,x1,y1,fill="blue", tag='blueBall')
			image = Image.open("ball.png")
			image = image.resize((200,200),Image.BICUBIC)
			im=ImageTk.PhotoImage(image)
			which = canvas.create_image(x0,y0,image=im,tag='blueBall')
			noBall = False
		if x0 >= 600:
			canvas.delete(which)
			noBall = True
			x0 = 10		# initial left-most edge of ball
			y0 = 180		# initial top-most edge of ball
			x1 = 60		# inital right-most edge of ball
			y1 = 230	# you've probably got the idea by now.
		else :
			x0 += dx
			x1 += dx
			canvas.move('blueBall', dx, 0)
			canvas.after(10)
			canvas.update()
		
	tkObj.mainloop()
if __name__ == "__main__":
	startGame()