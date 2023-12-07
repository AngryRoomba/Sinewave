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
        self.spectrum, self.freqs, self.t, self.im = None

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
        self.sample_rate, self.data = wavfile.read(self.raw_audio_mono)
        self.spectrum, self.freqs, self.t, self.im = plt.specgram(self.data, Fs=self.sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))

        dataInDb = self.frequencyCheck()

    def findTargetFrequency(self,freqs):
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
