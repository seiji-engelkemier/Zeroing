import RPi.GPIO as GPIO
import time


try:
	# GPIO.setmode(GPIO.BOARD)
	# ZeroPin = 7
	# LedPin = 8

	GPIO.setmode(GPIO.BCM)
	ZeroPin = 4
	LedPin = 14
	
	GPIO.setup(ZeroPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(LedPin, GPIO.OUT)

	# GPIO.output(LedPin, GPIO.HIGH)
	# time.sleep(10)

	state = GPIO.input(ZeroPin)
	print(state)
	while True:
		new_state = GPIO.input(ZeroPin)
		if state != new_state:
			print("beep: "+ repr(new_state))
			state = new_state
			# GPIO.output(LedPin,GPIO.HIGH)
			time.sleep(0.2)
			if state:
				print("here")
				GPIO.output(LedPin, GPIO.HIGH)
			else:
				GPIO.output(LedPin, GPIO.LOW)
			time.sleep(2)
			GPIO.output(LedPin, GPIO.LOW)

		

except KeyboardInterrupt:
	print("You've exited the program.")

finally:
	GPIO.cleanup()