from pyaudio import PyAudio, paInt16
import numpy as np
import wave

BUFFER_SIZE = 1024
SAMPLING_RATE = 44032   # about 22050 * 2
SAVE_LENGTH = 43

class Wav:
	def __init__(self, fileName):
		self.fileName = fileName
		self.stringAudioData = None
		self.audioData = None
		self.feature = None

	def record(self):
		pa = PyAudio()
		in_stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True, frames_per_buffer=BUFFER_SIZE)
		save_count = 0
		save_buffer = []
		save_data   = None

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
		
	def play(self):
		print "play %s" % (self.fileName)
		pa = PyAudio()
		stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, output=True, frames_per_buffer=BUFFER_SIZE)
		
		stream.write(self.stringAudioData)

		stream.stop_stream()
		stream.close()
		pa.terminate()
		
