import os
import sys
from Tkinter import *
from PIL import Image, ImageTk
import random
from comment import *
from ball import *
global canvas
global balls
global openBall
global index
global exiting
global comments
global isComment
global commentIndex
global commentNum

def startGame(number):
	global canvas
	global im
	global balls
	global openBall
	global exiting
	global comments
	global isComment
	global commentIndex
	global commentNum
	tkObj = Tk()
	canvas = Canvas(tkObj, width = 1200, height = 400)
	canvas.pack()
	background = ImageTk.PhotoImage(master = canvas,file="../resource/background.jpg")
	canvas.create_image(600,100,image=background)
	x0 = 10
	dx = 2
	image = []
	im = []
	balls = []
	openBall = False
	exiting = False
	isComment = False
	comments = []
	count = 0
	for i in range(number):
		image.append(Image.open("../resource/ball"+str(i)+".png"))
		image[i] = image[i].resize((100,100),Image.BICUBIC)
		im.append(ImageTk.PhotoImage(image[i],master = canvas))
	for i in range(3) :
		image.append(Image.open("../resource/comment"+str(i)+".png"))
		im.append(ImageTk.PhotoImage(image[i+number],master = canvas))
	while True:
		if openBall == True :
			x0 = 10
			y0 = (400/number)*index+50
			balls.append(ball(canvas.create_image(x0,y0,image=im[index])))
			openBall = False
		if isComment == True :
			isComment = False
			y0 = (400/number)*commentIndex+50
			comments.append(comment(canvas.create_image(1000,y0,image=im[number+commentNum])))
		if exiting == True :
			count+=1
		if count == 300 :
			tkObj.destroy()
		goBalls()
		checkComment()
		checkBall()
	tkObj.mainloop()

# Create balls
def createBall(_index):
	global openBall
	global index
	openBall = True
	index = _index

# Run all balls on the window
def goBalls():
	global canvas
	global balls
	dx = 10
	for i in balls :
		canvas.move(i.getImg(), dx, 0)
	canvas.after(50)
	canvas.update()
	
# Check all comment is timeout or not
def checkComment():
	global comments
	global canvas
	for i in comments :
		i.timerAdd()
		if i.isTimeOut() :
			canvas.delete(i.getImg())
			comments.remove(i)
			
# Check all ball is timeout or not
def checkBall():
	global comments
	global canvas
	for i in balls :
		i.timerAdd()
		if i.isTimeOut() :
			canvas.delete(i.getImg())
			balls.remove(i)
			
# Exit the Game
def exitGame():
	global exiting
	exiting = True
	
# Deliver comments
def judgeComment(_comment,_index):
	global isComment
	global commentIndex
	global commentNum
	isComment = True
	commentIndex = _index
	commentNum = _comment
if __name__ == "__main__":
	startGame(4)