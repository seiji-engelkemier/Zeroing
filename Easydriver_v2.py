
#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time, sys


class easydriver(object):
    def __init__(self,pin_step=0,delay=0.1,pin_direction=0,pin_ms1=0,pin_ms2=0,pin_ms3=0,pin_sleep=0,pin_enable=0,pin_reset=0,name="Stepper"):
        self.pin_step = pin_step
        self.delay = delay / 2
        self.pin_direction = pin_direction
        self.pin_microstep_1 = pin_ms1
        self.pin_microstep_2 = pin_ms2
        self.pin_microstep_3 = pin_ms3
        self.pin_sleep = pin_sleep
        self.pin_enable = pin_enable
        self.pin_reset = pin_reset
        self.name = name

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        if self.pin_step > 0:
            GPIO.setup(self.pin_step, GPIO.OUT)
        if self.pin_direction > 0:
            GPIO.setup(self.pin_direction, GPIO.OUT)
            GPIO.output(self.pin_direction, True)
        if self.pin_microstep_1 > 0:
            GPIO.setup(self.pin_microstep_1, GPIO.OUT)
            GPIO.output(self.pin_microstep_1, False)
        if self.pin_microstep_2 > 0:
            GPIO.setup(self.pin_microstep_2, GPIO.OUT)
            GPIO.output(self.pin_microstep_2, False)
        if self.pin_microstep_3 > 0:
            GPIO.setup(self.pin_microstep_3, GPIO.OUT)
            GPIO.output(self.pin_microstep_3, False)
        if self.pin_sleep > 0:
            GPIO.setup(self.pin_sleep, GPIO.OUT)
            GPIO.output(self.pin_sleep,True)
        if self.pin_enable > 0:
            GPIO.setup(self.pin_enable, GPIO.OUT)
            GPIO.output(self.pin_enable,False)
        if self.pin_reset > 0:
            GPIO.setup(self.pin_reset, GPIO.OUT)
            GPIO.output(self.pin_reset,True)


    def step(self):
        GPIO.output(self.pin_step,True)
        time.sleep(self.delay)
        GPIO.output(self.pin_step,False)
        time.sleep(self.delay)

    def set_direction(self,direction):
        GPIO.output(self.pin_direction,direction)

    def set_full_step(self):
        GPIO.output(self.pin_microstep_1,False)
        GPIO.output(self.pin_microstep_2,False)
        #GPIO.output(self.pin_microstep_3,False)
        
    def set_half_step(self):
        GPIO.output(self.pin_microstep_1,True)
        GPIO.output(self.pin_microstep_2,False)
        GPIO.output(self.pin_microstep_3,False)
        
    def set_quarter_step(self):
        GPIO.output(self.pin_microstep_1,False)
        GPIO.output(self.pin_microstep_2,True)
        GPIO.output(self.pin_microstep_3,False)
        
    def set_eighth_step(self):
        GPIO.output(self.pin_microstep_1,True)
        GPIO.output(self.pin_microstep_2,True)
        #GPIO.output(self.pin_microstep_3,False)

    def set_sixteenth_step(self):
        GPIO.output(self.pin_microstep_1,True)
        GPIO.output(self.pin_microstep_2,True)
        GPIO.output(self.pin_microstep_3,True)

    def sleep(self):
        GPIO.output(self.pin_sleep,False)

    def wake(self):
        GPIO.output(self.pin_sleep,True)
    
    def disable(self):
        GPIO.output(self.pin_enable,True)

    def enable(self):
        GPIO.output(self.pin_enable,False)

    def reset(self):
        GPIO.output(self.pin_reset,False)
        time.sleep(1)
        GPIO.output(self.pin_reset,True)

    def set_delay(self, delay):
        self.delay = delay / 2

    def finish(self):
        GPIO.cleanup()