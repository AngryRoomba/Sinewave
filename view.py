from tkinter import *
from tkinter import filedialog
import os
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from pydub import AudioSegment
import scipy.io
from scipy.io import wavfile
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from controller import Controller

class View:
    def __init__(self):
        root = Tk()
        root.title("Audiowave display")
        root.configure(background="grey")
        root.minsize(400, 400)
        root.geometry('860x640+360+80')

        self.controller = Controller()

        self.request = Label(root, text='Please choose an audio file', bg='white', fg='black')
        self.request.pack(side="top", pady=(5,0))
        self.reqButton = Button(root, text='choose an audio file',command=self.open_file)
        self.reqButton.pack(side='top', pady=(5,0))

        self.checkButton = Button(root, text='Plot the given data', command=self.plotData)

        self.dataDisplay = Label(root, text="Place holder for echo data", bg='white', fg='black')

        self.fig = Figure(figsize= (5,5), dpi=100)
        self.graph = FigureCanvasTkAgg(self.fig, master=root)
        root.mainloop()


    def open_file(self):
        filepath = filedialog.askopenfilename(title='choose an audio file')
        if ('.wav' in filepath) or ('.mp3' in filepath):
            self.request['text']= filepath
            self.checkButton.pack(side='top', pady=(5,0))
            self.dataDisplay.pack_forget()
            self.graph.get_tk_widget().pack_forget()
        else:
            self.request['text']= "ERROR: File must be .wav or .mp3!"
            self.checkButton.pack_forget()
            self.dataDisplay.pack_forget()
            self.graph.get_tk_widget().pack_forget()
            return
        self.controller.convert(filepath)




    def plotData(self):
        samplerate, data = wavfile.read(self.request['text'])
        length = data.shape[0] / samplerate
        time = np.linspace(0., length, data.shape[0])
        plotter = self.fig.add_subplot(111)
        plotter.plot(time, data[:])
        self.graph.draw()
        self.graph.get_tk_widget().pack(side='left', pady=(5,0))
        self.dataDisplay.pack(side='right')

    def getCurretFile(self):
        if self.request['text'] == "ERROR: File must be .wav or .mp3!" or self.request['text'] == 'choose an audio file':
            return 0
        else:
            return self.request['text']