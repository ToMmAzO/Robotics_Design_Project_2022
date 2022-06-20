# Custom libraries
import Angel
import Devil
import Sonar

# Threading
from queue import Queue
from threading import Thread, Lock
from time import sleep, time

# Raspi Connect
import RPi.GPIO as GPIO

# Voice recognition
from vosk import Model, KaldiRecognizer
import json
import pyaudio
import pygame

# Sound Control
from pydub import AudioSegment
from pydub.playback import play

# Capative sensor
import board
from digitalio import DigitalInOut, Direction

# various libraries
import numpy as np


def voice_recognizer(out_q_angel, out_q_devil, lock, sonar_left, sonar_right, pad_angel, pad_devil):
	print("voice_recognition activated")

	list_keywords = ["thanks", "hello", "goodbye", "please", "stupid", "idiot"]

	global state_on_off
	global pad_angel_already_pressed
	global pad_devil_already_pressed
	global person_detected

	timer_state = False
	# voice regonition setup up
	model = Model("model")
	rec = KaldiRecognizer(model, 16000)
	p = pyaudio.PyAudio()
	stream = p.open(format=pyaudio.paInt16, channels=1,
					rate=16000, input=True, frames_per_buffer=8000)
	stream.start_stream()

	sound = AudioSegment.from_wav("Sounds/woow.wav")
	play(sound)

	out_q_angel.put("woow")
	out_q_devil.put("woow")


	# main loop
	while True:
		data = stream.read(12000, exception_on_overflow=False)

		if len(data) == 0:
			break

		# touch based activation
		if pad_angel.value and not pad_angel_already_pressed:
			#print("Pad angel just pressed")
			out_q_angel.put("touch angel")
			timer_state = False
			#out_q.put("touch angel")
		pad_angel_already_pressed = pad_angel.value

		if pad_devil.value and not pad_devil_already_pressed:
			#print("Pad devil just pressed")
			out_q_devil.put("touch devil")
			timer_state = False
			#out_q.put("touch devil")
		pad_devil_already_pressed = pad_devil.value

		
		## person approaching
		if person_detected == False and state_on_off == True:
			print("person check")
			distance_sonar_left = sonar_left.mesure()
			distance_sonar_right = sonar_right.mesure()
			print("distances : {} and {}".format(distance_sonar_left, distance_sonar_right))
			if (30<distance_sonar_left<120) and (30<distance_sonar_right<120):
				person_detected = True
				out_q_angel.put("person")
				sleep(1)
				out_q_devil.put("person")
		
		# voice and random based avtivation

		if rec.AcceptWaveform(data):
			jres = json.loads(rec.Result())

			print(jres)

			# random based activation
			if jres['text'] in ['', 'huh'] and timer_state == False:
				print("silence conteur started")
				random_start = time()
				timer_state = True

			elif jres['text'] in ['', 'huh'] and timer_state == True:
				if ((time()-random_start) > 10):  # time before automated interection begins
					print("robot random action")
					out_q_angel.put("time based")
					sleep(0.8)
					out_q_devil.put("time based")
					timer_state = False

			# speech based activation
			else:
				timer_state = False

				list_words_recognized = jres['text'].split()


				#print("sonar distances : left = {} and right = {}".format(distance_sonar_left, distance_sonar_right))
				# and (30<distance_sonar_left<120) and (30<distance_sonar_right<120):
				if state_on_off == True: 
					for i in range(len(list_words_recognized)):
						if list_words_recognized[i] in list_keywords:
							# print("---*---*---*---*---*---")
							print("recognized words : ", list_words_recognized[i])
							out_q_angel.put(list_words_recognized[i])
							sleep(1)
							out_q_devil.put(list_words_recognized[i])
							break


def control_angel(in_q, lock, robot_angel, ):
	print("robot angel activated")
	
	global state_on_off

	while True:

		if state_on_off == True:

			# lock.acquire()

			if not in_q.empty():
				text = in_q.get(timeout=1)

				print("angel - received text : ", text)
				# lock.release()

				# transform word to adequate expression
				if text in ["hello"]:
					expression = "happy"
					sound = AudioSegment.from_wav("Sounds/ANGEL/new/Hi!.wav")
					play(sound)
				elif text in ["thanks"]:
					expression = "proud"
					sound = AudioSegment.from_wav("Sounds/ANGEL/new/You’re welcome.wav")
					play(sound)
				elif text in ["please"]:
					expression = "proud"
					sound = AudioSegment.from_wav("Sounds/ANGEL/new/Of course.wav")
					play(sound)
				elif text in ["goodbye"]:
					expression = "ashamed"
					sound = AudioSegment.from_wav("Sounds/ANGEL/new/Sorry about that, bye.wav")
					play(sound)
				elif text in ["idiot"]:
					expression = "sad"
					sound = AudioSegment.from_wav("Sounds/ANGEL/new/Please don’t say that.wav")
					play(sound)
				elif text in ["stupid"]:
					expression = "sad"
					sound = AudioSegment.from_wav("Sounds/ANGEL/new/No no no.wav")
					play(sound)
				elif text in ["time based"]:
					expression = "time based"
					sound = AudioSegment.from_wav("Sounds/ANGEL/new/Debate.wav")
					play(sound)
				elif text in ["touch angel"]:
					expression = "touch angel"
					sound = AudioSegment.from_wav("Sounds/ANGEL/new/Oh that’s nice.wav")
					play(sound)
				elif text in ["person"]:
					expression = "person"
					sound = AudioSegment.from_wav("Sounds/ANGEL/new/Come here.wav")
				elif text in ["woow"]:
					expression = "woow"

			else:
				expression = "no expression"
				#print("no expression")
				sleep(0.1)

		# robot does the expression
		robot_angel.express(expression, state_on_off)
		
		expression = None


