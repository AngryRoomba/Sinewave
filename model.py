import os
import pydub.utils
from pydub import AudioSegment
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

class Model:

    def __init__(self, file):
        self.file = file
        self.raw_audio = None
        self.raw_audio_mono = None
        self.samplerate = None
        self.data = None
        self.spectrum, self.freqs, self.t, self.im = None, None, None, None

    def format_conversion(self):
        file_extension = os.path.splitext(self.file)[1]
        if file_extension.lower() == ".mp3":
            sound = AudioSegment.from_file(self.file)
            sound.export("recording.wav", format="wav")
        self.raw_audio = AudioSegment.from_file("recording.wav", format="wav")

    def audio_to_mono(self):
        if self.raw_audio.channels != 1:
            self.raw_audio = self.raw_audio.set_channels(1)
            self.raw_audio.export("recording.wav", format="wav")
        self.raw_audio_mono = AudioSegment.from_file("recording.wav", format="wav")

    def math(self):
        self.samplerate, self.data = wavfile.read(self.file)
        self.spectrum, self.freqs, self.t, self.im = plt.specgram(self.data, Fs=self.samplerate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))

        dataInDb = self.frequencyCheck()
        plt.figure()
        plt.plot(self.t, dataInDb, linewidth = 1, alpha=0.7, color='#004bc6')
        plt.xlabel('Time (s)')
        plt.ylabel('Power (dB)')

        indexOfMax = np.argmax(dataInDb)
        valueOfMax = dataInDb[indexOfMax]

        plt.plot(self.t[indexOfMax], dataInDb[indexOfMax], 'go')

        slicedArray = dataInDb[indexOfMax:]

        maxLess5 = valueOfMax - 5

        maxLess5 = self.findNearestValue(slicedArray, maxLess5)

        indexLess5 = np.where(dataInDb == maxLess5)

        plt.plot(self.t[indexLess5], dataInDb[indexLess5], 'yo')

        maxless25 = valueOfMax - 25
        maxless25 = self.findNearestValue(slicedArray, maxless25)
        indexLess25 = np.where(dataInDb == maxless25)

        plt.plot(self.t[indexLess25], dataInDb[indexLess25], 'ro')
        rt20 = (self.t[indexLess5] - self.t[indexLess25])[0]
        rt60 = rt20 *3
        plt.grid()
        plt.show()
        print(rt60)

    def findTargetFrequency(self, freqs):
        for x in freqs:
            if x > 1000:
                break
        return x

    def frequencyCheck(self):
        global targetFrequency
        targetFrequency = self.findTargetFrequency(self.freqs)
        indexOfFrequency = np.where(self.freqs == targetFrequency)[0][0]
        dataForFrequency = self.spectrum[indexOfFrequency]
        dataInDBFun = 10* np.log10(dataForFrequency)
        return dataInDBFun

    def findNearestValue(self,array,value):
        array = np.asarray(array)
        idx = (np.abs(array-value)).argmin()
        return array[idx]
