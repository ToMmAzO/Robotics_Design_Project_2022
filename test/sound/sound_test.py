# import pyaudio
# import pygame

# print("-------------------------------------1")
# p = pyaudio.PyAudio()

# print("-------------------------------------2")
# stream = p.open(format=pyaudio.paInt16, channels=1,
#                 rate=16000, input=True, frames_per_buffer=8000)

# print("-------------------------------------3")
# stream.start_stream()

# print("-------------------------------------4")
# pygame.mixer.init()

# print("-------------------------------------5")
# pygame.mixer.music.load('song.mp3')

# print("-------------------------------------6")
# pygame.mixer.music.play()

from playsound import playsound

playsound('song.wav')