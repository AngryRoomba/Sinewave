from model import Model

class Controller:

    def __init__(self):
        self.model = Model("")


    def convert(self, file):
        #print('converting')
        self.model.file = file
        self.model.format_conversion()
        self.model.audio_to_mono()
        return

    def math(self):
        self.model.math()
