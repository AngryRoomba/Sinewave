from tkinter import *
from tkinter import filedialog
import os
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from pydub import AudioSegment
import scipy.io
from scipy.io import wavfile
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

root = Tk()
root.title("Audiowave display")
root.configure(background="grey")
root.minsize(400, 400)
root.geometry('860x640+360+80')

request = Label(root, text='Please choose an audio file', bg='white', fg='black')
request.pack(side="top", pady=(5,0))


def open_file():
    filepath = filedialog.askopenfilename(title='choose an audio file')
    if ('.wav' in filepath) or ('.mp3' in filepath):
        request['text']= filepath
        checkButton.pack(side='top', pady=(5,0))
    else:
        request['text']= "ERROR: File must be .wav or .mp3!"
        checkButton.pack_forget()
        return
    filename = os.path.basename(filepath)
    request['text'] = filepath
    if '.mp3' in filename:
        request['text'] = 'finding...'
        sound = AudioSegment.from_file(filepath)
        request['text'] = 'converting...'
        sound.export('file.wav', format='wav')
        request['text'] = 'converted!'



def plotData():
    samplerate, data = wavfile.read(request['text'])
    length = data.shape[0] / samplerate
    time = np.linspace(0., length, data.shape[0])
    fig = Figure(figsize= (5,5), dpi=100)
    plotter = fig.add_subplot(111)
    plotter.plot(time, data[:])
    graph = FigureCanvasTkAgg(fig, master=root)
    graph.draw()
    graph.get_tk_widget().pack(side='left', pady=(5,0))


reqButton = Button(root, text='choose an audio file',command=open_file)
reqButton.pack(side='top', pady=(5,0))

checkButton = Button(root, text='Plot the given data', command=plotData)

root.mainloop()