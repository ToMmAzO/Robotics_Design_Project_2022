#Libraries
import RPi.GPIO as GPIO
import time


class Sonar:

	def __init__(self, pin_trigger, pin_echo):
		self.pin_trigger = pin_trigger
		self.pin_echo = pin_echo
		GPIO.setup(self.pin_trigger, GPIO.OUT)
		GPIO.setup(self.pin_echo, GPIO.IN)
		print("*** --- *** --- *** --- ***")
		print("*** sonar activated ***")
		print("*** --- *** --- *** --- ***")
		print("\n")

	def mesure(self):
		# set Trigger to HIGH
		GPIO.output(self.pin_trigger, True)
	
		# set Trigger after 0.01ms to LOW
		time.sleep(0.00001)
		GPIO.output(self.pin_trigger, False)
	
		StartTime = time.time()
		StopTime = time.time()
	
		# save StartTime
		while GPIO.input(self.pin_echo) == 0:
			StartTime = time.time()
	
		# save time of arrival
		while GPIO.input(self.pin_echo) == 1:
			StopTime = time.time()
	
		# time difference between start and arrival
		TimeElapsed = StopTime - StartTime
		# multiply with the sonic speed (34300 cm/s)
		# and divide by 2, because there and back
		distance = (TimeElapsed * 34300) / 2
	
		return distance

