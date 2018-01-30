import RPi.GPIO as GPIO
import time


try:
	# GPIO.setmode(GPIO.BOARD)
	# ButtonPin = 7
	# LedPin = 8

	GPIO.setmode(GPIO.BCM)
	ButtonPin = 6
	LedPin = 14

	GPIO.setup(ButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(LedPin, GPIO.OUT)

	for i in range(0,4):
		state = GPIO.input(ButtonPin)
		print(state)
		if state:
			GPIO.output(LedPin, GPIO.HIGH)
			print("high")
		else:
			GPIO.output(LedPin, GPIO.LOW)
			print("low")
		time.sleep(2)
		GPIO.output(LedPin, GPIO.LOW)

# for i in range(0,3):
# 	GPIO.output(LedPin,GPIO.HIGH)
# 	time.sleep(0.5)
# 	GPIO.output(LedPin, GPIO.LOW)
# 	time.sleep(0.5)
	print("Successfully completed the program")
except KeyboardInterrupt:
	print("You've exited the program")
finally:	
	GPIO.cleanup()