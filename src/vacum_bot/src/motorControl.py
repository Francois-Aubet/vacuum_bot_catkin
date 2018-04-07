# !/usr/bin/env python

import RPi.GPIO as GPIO
import time





class MotorControl():

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        self.L_DIR_PIN = 13
        self.L_PWM_PIN = 6
        self.R_DIR_PIN = 26
        self.R_PWM_PIN = 19

        self.FWD = GPIO.LOW
        self.BWD = GPIO.HIGH

        self.DRIVE_SPEED = 100.0
        self.TURN_SPEED = 80.0

        self.PWM_frequency = 10000

        gpios = [self.L_DIR_PIN, self.L_PWM_PIN, self.R_DIR_PIN, self.R_PWM_PIN]

        for pin in gpios:
            GPIO.setup(pin, GPIO.OUT)

        L_PWM = GPIO.PWM(self.L_PWM_PIN, self.PWM_frequency)
        R_PWM = GPIO.PWM(self.R_PWM_PIN, self.PWM_frequency)

        L_PWM.start(0)
        R_PWM.start(0)

    def PWM(self,seconds, dc):
        self.L_PWM.ChangeDutyCycle(dc)
        self.R_PWM.ChangeDutyCycle(dc)

        time.sleep(seconds)

        self.L_PWM.ChangeDutyCycle(0)
        self.R_PWM.ChangeDutyCycle(0)


    def driveForward(self, seconds ):

        GPIO.output(self.L_DIR_PIN, self.FWD)
        GPIO.output(self.R_DIR_PIN, self.FWD)

        self.PWM(seconds, self.DRIVE_SPEED)
        self.stop()

    def driveBackward(self, seconds ):

        GPIO.output(self.L_DIR_PIN, self.BWD)
        GPIO.output(self.R_DIR_PIN, self.BWD)

        self.PWM(seconds, self.DRIVE_SPEED)
        self.stop()

    def turnLeft(self, seconds ):

        GPIO.output(self.L_DIR_PIN, self.BWD)
        GPIO.output(self.R_DIR_PIN, self.FWD)

        self.PWM(seconds, self.TURN_SPEED)
        self.stop()

    def turnRight(self, seconds ):

        GPIO.output(self.L_DIR_PIN, self.FWD)
        GPIO.output(self.R_DIR_PIN, self.BWD)

        self.PWM(seconds, self.TURN_SPEED)
        self.stop()

    def stop(self):
        self.L_PWM.stop()
        self.R_PWM.stop()