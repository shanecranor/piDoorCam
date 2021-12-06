import adcUtil as adc
from time import sleep
from time import time
import numpy as np
import soundfile as sf
#runs always
while True:
    #reads the "Loudness"
    envelope = adc.readADC(device = 0, channel=0)
    
    #if its lout enough, start recoding
    if (envelope > .08):
        #debug
        print("recording")
        
        start = time()
        finsih = start + 5
        audio = np.empty(1)
        
        # reads in the audio files for 5 seconds
        while time() < finish:
            audio = np.append(audio, adc.readADC(channel=0,device=0) )
                
        
        # debug
        #print(len(audio))
        
        #stores audio to a wav file
        filename = str(start) + "_audio.wav" 
        sf.write(filename, audio, 2700)
        
        # Debug
        # print("recording stop")