def control_devil(in_q, lock, robot_devil, ):
	print("robot devil activated")

	# |--- Audio directory ---|
	directory = "Sounds/DEVIL/new/"

	global state_on_off

	while True:

		if state_on_off == True:

			# lock.acquire()

			if not in_q.empty():
				text = in_q.get()
				print("devil - received text : ", text)
				# lock.release()

				# transform word to adequate expression
				if text in ["hello"]:
					expression = "irritation"
					sound = AudioSegment.from_wav("Sounds/DEVIL/new/Don’t talk to me.wav")
					play(sound)

				elif text in ["thanks"]:
					expression = "angry"
					sound = AudioSegment.from_wav("Sounds/DEVIL/new/Ewww.wav")
					play(sound)

				elif text in ["please"]:
					expression = "angry"
					sound = AudioSegment.from_wav("Sounds/DEVIL/new/Can you not.wav")
					play(sound)

				elif text in ["goodbye"]:
					expression = "relieved"
					sound = AudioSegment.from_wav("Sounds/DEVIL/new/Oh finally.wav")
					play(sound)

				elif text in ["idiot"]:
					expression = "proud"
					sound = AudioSegment.from_wav("Sounds/DEVIL/new/Oh good job.wav")
					play(sound)

				elif text in ["stupid"]:
					expression = "happy"
					sound = AudioSegment.from_wav("Sounds/DEVIL/new/I agree.wav")
					play(sound)

				elif text in ["time based"]:
					expression = "time based"
					sound = AudioSegment.from_wav("Sounds/DEVIL/new/Debate.wav")
					play(sound)

				elif text in ["touch devil"]:
					expression = "touch devil"
					sound = AudioSegment.from_wav("Sounds/DEVIL/new/Eww go away.wav")
					play(sound)

				elif text in ["person"]:
					expression = "person"
					sound = AudioSegment.from_wav("Sounds/DEVIL/new/No why.wav")
					play(sound)

				elif text in ["woow"]:
					expression = "woow"

			else:
				expression = "no expression"
				#print("no expression")
				sleep(1)

		# robot does the expression
		robot_devil.express(expression, state_on_off)
		expression = None

# create robot instances


robot_angel = Angel.Angel(25, 13, 12)
robot_devil = Devil.Devil(23, 22, 24)

# creat sonar instances

sonar_left = Sonar.Sonar(20, 16)
sonar_right = Sonar.Sonar(6, 5)

# Define capacitive sensor parameters

pad_angel_pin = board.D17
pad_devil_pin = board.D4

pad_angel = DigitalInOut(pad_angel_pin)
pad_devil = DigitalInOut(pad_devil_pin)

pad_angel.direction = Direction.INPUT
pad_devil.direction = Direction.INPUT

pad_angel_already_pressed = True
pad_devil_already_pressed = True


# Create the shared queue and launch both threads
q_angel = Queue()
q_devil = Queue()

lock = Lock()

t_angel = Thread(target=control_angel, args=(q_angel, lock, robot_angel, ))
t_devil = Thread(target=control_devil, args=(q_devil, lock, robot_devil, ))
t_main = Thread(target=voice_recognizer, args=(q_angel, q_devil, lock, sonar_left, sonar_right, pad_angel, pad_devil))

# t_angel.start()
# t_devil.start()
# t_main.start()

# Wait for all produced items to be consumed
# q.join()

###########################################################################################
GPIO.setwarnings(False)  # Ignore warning for now
GPIO.setmode(GPIO.BCM)  # Use physical pin numbering

state_on_off = False
pin_button = 27
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

person_detected = False

###########################################################################################


def my_callback(channel, t_main, t_angel, t_devil):
	#sleep(0.1)
	print("button pressed")
	global state_on_off
	global compteur
	#print("state_on_off = ", state_on_off)
	if GPIO.input(27) and state_on_off == False:     # if port 25 == 1
		print("Robot turned on !")
		state_on_off = True

		if compteur == 0:
			compteur += 1
			t_angel.start()
			t_devil.start()
			t_main.start()
			sleep(1)

	if state_on_off == True and GPIO.input(27):
		tik = time()
		print("first press for off")
		sleep(0.2)
		dt = time() - tik
		while(dt < 1.2):
			#print("waiting for second press ")
			dt = time() - tik
			sleep(0.1)
			if GPIO.input(27):
				state_on_off = False
				print("Robot turned off")
				dt = 5

############################################################################################


i = 0
compteur = 0

GPIO.add_event_detect(27, GPIO.RISING, callback=lambda channel: my_callback(
	channel, t_main, t_angel, t_devil))

while True:
	i = (i+1) % 2
	sleep(0.1)

GPIO.cleanup()
