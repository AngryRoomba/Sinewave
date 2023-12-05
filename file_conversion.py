import os
import pydub.utils
from pydub import AudioSegment


file_extension = os.path.splitext("recording.mp3")[1]
if file_extension.lower() == ".mp3":
    sound = AudioSegment.from_file("recording.mp3")
    sound.export("recording.wav", format="wav")
raw_audio = AudioSegment.from_file("recording.wav", format="wav")
if raw_audio.channels != 1:
    raw_audio = raw_audio.set_channels(1)
    raw_audio.export("recording_mono.wav", format="wav")
else:
    raw_audio.export("recording_mono.wav", format="wav")
raw_audio_mono = AudioSegment.from_file("recording_mono.wav", format="wav")
