from pyaudio import PyAudio, paInt16
import matplotlib.pyplot as plt
import numpy as np
import wave
from MFCC import extract

BUFFER_SIZE = 1024
SAMPLING_RATE = 44032   # about 22050 * 2
SAVE_LENGTH = 43

class Wav:
	def __init__(self, fileName):
		self.fileName = fileName
		self.txtName = None
		self.stringAudioData = None
		self.audioData = None
		self.beat = None
		self.beatAudio = None
		self.vol = None
		self.cutAudio = None
		self.feature = None
		self.ans = None
		

	def record(self):
		pa = PyAudio()
		in_stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True, frames_per_buffer=BUFFER_SIZE)
		save_count = 0
		save_buffer = []

		save_count = SAVE_LENGTH
		
		print 'start recording'
		while save_count>0:
			string_audio_data = in_stream.read(BUFFER_SIZE)
			audio_data = np.fromstring(string_audio_data, dtype=np.short)
			save_buffer.append( string_audio_data )
			save_count = save_count - 1

		print 'save %s' % (self.fileName)
		pa.terminate()
		
		wf = wave.open(self.fileName, 'wb')
		wf.setnchannels(1)
		wf.setsampwidth(2)
		wf.setframerate(SAMPLING_RATE)
		wf.writeframes("".join(save_buffer))
		wf.close()
		
		self.stringAudioData = "".join(save_buffer)
		save_data = np.fromstring(self.stringAudioData, dtype=np.short)
		self.audioData = save_data
		self.cut2()
		self.getFeature()
		
	def play(self):
		print "play %s" % (self.fileName)
		pa = PyAudio()
		stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, output=True, frames_per_buffer=BUFFER_SIZE)
		
		#stream.write(self.stringAudioData)
		stream.write(self.cutAudio)
		
		stream.stop_stream()
		stream.close()
		pa.terminate()
	
	def load(self):
		pa = PyAudio()
		wf = wave.open(self.fileName, 'rb')
		save_buffer = []
		string_audio_data = wf.readframes(BUFFER_SIZE)
		while string_audio_data != '':
			audio_data = np.fromstring(string_audio_data, dtype=np.short)
			save_buffer.append( string_audio_data )
			string_audio_data = wf.readframes(BUFFER_SIZE)

		pa.terminate()
		self.stringAudioData = "".join(save_buffer)
		save_data = np.fromstring(self.stringAudioData, dtype=np.short)
		self.audioData = save_data
			
		self.cut2()
		self.getFeature()


		
	def loadTxt(self, fileName):
		fp = open(fileName, 'r')
		self.beat = [int(line) for line in fp]
		fp.close()
		self.beatAudio = [(max(0,b-5000),min(b+5000,len(self.audioData)-1)) for b in self.beat]

	def plot(self):
		audio = self.audioData
		plt.plot(audio)
		plt.show()
		
	def plot2(self,w):
		plt.plot(w)
		plt.show()
		
	def calVol(self):
		length = self.audioData.shape[0]
		self.vol = [None]*length

		for i in range(length):
			ia = max((i-512,0))
			ib = min((i+512,length-1))
			v = self.audioData[ia:ib]
			self.vol[i] = np.sum(np.abs(v))


	def cut2(self):
		rad = 5000
		self.calVol()
		maxv = max(self.vol)
		mid  = np.argmax(self.vol)
		length = self.audioData.shape[0]
		if mid<rad:
			mid = rad
		elif mid>length-rad:
			mid = length - rad
			
		
		self.cutAudio = self.audioData[mid-rad:mid+rad]
	
	
	def cut(self):
		self.load()
		self.calVol()
		maxv = max(self.vol)
		thv = 0.3*maxv
		
		length = self.audioData.shape[0]
		ia = None
		ib = None
		for i in range(length):
			if ia==None and self.vol[i]>thv:
				ia = i
			if ia!=None and ib==None and self.vol[i]<thv:
				ib = i
				break

		#print ia,ib
		self.cutAudio = self.audioData[ia:ib]
	
	def getFeature(self):
		cutAudio = self.cutAudio
		f = extract( np.asarray(cutAudio))
		f = f.flatten()
		self.feature = f
	
	def match(self, wav):
		for w in wav:
			print w

