#!/usr/bin/python

import Easydriver as ed
import threading
import time
import Queue
import test
import AMT203
import RPi.GPIO as gpio
import wiringpi

MM_PER_STEP = 0.036
MM_COUNTER = 0

cw = True
ccw = False

print "AQUI: ", test.test_list

#test_list = [(10,True),(50,False)] #,(100,True),(200,False),(350,True),(500,False)]
"""
Arguments to pass or set up after creating the instance.
Step GPIO pin number.
Delay between step pulses in seconds.
Direction GPIO pin number.
Microstep 1 GPIO pin number.
Microstep 2 GPIO pin number.
Microstep 3 GPIO pin number.
Sleep GPIO pin number.
Enable GPIO pin number.
Reset GPIO pin number.
Name as a string.
"""

# Create an instance of the easydriver class.
# Not using sleep, enable or reset in this example.

# stepper_spool = ed.easydriver(18, 0.004, 23, 24, 17)
# stepper_pen = ed.easydriver(27, 0.001, 22, 26, 19)

# Set motor direction to clockwise.

class Z_Motor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.motor = ed.easydriver(27, 0.0001, 22, 26, 19)
        self.motor.set_eighth_step()
        self.mm_per_step_z = 0.003636

    def initial_sequence(self):
        print("Begin zero-ing")
        self.counter = 0
        while Zeroing.zero() == False:
            self.move_down(1)
        if Zeroing.zero():
            print("First contact made")
        self.move_up(6)
        self.move_down(6)
        if Zeroing.zero():
            print("Second contact made")
        else:
            print("Second contact not made")
        self.move_up(6)
        print("Tool is zeroed")

        # First attempt
        # while self.counter < 2:
        #     # print(self.counter)
        #     # self.counter += 1
        #     if zeroing.zero():
        #         print("now here")
        #         self.counter += 1
        #         self.move_up(2)
        #         self.move_down(2)
        #         time.sleep(1)
        #         if Zeroing.zero():
        #             print("Tool is zeroed")
        #             self.counter += 1
        #             time.sleep(3)
        #     else:
        #         self.move_down(1)
        #         time.sleep(1)
        
        # Joao's code
        # self.move_down(6)
        # time.sleep(1)
        # self.move_up(6)
        # time.sleep(1)

    def move_down(self,mm):
        #print "moving down: %s mm" % (mm)
        self.steps_to_move = int(mm/self.mm_per_step_z)
        self.motor.set_direction(cw)
        for i in range(0,self.steps_to_move):
            self.motor.step()
    def move_up(self,mm):
        #print "moving up: %s mm" % (mm)
        self.steps_to_move = int(mm/self.mm_per_step_z)
        self.motor.set_direction(ccw)
        for i in range(0,self.steps_to_move):
            self.motor.step()
    def receive(self, value):
        if value:
            self.move_down(6)
        else:
            self.move_up(6)

    def run(self):
        print "starting pen..."
        self.initial_sequence()


