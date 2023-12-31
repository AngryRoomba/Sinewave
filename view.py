# Imports
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

# Class definition
class View:
    # Creates all elements of the GUI
    def __init__(self):
        # Creates the popup GUI
        root = Tk()
        root.title("Audiowave display")
        root.configure(background="grey")
        root.minsize(400, 400)
        root.geometry('980x760+300+20')

        # Initialises the controller to allow model-view communication
        self.controller = Controller()
        
        # Creates the frame in which all elements will be arranged
        self.framebutton = Frame(root, bg='grey')

        # Creates the upload button and prompt and attaches them to the frame
        self.request = Label(root, text='Please choose an audio file', bg='white', fg='black')
        self.request.pack(side="top", pady=(5, 0))
        self.reqButton = Button(root, text='Select Audio File', command=self.open_file)
        self.reqButton.pack(side='top', pady=(5, 0))

        # Creates the various graph buttons and puts them in the frame
        self.checkButton = Button(master=self.framebutton, text='Plot RT60s', command=self.plotRT60s)
        self.waveButton = Button(master=self.framebutton, text='Show the Waveform', command=self.plotWaveform)
        self.spectButton = Button(master=self.framebutton, text='Show the Spectrogram', command=self.plotSpectrogram)
        self.totalButton = Button(root, text='Display all RT60s at once', command=self.plotAllRT60s)

        # Creates the text box for additional information and binds it to the frame
        self.dataDisplay = Label(root, text="Place holder for echo data", bg='white', fg='black')

        # Initialises a counter for the cycling RT60 graph button and the button itself
        self.RT60counter = 0
        self.cycleButton = Button(root, text='Show next RT60 graph', command=self.cycleRT60)

        # Creates frames to contain graphs
        self.frametop = Frame(root)
        self.framebottom = Frame(root)

        # Initialises figures for each graph and binds the appropriate graph to them.
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.dBfig = Figure(figsize=(5, 5), dpi=100)
        self.specfig = Figure(figsize=(5, 5), dpi=100)
        self.lowfig = Figure(figsize=(5, 5), dpi=100)
        self.highfig = Figure(figsize=(5, 5), dpi=100)
        self.totalfig = Figure(figsize=(5, 5), dpi=100)
        self.graph = FigureCanvasTkAgg(self.fig, master=self.frametop)
        self.dBgraph = FigureCanvasTkAgg(self.dBfig, master=self.framebottom)
        self.specGraph = FigureCanvasTkAgg(self.specfig, master=self.frametop)
        self.lowGraph = FigureCanvasTkAgg(self.lowfig, master=self.framebottom)
        self.highGraph = FigureCanvasTkAgg(self.highfig, master=self.framebottom)
        self.totalgraph = FigureCanvasTkAgg(self.totalfig, master=root)

        # Makes the window start working
        root.mainloop()

    def open_file(self):
        # Creates the upload popup using the default file management application
        filepath = filedialog.askopenfilename(title='Select Audio File')
        
        # Gets the file extention by cutting the file path
        ext = os.path.splitext(filepath)[-1].lower()

        # Checks if the file is .wav or .mp3
        if (ext == ".wav") or (ext == ".mp3"):
            # If it is make the graph buttons visible and removes all curently visible graphs
            self.request['text'] = filepath
            self.framebutton.pack(side='top', pady=(5,0))
            self.checkButton.pack(side='left')
            self.waveButton.pack(side='left', padx=(8, 0))
            self.spectButton.pack(side='left', padx=(8, 0))
            self.totalButton.pack(pady=(5,0))
            self.RT60counter = 0
            self.dataDisplay.pack_forget()
            self.unpackGraphs()
            self.frametop.pack_forget()
            self.framebottom.pack_forget()
        
        # If the File is not .wav or .mp3 throw an error and reset all graphs
        else:
            self.request['text'] = "ERROR: File must be .wav or .mp3!"
            self.checkButton.pack_forget()
            self.dataDisplay.pack_forget()
            self.unpackGraphs()
            self.waveButton.pack_forget()
            self.spectButton.pack_forget()
            self.framebutton.pack_forget()
            self.totalButton.pack_forget()
            return

        # Converts .mp3 files to .wav files
        self.controller.convert(self.request['text'])
        
        # Creates but does not show all the graphs
        self.plotData()

    def plotData(self):
        # Gets all of the values from the math function
        t, DbData, iMax, i5, i25, file, rt60, highest = self.controller.math(1000)
        tLow, dBDataLow, iMaxLow, i5Low, i25Low, file, rt60Low, highestL = self.controller.math(250)
        tHigh, dBDataHigh, iMaxHigh, i5High, i25High, file, rt60High, highestH = self.controller.math(5000)
        
        # Gets the samplerate and data from the audio file
        samplerate, data = wavfile.read(file)
        
        # Determines the width of the graph
        length = data.shape[0] / samplerate
        
        # Determines what time the graph spans
        time = np.linspace(0., length, data.shape[0])

        # Plots the medium RT60 graph
        dBplotter = self.dBfig.add_subplot(111)
        dBplotter.plot(t, DbData, linewidth=1, alpha=0.7, color='#004bc6')
        self.dBfig.supxlabel("Time (s)")
        self.dBfig.supylabel("Power (dB)")
        self.dBfig.suptitle("Medium Frequency RT60")
        dBplotter.plot(t[iMax], DbData[iMax], 'go')
        dBplotter.plot(t[i5], DbData[i5], 'yo')
        dBplotter.plot(t[i25], DbData[i25], 'ro')

        # Plots the low RT60 graph
        Lowplotter = self.lowfig.add_subplot(111)
        Lowplotter.plot(tLow, dBDataLow, linewidth=1, alpha=0.7, color='#004bc6')
        self.lowfig.supxlabel("Time (s)")
        self.lowfig.supylabel("Power (dB)")
        self.lowfig.suptitle("Low Frequency RT60")
        Lowplotter.plot(t[iMaxLow], dBDataLow[iMaxLow], 'go')
        Lowplotter.plot(t[i5Low], dBDataLow[i5Low], 'yo')
        Lowplotter.plot(t[i25Low], dBDataLow[i25Low], 'ro')

        # Plots the high RT60 graph
        Highplotter = self.highfig.add_subplot(111)
        Highplotter.plot(tHigh, dBDataHigh, linewidth=1, alpha=0.7, color='#004bc6')
        self.highfig.supxlabel("Time (s)")
        self.highfig.supylabel("Power (dB)")
        self.highfig.suptitle("High Frequency RT60")
        Highplotter.plot(t[iMaxHigh], dBDataHigh[iMaxHigh], 'go')
        Highplotter.plot(t[i5High], dBDataHigh[i5High], 'yo')
        Highplotter.plot(t[i25High], dBDataHigh[i25High], 'ro')

        # Plots the spectrogram
        self.specfig.suptitle("Spectrogram")
        specPlotter = self.specfig.add_subplot(111)
        spec, fr, ti, im = specPlotter.specgram(data, Fs=samplerate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        cbar = self.specfig.colorbar(im)
        cbar.set_label('Intensity (dB)')

        # Plots the waveform
        self.fig.suptitle("Waveform")
        self.fig.supxlabel('Time (s)')
        self.fig.supylabel('Frequency (Hz)')
        plotter = self.fig.add_subplot(111)
        plotter.plot(time, data[:])

        # Plots the combined RT60 graph
        self.totalfig.suptitle("All RT60s")
        self.totalfig.supylabel("Power (dB)")
        self.totalfig.supxlabel("Time (s)")
        totalplotter = self.totalfig.add_subplot(111)
        line1 = totalplotter.plot(tHigh, dBDataHigh, linewidth=1, alpha=0.7, color='#00f6ff',label='High')
        totalplotter.plot(t[iMaxHigh], dBDataHigh[iMaxHigh], 'go', label="_")
        totalplotter.plot(t[i5High], dBDataHigh[i5High], 'yo', label="_")
        totalplotter.plot(t[i25High], dBDataHigh[i25High], 'ro', label="_")
        line2 =totalplotter.plot(t, dBDataLow, linewidth=1, alpha=0.7, color='#5b1a5d', label='Low')
        totalplotter.plot(t[iMaxLow], dBDataLow[iMaxLow], 'go', label="_")
        totalplotter.plot(t[i5Low], dBDataLow[i5Low], 'yo', label="_")
        totalplotter.plot(t[i25Low], dBDataLow[i25Low], 'ro', label="_")
        line3 =totalplotter.plot(t, DbData, linewidth=1, alpha=0.7, color='#004bc6', label = 'Medium')
        totalplotter.plot(t[iMax], DbData[iMax], 'go', label="_")
        totalplotter.plot(t[i5], DbData[i5], 'yo', label="_")
        totalplotter.plot(t[i25], DbData[i25], 'ro', label="_")
        self.totalfig.legend()

        # Creates the additional information text using data gathered by the math dunction
        self.dataDisplay['text']= 'The file is ' + str(round(self.controller.model.time, 3)) + ' seconds long, the frequency of highest amplitude is '+ str(highest) + 'Hz and the average RT60s are:\n LOW: '+ str(round(rt60Low-0.5, 3)) + ' MEDIUM: ' + str(round(rt60-.5, 3)) + ' HIGH: '+ str(round(rt60High-0.5, 3))
        self.dataDisplay.pack(side='bottom')

    
    def plotSpectrogram(self):
        # Deletes any previous graph
        self.unpackGraphs()

        # Plots the spectrogram
        self.frametop.pack(pady=(20,0))
        self.specGraph.draw()
        self.specGraph.get_tk_widget().pack(side='left', pady=(5, 0), anchor='nw', expand=True)

    def plotWaveform(self):
        # Deletes any previous graph
        self.unpackGraphs()

        # Plots the waveform
        self.frametop.pack(pady=(20,0))
        self.graph.draw()
        self.graph.get_tk_widget().pack(side='left', padx=(5, 0), pady=(5, 0), anchor='nw', expand=True)

    def plotRT60s(self):
        # Deletes any previous graph
        self.unpackGraphs()

        # Ensures the cycle button is visible
        self.cycleButton.pack(pady=(20, 0))
        self.framebottom.pack(pady=(20,0))

        # Checks which graph to display by checking the value of the counter
        if self.RT60counter == 0:
            self.lowGraph.draw()
            self.lowGraph.get_tk_widget().pack(side='left', anchor='sw', expand=True)
        elif self.RT60counter == 1:
            self.dBgraph.draw()
            self.dBgraph.get_tk_widget().pack(side='left', padx=(3, 3), pady=(5, 0), anchor='nw', expand=True)
        else:
            self.highGraph.draw()
            self.highGraph.get_tk_widget().pack(side='bottom', anchor='sw', expand=True)

    def cycleRT60(self):
        # Increments the counter
        self.RT60counter += 1

        # Ensures the counter cannot exceed 2
        if self.RT60counter > 2:
            self.RT60counter = 0
        
        # Plots the graph
        self.plotRT60s()

    def plotAllRT60s(self):
        # Deletes any previous graph
        self.unpackGraphs()

        # Plots the combined RT60 graph
        self.totalgraph.draw()
        self.totalgraph.get_tk_widget().pack(pady=(20,0))


    def unpackGraphs(self):
        # Hides all graphs
        self.graph.get_tk_widget().pack_forget()
        self.dBgraph.get_tk_widget().pack_forget()
        self.specGraph.get_tk_widget().pack_forget()
        self.lowGraph.get_tk_widget().pack_forget()
        self.highGraph.get_tk_widget().pack_forget()
        self.frametop.pack_forget()
        self.framebottom.pack_forget()
        self.totalgraph.get_tk_widget().pack_forget()
        self.cycleButton.pack_forget()
        self.totalgraph.get_tk_widget().pack_forget()


    def getCurretFile(self):
        # Returns the location of the selected file
        if self.request['text'] == "ERROR: File must be .wav or .mp3!" or self.request[
            'text'] == 'choose an audio file':
            return 0
        else:
            return self.request['text']

# Runs the program
view = View()
