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
        root.geometry('980x760+300+20')

        self.controller = Controller()

        self.request = Label(root, text='Please choose an audio file', bg='white', fg='black')
        self.request.pack(side="top", pady=(5, 0))
        self.reqButton = Button(root, text='Select Audio File', command=self.open_file)
        self.reqButton.pack(side='top', pady=(5, 0))

        self.checkButton = Button(root, text='Plot the given data', command=self.plotData)
        self.waveButton = Button(root, text='Show the Waveform', command=self.plotData)
        self.spectButton = Button(root, text='Show the Spectrogram', command=self.plotData)

        self.time = Label(root, text='Time display', bg='white', fg='black')

        self.dataDisplay = Label(root, text="Place holder for echo data", bg='white', fg='black')

        self.frametop = Frame(root)
        self.framebottom = Frame(root)

        self.fig = Figure(figsize=(4, 4), dpi=80)
        self.dBfig = Figure(figsize=(4, 4), dpi=80)
        self.specfig = Figure(figsize=(4, 4), dpi=80)
        self.lowfig = Figure(figsize=(4, 4), dpi=80)
        self.highfig = Figure(figsize=(4, 4), dpi=80)
        self.graph = FigureCanvasTkAgg(self.fig, master=self.frametop)
        self.dBgraph = FigureCanvasTkAgg(self.dBfig, master=self.framebottom)
        self.specGraph = FigureCanvasTkAgg(self.specfig, master=self.frametop)
        self.lowGraph = FigureCanvasTkAgg(self.lowfig, master=self.framebottom)
        self.highGraph = FigureCanvasTkAgg(self.highfig, master=self.framebottom)

        root.mainloop()

    def open_file(self):
        filepath = filedialog.askopenfilename(title='Select Audio File')
        ext = os.path.splitext(filepath)[-1].lower()
        if (ext == ".wav") or (ext == ".mp3"):
            self.request['text'] = filepath
            self.checkButton.pack(side='top', pady=(5, 0))
            self.waveButton.pack(side='top', pady=(5, 0))
            self.spectButton.pack(side='top', pady=(5, 0))
            self.dataDisplay.pack_forget()
            self.graph.get_tk_widget().pack_forget()
            self.dBgraph.get_tk_widget().pack_forget()
        else:
            self.request['text'] = "ERROR: File must be .wav or .mp3!"
            self.checkButton.pack_forget()
            self.dataDisplay.pack_forget()
            self.graph.get_tk_widget().pack_forget()
            self.dBgraph.get_tk_widget().pack_forget()
            return
        self.controller.convert(self.request['text'])

    def plotData(self):
        t, DbData, iMax, i5, i25, file = self.controller.math(1000)
        tLow, dBDataLow, iMaxLow, i5Low, i25Low, file = self.controller.math(250)
        tHigh, dBDataHigh, iMaxHigh, i5High, i25High, file = self.controller.math(5000)
        samplerate, data = wavfile.read(file)
        length = data.shape[0] / samplerate
        time = np.linspace(0., length, data.shape[0])

        dBplotter = self.dBfig.add_subplot(111)
        dBplotter.plot(t, DbData, linewidth=1, alpha=0.7, color='#004bc6')
        self.dBfig.supxlabel("Time (s)")
        self.dBfig.supylabel("Power (dB)")
        self.dBfig.suptitle("Medium Frequency RT60")
        self.fig.suptitle("Waveform")
        dBplotter.plot(t[iMax], DbData[iMax], 'go')
        dBplotter.plot(t[i5], DbData[i5], 'yo')
        dBplotter.plot(t[i25], DbData[i25], 'ro')

        Lowplotter = self.lowfig.add_subplot(111)
        Lowplotter.plot(tLow, dBDataLow, linewidth=1, alpha=0.7, color='#004bc6')
        self.lowfig.supxlabel("Time (s)")
        self.lowfig.supylabel("Power (dB)")
        self.lowfig.suptitle("Low Frequency RT60")
        Lowplotter.plot(t[iMaxLow], dBDataLow[iMaxLow], 'go')
        Lowplotter.plot(t[i5Low], dBDataLow[i5Low], 'yo')
        Lowplotter.plot(t[i25Low], dBDataLow[i25Low], 'ro')

        Highplotter = self.highfig.add_subplot(111)
        Highplotter.plot(tHigh, dBDataHigh, linewidth=1, alpha=0.7, color='#004bc6')
        self.highfig.supxlabel("Time (s)")
        self.highfig.supylabel("Power (dB)")
        self.highfig.suptitle("High Frequency RT60")
        Highplotter.plot(t[iMaxHigh], dBDataHigh[iMaxHigh], 'go')
        Highplotter.plot(t[i5High], dBDataHigh[i5High], 'yo')
        Highplotter.plot(t[i25High], dBDataHigh[i25High], 'ro')

        self.fig.supxlabel('Time (s)')
        self.fig.supylabel('Frequency (Hz)')
        plotter = self.fig.add_subplot(111)
        plotter.plot(time, data[:])

        self.specfig.suptitle("Spectrogram")
        specPlotter = self.specfig.add_subplot(111)
        spec, fr, ti, im = specPlotter.specgram(data, Fs=samplerate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        cbar = self.specfig.colorbar(im)
        cbar.set_label('Intensity (dB)')

        self.frametop.pack(side='top')
        self.framebottom.pack(side='bottom')
        self.specGraph.draw()
        self.specGraph.get_tk_widget().pack(side='left', pady=(5, 0), anchor='nw', expand=True)
        self.graph.draw()
        self.graph.get_tk_widget().pack(side='left', padx=(5, 0), pady=(5, 0), anchor='nw', expand=True)
        # self.dataDisplay.pack(side='right')
        self.dBgraph.draw()
        self.dBgraph.get_tk_widget().pack(side='left', padx=(3, 3), pady=(5, 0), anchor='nw', expand=True)
        self.lowGraph.draw()
        self.lowGraph.get_tk_widget().pack(side='left', anchor='sw', expand=True)
        self.highGraph.draw()
        self.highGraph.get_tk_widget().pack(side='bottom', anchor='sw', expand=True)

    def getCurretFile(self):
        if self.request['text'] == "ERROR: File must be .wav or .mp3!" or self.request[
            'text'] == 'choose an audio file':
            return 0
        else:
            return self.request['text']


view = View()
