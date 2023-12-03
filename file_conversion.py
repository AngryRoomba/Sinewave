import os.path
from os import path
from pydub import AudioSegment

file_extension = os.path.splitext("Recording.mp3")[1]
if file_extension.lower() == ".mp3":
    sound = AudioSegment.from_mp3("Recording.mp3")
    sound.export("Recording.wav", format="wav")