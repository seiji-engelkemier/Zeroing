import RPi.GPIO as GPIO
import time

# Checks whether pin is zeroed (on z-axis).
# Returns True when zeroed, otherwise False.

def zero():
	try:
		# GPIO.setmode(GPIO.BOARD)
		# ZeroPin = 7
		# LedPin = 8

		GPIO.setmode(GPIO.BCM)
		ZeroPin = 6
		LedPin = 14

		GPIO.setup(ZeroPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(LedPin, GPIO.OUT)

		state = GPIO.input(ZeroPin)
		if state:
			return True
		else:
			return False
	except KeyboardInterrupt:
		print("You've exited the program.")

	finally:
		GPIO.cleanup()