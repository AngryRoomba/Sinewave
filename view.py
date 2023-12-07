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

        self.time = Label(root, text='Time display', bg='white', fg='black')

        self.dataDisplay = Label(root, text="Place holder for echo data", bg='white', fg='black')

        self.fig = Figure(figsize= (4,4), dpi=80)
        self.dBfig = Figure(figsize= (4,4), dpi=80)
        self.graph = FigureCanvasTkAgg(self.fig, master=root)
        self.dBgraph = FigureCanvasTkAgg(self.dBfig, master=root)
        root.mainloop()


    def open_file(self):
        filepath = filedialog.askopenfilename(title='choose an audio file')
        if ('.wav' in filepath) or ('.mp3' in filepath):
            self.request['text']= filepath
            self.checkButton.pack(side='top', pady=(5,0))
            self.dataDisplay.pack_forget()
            self.graph.get_tk_widget().pack_forget()
            self.dBgraph.get_tk_widget().pack_forget()
        else:
            self.request['text']= "ERROR: File must be .wav or .mp3!"
            self.checkButton.pack_forget()
            self.dataDisplay.pack_forget()
            self.graph.get_tk_widget().pack_forget()
            self.dBgraph.get_tk_widget().pack_forget()
            return
        self.controller.convert(self.request['text'])


    def plotData(self):
        t, DbData, iMax, i5, i25 = self.controller.math()
        samplerate, data = wavfile.read(self.request['text'])
        length = data.shape[0] / samplerate
        time = np.linspace(0., length, data.shape[0])
        dBplotter = self.dBfig.add_subplot(111)
        dBplotter.plot(t, DbData, linewidth=1, alpha=0.7, color='#004bc6')
        dBplotter.plot(t[iMax], DbData[iMax], 'go')
        dBplotter.plot(t[i5], DbData[i5], 'yo')
        dBplotter.plot(t[i25], DbData[i25], 'ro')
        plotter = self.fig.add_subplot(111)
        plotter.plot(time, data[:])
        self.graph.draw()
        self.graph.get_tk_widget().pack(side='left', pady=(5,0))
        #self.dataDisplay.pack(side='right')
        self.dBgraph.draw()
        self.dBgraph.get_tk_widget().pack(side='right', pady=(5,0))

    def getCurretFile(self):
        if self.request['text'] == "ERROR: File must be .wav or .mp3!" or self.request['text'] == 'choose an audio file':
            return 0
        else:
            return self.request['text']

view = View()