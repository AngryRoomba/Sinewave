import os
import pydub.utils
from pydub import AudioSegment


class AudioFile:
    def __init__(self, file):
        self.file = file
        self.raw_audio = None
        self.raw_audio_mono = None

    def format_conversion(self):
        file_extension = os.path.splitext(self.file)[1]
        if file_extension.lower() == ".mp3":
            sound = AudioSegment.from_file(self.file)
            sound.export("recording.wav", format="wav")
            self.raw_audio = AudioSegment.from_file("recording.wav", format="wav")
        else:
            self.raw_audio = AudioSegment.from_file(self.file, format="wav")

    def audio_to_mono(self):
        if self.raw_audio.channels != 1:
            self.raw_audio = self.raw_audio.set_channels(1)
            self.raw_audio.export("recording_mono.wav", format="wav")
        else:
            self.raw_audio.export("recording_mono.wav", format="wav")
        self.raw_audio_mono = AudioSegment.from_file("recording_mono.wav", format="wav")


