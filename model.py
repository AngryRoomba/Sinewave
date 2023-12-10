# Imports
from pydub import AudioSegment
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

# Class definition
class Model:

    # On creation of an object set all properties to none by default
    def __init__(self, file):
        self.file = file
        self.raw_audio = None
        self.raw_audio_mono = None
        self.time = None
        self.samplerate = None
        self.data = None
        self.spectrum, self.freqs, self.t, self.im = None, None, None, None

    # Export the audio file as a .wav to force the file type and remove metadata
    def format_conversion(self):
        sound = AudioSegment.from_file(self.file)
        sound.export("recording.wav", format="wav")
        self.file = "recording.wav"
        self.raw_audio = AudioSegment.from_file(self.file, format="wav")

    # Check if the audio is not set to mono, if it isnt forcibly set it to be and re-export the file
    def audio_to_mono(self):
        if self.raw_audio.channels != 1:
            self.raw_audio = self.raw_audio.set_channels(1)
            self.raw_audio.export(self.file, format="wav")
        self.raw_audio_mono = AudioSegment.from_file(self.file, format="wav")
        self.time = self.raw_audio_mono.duration_seconds

    # Does all nessesary calculations
    def math(self, targetFreq):
        # Gets the sample rate and data by reading the audio file
        self.samplerate, self.data = wavfile.read(self.file)

        # Plots a sprectrogram of the audio then extracts the spectrum, frequencies, time, and the im
        self.spectrum, self.freqs, self.t, self.im = plt.specgram(self.data, Fs=self.samplerate, NFFT=1024,
                                                                  cmap=plt.get_cmap('autumn_r'))

        # Converts the data to decibles
        dataInDb = self.frequencyCheck(targetFreq)

        # Plots the realated graph using the time and decibles found earlier
        plt.figure()
        plt.plot(self.t, dataInDb, linewidth=1, alpha=0.7, color='#004bc6')
        plt.xlabel('Time (s)')
        plt.ylabel('Power (dB)')

        # Finds the maximum freqency from the extracted values
        indexOfMax = np.argmax(dataInDb)
        valueOfMax = dataInDb[indexOfMax]

        # Plots the maximum frequency as a special point
        plt.plot(self.t[indexOfMax], dataInDb[indexOfMax], 'go')

        # Gets the data the the maximum frequency
        slicedArray = dataInDb[indexOfMax:]

        # Finds the value of the frequency 5 decibles below the maximum
        maxLess5 = valueOfMax - 5

        # Finds the frequency closest to the above and replaces the above with it
        maxLess5 = self.findNearestValue(slicedArray, maxLess5)

        # Gets the index of the above frequency
        indexLess5 = np.where(dataInDb == maxLess5)

        # Plots the found frequency as a special point
        plt.plot(self.t[indexLess5], dataInDb[indexLess5], 'yo')

        # Repeats the same process as above only to find the value closest to 25 below the maximum
        maxless25 = valueOfMax - 25
        maxless25 = self.findNearestValue(slicedArray, maxless25)
        indexLess25 = np.where(dataInDb == maxless25)
        plt.plot(self.t[indexLess25], dataInDb[indexLess25], 'ro')
        
        # Calculates the RT60 by first calulating the RT20 and multiplying it by 3
        rt20 = (self.t[indexLess5] - self.t[indexLess25])[0]
        rt60 = rt20 * 3
        
        # Plots the RT60 graph
        plt.grid()

        # Returns all calculated values
        return self.t, dataInDb, indexOfMax, indexLess5, indexLess25, self.file, rt60, self.findHighestFreq(self.freqs)

    # Finds the desired frequency from an array using itteration then returns it
    def findTargetFrequency(self, freqs, targetFreq):

        for x in freqs:
            if x > targetFreq:
                break
        return x

    # Finds where in the audio the target frequency occurs and returns the data in decibles
    def frequencyCheck(self, targetFreq):
        global targetFrequency
        targetFrequency = self.findTargetFrequency(self.freqs, targetFreq)
        indexOfFrequency = np.where(self.freqs == targetFrequency)[0][0]
        dataForFrequency = self.spectrum[indexOfFrequency]
        dataInDBFun = 10 * np.log10(dataForFrequency)
        return dataInDBFun

    # Finds the index of a desired value by converting an array to a numpy array
    def findNearestValue(self, array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    # Finds the highest frequency using itteration
    def findHighestFreq(self, freqs):
        largest = 0
        for x in freqs:
            if x > largest:
                largest = x
        return x
