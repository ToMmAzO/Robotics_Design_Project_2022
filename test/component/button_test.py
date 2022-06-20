import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep, time


GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering

state_on_off = False
pin_button = 27
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) 

def my_callback(channel):
	sleep(0.1)

	global state_on_off

	if GPIO.input(27) and state_on_off == False :     # if port 25 == 1  
		print ("Robot turned on !")
		state_on_off = True
		sleep(1)

	if state_on_off == True and GPIO.input(27):
		tik = time()
		print("first press for off")
		sleep(0.2)
		dt = time() -tik
		while(dt<1.2):
			#print("waiting for second press ")
			dt = time() - tik
			sleep(0.1)
			if GPIO.input(27):
				state_on_off = False
				print("Robot turned off")
				dt = 5





i=0

GPIO.add_event_detect(27, GPIO.BOTH, callback=my_callback) 

while True:
	if state_on_off == True:
		i = i+1
		print ("i = ", i)
		sleep(1)

GPIO.cleanup() # Clean up
