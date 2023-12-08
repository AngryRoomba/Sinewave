import os
import ffmpeg
from pydub import AudioSegment


class Model:

    def __init__(self, file):
        self.file = file
        self.raw_audio = None
        self.raw_audio_mono = None

    def format_conversion(self):
        sound = AudioSegment.from_file(self.file)
        sound.export("recording.wav", format="wav")
        self.file = 'recording.wav'
        self.raw_audio = AudioSegment.from_file(self.file, format="wav")

    def audio_to_mono(self):
        if self.raw_audio.channels != 1:
            self.raw_audio = self.raw_audio.set_channels(1)
            self.raw_audio.export("recording.wav", format="wav")
        self.raw_audio_mono = AudioSegment.from_file("recording.wav", format="wav")


audio = Model("bruh.wav")
print(ffmpeg.probe("bruh.wav"))
audio.format_conversion()
