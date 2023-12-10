# Imports
from model import Model

# Class definition
class Controller:
    # When crated create a blank model
    def __init__(self):
        self.model = Model("")

    # Converts the file to .wav and mono audio by calling related functions
    def convert(self, file):
        self.model.file = file
        self.model.format_conversion()
        self.model.audio_to_mono()
        return

    # Returns all calculations associated with the audio file
    def math(self, targetFreq):
        return self.model.math(targetFreq)
