from model import Model

class Controller:

    def __init__(self):
        self.model = Model("")


    def convert(self, file):
        self.model.file = file
        self.model.format_conversion()
        self.model.audio_to_mono()
        return

