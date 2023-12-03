from os import path
from pydub import AudioSegment

src = "Recording.mp3"
dst = "Recording.wav"

sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")