class Spool(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.motor = ed.easydriver(18, 0.00005, 23, 24, 17)
        self.motor.set_eighth_step()
        self.mm_per_step_spool = 0.035

    def initial_sequence(self):
        self.move_forward(5)
        MM_COUNTER = 0
        time.sleep(1)

    def move_forward(self,mm):
        print "moving forward: %s mm" % (mm)
        self.steps_to_move = int(mm/self.mm_per_step_spool)
        self.motor.set_direction(cw)
        for i in range(0,self.steps_to_move):
            self.motor.step()

    def move_step_forward(self):
        self.motor.step()

    def move_back(self,mm):
        #print "moving up: %s mm" % (mm)
        self.steps_to_move = int(mm/self.mm_per_step_spool)
        self.motor.set_direction(ccw)
        for i in range(0,self.steps_to_move):
            self.motor.step()

    def run(self):
        print "starting spool..."
        self.initial_sequence()
        print "[Spool] Starting in:"
        print "[Spool] 3"
        print "[Spool] 2"
        print "[Spool] 1"

class Encoder(threading.Thread):
    def __init__(self, bus, deviceId):
        threading.Thread.__init__(self)
        self.encoder = AMT203.AMT203(bus, deviceId)
        self.last_position = self.encoder.get_position()
        self.last_relative_position = int(self.last_position)
        self.resolution = self.encoder.get_resolution()
        self.gap = 2000
        self.lap = 0
        self.direction = None
        self.perimeter = 44.0118
        self.mm_per_step = self.perimeter/self.resolution
        #self.encoder.set_zero()

    def get_relative_position(self):
        current_position = self.encoder.get_position()
        self.direction = True if (self.last_position < current_position and  current_position - self.last_position < self.gap) or  (self.last_position - current_position > self.gap) else False
        if current_position < self.last_position and self.direction:
            self.lap +=  1
        elif self.last_position - current_position < 0 and not self.direction:
            self.lap -= 1
        self.last_position = current_position
        #print "HELLO", abs(4096 - ((self.lap*self.resolution) + current_position))-4096
        return abs(4096 - ((self.lap*self.resolution) + current_position))-4096

    def set_zero(self):
        print "Setting zero"
        self.encoder.set_zero()

    def run(self):
        print "Class Encoder thread started."
        main.update_value(0.0)
        while True:
            current_relative_position = self.get_relative_position()
            # if current_relative_position != self.last_relative_position:
            #     self.last_relative_position = current_relative_position
            current_relative_position_in_mm = current_relative_position * self.mm_per_step
            main.update_value(current_relative_position_in_mm)
            time.sleep(0.002)

class DC_Motor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.motor_pin = 18
        # gpio.setmode(gpio.BCM)
        # gpio.setup(self.motor_pin, gpio.OUT)
        # gpio.output(self.motor_pin, False)

    def start_motor(self, value):
        #print "inside motor"
        wiringpi.pwmWrite(self.motor_pin, value)

    def stop_motor(self):
        wiringpi.pwmWrite(self.motor_pin, 0)



class Main(threading.Thread):
    def __init__(self):
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(18,2)
        threading.Thread.__init__(self)
        self.queue = Queue.Queue()
        #self.spool = Spool()
        self.dc_motor = DC_Motor()
        self.z_motor = Z_Motor()
        self.encoder = Encoder(0,1)
        self.current_position = None
        self.last_position = None
        self.tolerance = 0.5

    def initial_sequence(self):
        print "Running initial sequence..."
        goal = 5.0 #mm
        self.z_motor.receive(True)
        self.dc_motor.start_motor(700)
        time.sleep(1)
        self.dc_motor.start_motor(0)
        self.z_motor.receive(False)
        self.dc_motor.start_motor(700)
        time.sleep(1)
        self.dc_motor.start_motor(0)        
        self.z_motor.receive(True)
        self.dc_motor.start_motor(700)
        time.sleep(1)
        self.dc_motor.start_motor(0)
        self.z_motor.receive(False)


    def update_value(self,value):
        self.queue.put(value)

    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin
        valueScaled = float(value - leftMin) / float(leftSpan)
        return int(rightMin + (valueScaled * rightSpan))

    def run(self):
        print "HERE"
        self.initial_sequence()
        self.encoder.set_zero()
        time.sleep(1)
        print "THERE"
        self.encoder.start()
        for index, item in enumerate(test.test_list):
            print index
            self.current_position = self.queue.get(True,None)
            objective = 10*item[0]
            if index is not 0:
                start_point = 10*(test.test_list[index-1][0])
            else:
                start_point = 0

            while not 10*item[0] - self.tolerance <= self.current_position <= 10*item[0] + self.tolerance:
                self.current_position = self.queue.get(True,None)
                speed = self.translate(self.current_position, start_point, objective, 1023,500)
                print "Current position in mm: ", self.current_position
                self.dc_motor.start_motor(speed)
                time.sleep(0.001)
            self.dc_motor.stop_motor()
            self.z_motor.receive(item[1])
            #print "We're at: %smm" % (self.current_position)
        self.initial_sequence()
        self.dc_motor.stop_motor()
        gpio.cleanup()
        self.dc_motor.join()
        self.z_motor.join()
        self.encoder.join()
        self.join()

main = Main()
main.start()





# spool = Spool()
# spool.start()

# z_motor = Z_Motor()
# z_motor.start()    			





# stepper_spool.set_direction(cw)
# stepper_spool.set_eighth_step()

# stepper_pen.set_direction(cw)
# stepper_pen.set_eighth_step()

# # for i in range (0,999):
# # 	stepper_spool.step()
# # 	MM_COUNTER = MM_COUNTER + MM_PER_STEP
# # 	print MM_COUNTER

# for i in range (0,1650):
# 	stepper_pen.step()
# 	MM_COUNTER = MM_COUNTER + MM_PER_STEP
# 	print MM_COUNTER

# stepper_pen.set_direction(ccw)

# for i in range (0,1650):
# 	stepper_pen.step()
# 	MM_COUNTER = MM_COUNTER + MM_PER_STEP
# 	print MM_COUNTER


# # Clean up (just calls GPIO.cleanup() function.)
