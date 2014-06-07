# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16 
from datetime import datetime 
from aubio import source, pitch, freqtomidi

import matplotlib.pyplot as plt
import numpy as np
import wave
import sys

def save_wave_file(filename, data): 
    wf = wave.open(filename, 'wb') 
    wf.setnchannels(1) 
    wf.setsampwidth(2) 
    wf.setframerate(SAMPLING_RATE) 
    wf.writeframes("".join(data)) 
    wf.close() 


'''

win_s = 4096
hop_s = 512

pa = PyAudio()
stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True,
				 frames_per_buffer=NUM_SAMPLES)
s =
'''


NUM_SAMPLES = 2000      # pyAudio內部緩存的塊的大小
SAMPLING_RATE = 44000   # about 22050 * 2
LEVEL = 1500            # 聲音保存的閾值
COUNT_NUM = 20          # NUM_SAMPLES個取樣之內出現COUNT_NUM個大於LEVEL的取樣則記錄聲音
SAVE_LENGTH = 22        # 聲音記錄的最小長度：SAVE_LENGTH * NUM_SAMPLES 個取樣

pa = PyAudio() 
in_stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True,
                frames_per_buffer=NUM_SAMPLES)

out_stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE,output=True)

save_count = 0 
save_buffer = [] 
save_data   = []

save_count = SAVE_LENGTH

print 'start recording'

while save_count>0:
	string_audio_data = in_stream.read(NUM_SAMPLES)
	audio_data = np.fromstring(string_audio_data, dtype=np.short) 

	save_buffer.append( string_audio_data )
	save_data.append( audio_data )

	out_stream.write(string_audio_data)


'''
	else: 
	    # 將save_buffer中的數據寫入WAV文件，WAV文件的文件名是保存的時刻
	    if len(save_buffer) > 0: 
			#pl.plot(time, 
	        filename = datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + ".wav" 
	        save_wave_file(filename, save_buffer) 
	        #save_buffer = [] 
	        print filename, "saved" 

'''