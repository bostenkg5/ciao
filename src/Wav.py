from pyaudio import PyAudio, paInt16
import numpy as np
import wave

BUFFER_SIZE = 1024
SAMPLING_RATE = 44000   # about 22050 * 2
SAVE_LENGTH = 40

class Wav:
	def __init__(self, fileName):
		self.fileName = fileName
		self.x = None
		self.feature = None

	def record(self):
		pa = PyAudio()
		in_stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True, frames_per_buffer=BUFFER_SIZE)
		save_count = 0
		save_buffer = []
		save_data   = []

		save_count = SAVE_LENGTH
		
		print 'start recording'
		while save_count>0:
			string_audio_data = in_stream.read(BUFFER_SIZE)
			audio_data = np.fromstring(string_audio_data, dtype=np.short)
			
			save_buffer.append( string_audio_data )
			save_data.append( audio_data )

			save_count = save_count - 1

		print 'save %s' % (self.fileName)
		pa.terminate()
		
		wf = wave.open(self.fileName, 'wb')
		wf.setnchannels(1)
		wf.setsampwidth(2)
		wf.setframerate(SAMPLING_RATE)
		wf.writeframes("".join(save_buffer))
		wf.close()
		
	def play(self):
		print "play %s" % (self.fileName)
		wf = wave.open(self.fileName, 'rb')
		pa = PyAudio()
		stream = pa.open(format=pa.get_format_from_width(wf.getsampwidth()),
						channels=wf.getnchannels(),
						rate=wf.getframerate(),
						output=True)

		# td = threading.Thread(target=startGame)
		# td.start()
		
		data = wf.readframes(BUFFER_SIZE)
		while data != '':
			stream.write(data)
			data = wf.readframes(BUFFER_SIZE)

		stream.stop_stream()
		stream.close()
		wf.close()
		pa.terminate()
		
	# def getFeature(self):