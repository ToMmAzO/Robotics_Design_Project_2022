from vosk import Model, KaldiRecognizer
import json
import pyaudio

import pygame

import RPi.GPIO as GPIO
from time import sleep, time

from random import randint

# |--- START Voice Recognition ---|
model = Model("model")
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1,
                rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

# |--- Audio directory ---|
directory = "Answers/"

# |--- Servo Control ---|
def angle_to_dtcycle(angle):

    dtcycle = 1 + angle/180 # in ms
    dtcycle = 100*dtcycle/20 # in %

    return round(dtcycle,1) 

servo_pin1 = 12 #no
servo_pin2 = 22 #si
servo_pin3 = 13 #base

GPIO.setwarnings(False)         
GPIO.setmode(GPIO.BOARD)        

GPIO.setup(servo_pin1,GPIO.OUT)
GPIO.setup(servo_pin2,GPIO.OUT)
GPIO.setup(servo_pin3,GPIO.OUT)

servo1_pwm = GPIO.PWM(servo_pin1,50)        
servo1_pwm.start(0) 

servo2_pwm = GPIO.PWM(servo_pin2,50)        
servo2_pwm.start(0)     

servo3_pwm = GPIO.PWM(servo_pin3,50)        
servo3_pwm.start(0) 

# |--- main---|

compteur = 0 
value = 0

while True:

    pygame.mixer.init()
    data = stream.read(12000, exception_on_overflow=False)
    
    if len(data) == 0:
        break
    
    if rec.AcceptWaveform(data):
        jres = json.loads(rec.Result())

        print(jres)

        compteur += 1 
        if jres['text'] != '':
        	compteur = 0

        if "hello" in jres['text'] :  # | "hi" | "i"
            print("hello")
            if value == 0:
                print("sound check")
                pygame.mixer.music.load(directory + 'Hello_A.mp3')
                pygame.mixer.music.play()
                print("sound played")
                # happy movement
            # else:
            #     pygame.mixer.music.load(directory + 'Hello_D.mp3')
            #     pygame.mixer.music.play()
            #     # irritated movement

        if "thank you" in jres['text'] :  # | "thank's"
            print("thank you")
            if value == 0:
                pygame.mixer.music.load(directory + 'ThankYou_A.mp3')
                pygame.mixer.music.play()
                # proud movement
            # else:
            #     pygame.mixer.music.load(directory + 'ThankYou_D.mp3')
            #     pygame.mixer.music.play()
            #     # angry movement

        if "please" in jres['text'] :
            print("please")
            if value == 0:
                pygame.mixer.music.load(directory + 'Please_A.mp3')
                pygame.mixer.music.play()
                # proud movement
            # else:
            #     pygame.mixer.music.load(directory + 'Please_D.mp3')
            #     pygame.mixer.music.play()
            #     # angry movement

        if "goodbye" in jres['text'] :
            print("goodbye")
            if value == 0:
                pygame.mixer.music.load(directory + 'Goodbye_A.mp3')
                pygame.mixer.music.play()
            # else:
            #     pygame.mixer.music.load(directory + 'Goodbye_D.mp3')
            #     pygame.mixer.music.play()
            #     # relieved movement

        if "idiot" in jres['text'] :
            print("idiot")
            if value == 0:
                pygame.mixer.music.load(directory + 'Idiot_A.mp3')
                pygame.mixer.music.play()
                print("---angry---")
                # sad movement
            # else:
            #     pygame.mixer.music.load(directory + 'Idiot_D.mp3')
            #     pygame.mixer.music.play()
                # proud movement

        if "stupid" in jres['text'] :  
            print("that's stupid")
            if value == 0:
                pygame.mixer.music.load(directory + 'Stupid_A.mp3')
                pygame.mixer.music.play()
                print("---angry---")
            # else:
            #     pygame.mixer.music.load(directory + 'Stupid_D.mp3')
            #     pygame.mixer.music.play()
                # proud movement
    
    else:
        compteur += 1 
       	#print("compteur : ", compteur)
        if compteur > 35:
        	pass #lancer la discution automatique

