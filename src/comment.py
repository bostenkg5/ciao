class comment:
	def __init__(self,which) :
		self.which = which
		self.timer = 0
	def timerAdd(self) :
		self.timer+=1
	def isTimeOut(self) :
		if self.timer == 20 :
			return True
		else :
			return False
	def getImg(self):
		return self.which