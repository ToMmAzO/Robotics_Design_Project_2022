import RPi.GPIO as GPIO
from time import sleep, time
import numpy as np
from random import randint


class Angel:

	servo1_ang_min = 30
	servo1_ang_max = 180
	servo1_ang_mil = 90

	servo2_ang_min = 0
	servo2_ang_max = 180
	servo2_ang_mil = 90

	servo3_ang_min = 0
	servo3_ang_max = 180
	servo3_ang_mil = 90

	number_of_seperation = 10

	list_ang_servo1 = np.linspace(
		servo1_ang_min, servo1_ang_max, number_of_seperation, dtype=int)
	list_ang_servo2 = np.linspace(
		servo2_ang_min, servo2_ang_max, number_of_seperation, dtype=int)
	list_ang_servo3 = np.linspace(
		servo3_ang_min, servo3_ang_max, number_of_seperation, dtype=int)

	number_of_seperation_slow = 2*number_of_seperation

	list_ang_servo1_slow = np.linspace(
		servo1_ang_min, servo1_ang_max, number_of_seperation_slow, dtype=int)
	list_ang_servo2_slow = np.linspace(
		servo2_ang_min, servo2_ang_max, number_of_seperation_slow, dtype=int)
	list_ang_servo3_slow = np.linspace(
		servo3_ang_min, servo3_ang_max, number_of_seperation_slow, dtype=int)

	def angle_to_dtcycle(self, angle):
		dtcycle = 1 + angle/180 # in ms
		dtcycle = 100*dtcycle/20 # in %
		return round(dtcycle,1) 

	def __init__(self, pin_yes, pin_no, pin_base):

		self.servo_pin1 = pin_yes  # 25 #si
		self.servo_pin2 = pin_no  # 13 #no
		self.servo_pin3 = pin_base  # 12 #base

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)

		GPIO.setup(self.servo_pin1,GPIO.OUT)
		GPIO.setup(self.servo_pin2,GPIO.OUT)
		GPIO.setup(self.servo_pin3,GPIO.OUT)

		self.servo1_pwm = GPIO.PWM(self.servo_pin1,50)
		self.servo1_pwm.start(0)

		self.servo2_pwm = GPIO.PWM(self.servo_pin2,50)
		self.servo2_pwm.start(0)

		self.servo3_pwm = GPIO.PWM(self.servo_pin3,50)
		self.servo3_pwm.start(0)

		print("*** --- *** --- *** --- ***")
		print("*** robot angel launched ***")
		print("*** --- *** --- *** --- ***")
		print("\n")
	
	def express(self, expression, state_on_off):
		if state_on_off:
			#################################################################
			if expression == "happy":
				print("robot angel acting happy")
				for i in range(2):
					for i in range(self.number_of_seperation):
						self.servo1_pwm.ChangeDutyCycle(self.angle_to_dtcycle(self.list_ang_servo1[i])) 
						sleep(0.03)
						self.servo1_pwm.ChangeDutyCycle(0)

					for i in range(self.number_of_seperation-1,-1,-1):
						self.servo1_pwm.ChangeDutyCycle(self.angle_to_dtcycle(self.list_ang_servo1[i])) 
						sleep(0.03)
						self.servo1_pwm.ChangeDutyCycle(0)
				sleep(1)

			#################################################################
			elif expression == "proud":
				print("robot angel acting with proud thanks")
				angle_down = 10
				self.servo1_pwm.ChangeDutyCycle(self.angle_to_dtcycle(self.servo1_ang_max))
				sleep(0.05)
				self.servo1_pwm.ChangeDutyCycle(0)

				angle_shake = 15
				angle_changer = 0

				for i in range(3):
					angle_changer = (angle_changer+1) 
					self.servo1_pwm.ChangeDutyCycle(self.angle_to_dtcycle(self.servo1_ang_mil + (-1)**(angle_changer)*angle_shake))
					sleep(0.1)
					self.servo1_pwm.ChangeDutyCycle(0)
					sleep(0.1)
					self.servo1_pwm.ChangeDutyCycle(self.angle_to_dtcycle(self.servo1_ang_mil))
					sleep(0.1)
				sleep(1)


			#################################################################
			elif expression == "ashamed":
				print("robot angel acting with ashamed")
				for i in range(self.number_of_seperation_slow//2, self.number_of_seperation_slow):
					self.servo2_pwm.ChangeDutyCycle(self.angle_to_dtcycle(self.list_ang_servo2_slow[i]))
					self.servo3_pwm.ChangeDutyCycle(self.angle_to_dtcycle(self.list_ang_servo3_slow[i]))
					sleep(0.01)
					self.servo2_pwm.ChangeDutyCycle(self.angle_to_dtcycle(0))
					self.servo3_pwm.ChangeDutyCycle(self.angle_to_dtcycle(0))
				sleep(1)


			#################################################################
			elif expression == "sad":
				print("robot angel acting with sad idiot")
				for i in range(self.number_of_seperation):
					self.servo1_pwm.ChangeDutyCycle(self.angle_to_dtcycle(self.list_ang_servo1[i]))
					sleep(0.05)
					self.servo1_pwm.ChangeDutyCycle(0)

				for i in range(2):
					for i in range(self.number_of_seperation-1,-1,-1):
						self.servo3_pwm.ChangeDutyCycle(self.angle_to_dtcycle(self.list_ang_servo3[i])/2)
						sleep(0.05)
						self.servo3_pwm.ChangeDutyCycle(0)
					for i in range(self.number_of_seperation):
						self.servo3_pwm.ChangeDutyCycle(self.angle_to_dtcycle(self.list_ang_servo3[i])/2)
						sleep(0.05)
						self.servo3_pwm.ChangeDutyCycle(0)
				sleep(1)

			#################################################################
			elif expression == "time based":
				print("robot angel acting based on time")
				for i in range(2):
					for i in range(self.number_of_seperation-1,-1,-1):
						self.servo3_pwm.ChangeDutyCycle(self.angle_to_dtcycle(self.list_ang_servo3[i])/2)
						sleep(0.05)
						self.servo3_pwm.ChangeDutyCycle(0)
					for i in range(self.number_of_seperation):
						self.servo3_pwm.ChangeDutyCycle(self.angle_to_dtcycle(self.list_ang_servo3[i])/2)
						sleep(0.05)
						self.servo3_pwm.ChangeDutyCycle(0)
				sleep(1)

			#################################################################
			elif expression == "touch angel":
				print("robot angel acting based on touch")
				for i in range(2):
					for i in range(self.number_of_seperation):
						self.servo1_pwm.ChangeDutyCycle(self.angle_to_dtcycle(self.list_ang_servo1[i])) 
						sleep(0.03)
						self.servo1_pwm.ChangeDutyCycle(0)

					for i in range(self.number_of_seperation-1,-1,-1):
						self.servo1_pwm.ChangeDutyCycle(self.angle_to_dtcycle(self.list_ang_servo1[i])) 
						sleep(0.03)
						self.servo1_pwm.ChangeDutyCycle(0)
				sleep(1)

			#################################################################
			elif expression == "person":
				print("robot angel acting based on person")
				for i in range(2):
					for i in range(self.number_of_seperation):
						self.servo1_pwm.ChangeDutyCycle(self.angle_to_dtcycle(self.list_ang_servo1[i])) 
						sleep(0.03)
						self.servo1_pwm.ChangeDutyCycle(0)

					for i in range(self.number_of_seperation-1,-1,-1):
						self.servo1_pwm.ChangeDutyCycle(self.angle_to_dtcycle(self.list_ang_servo1[i])) 
						sleep(0.03)
						self.servo1_pwm.ChangeDutyCycle(0)
				sleep(1)

			elif expression == "woow":
				for i in range(self.number_of_seperation):
					self.servo1_pwm.ChangeDutyCycle(self.angle_to_dtcycle(self.list_ang_servo1[i]))
					self.servo2_pwm.ChangeDutyCycle(self.angle_to_dtcycle(self.list_ang_servo2[i]))
					sleep(0.05)
					self.servo1_pwm.ChangeDutyCycle(0)
					self.servo2_pwm.ChangeDutyCycle(0)

				for i in range(self.number_of_seperation-1, -1, -1):
					self.servo1_pwm.ChangeDutyCycle(self.angle_to_dtcycle(self.list_ang_servo1[i]))
					self.servo2_pwm.ChangeDutyCycle(self.angle_to_dtcycle(self.list_ang_servo2[i]))
					sleep(0.05)
					self.servo1_pwm.ChangeDutyCycle(0)
					self.servo2_pwm.ChangeDutyCycle(0)


			#################################################################
			else:
				#sleep(1)
				if randint(1,15) == 1:
					#print("----------robot angel acting natural")
					for i in range(self.number_of_seperation):
						self.servo2_pwm.ChangeDutyCycle(self.angle_to_dtcycle(self.list_ang_servo2[i])) 
						sleep(0.03)
						self.servo2_pwm.ChangeDutyCycle(0)

					for i in range(self.number_of_seperation-1,-1,-1):
						self.servo2_pwm.ChangeDutyCycle(self.angle_to_dtcycle(self.list_ang_servo2[i])) 
						sleep(0.03)
						self.servo2_pwm.ChangeDutyCycle(0)

					sleep(1)
				else:
					sleep(1)	

