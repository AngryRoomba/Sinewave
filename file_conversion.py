import os
from pydub import AudioSegment

file_extension = os.path.splitext("recording.mp3")[1]
if file_extension.lower() == ".mp3":
    sound = AudioSegment.from_file("recording.mp3")
    sound.export("recording.wav", format="wav")