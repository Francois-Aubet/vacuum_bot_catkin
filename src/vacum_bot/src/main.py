#!/usr/bin/env python

import numpy as np
import math
import time
from socketManager import SocketManager
from picoFlexxSens import PicoFlexxSens
from motorControl import MotorControl
import rospy


# one entry in the matrix is 10cm times 10cm
# unit of the sensor is m

class Main:

    """
    Be carfull!!! every thing is :
        angles in rad
        distances in cm

    """


    def __init__(self):
        """

        """


        # Hyperparameters
        self.LAMBDA = 1.047 # Angle of the depth sensor 60*pi/180         but in rad!!!!!
        self.N_RASTERPOINTS = 224 # Amount of values in one row of the depth sensor matrix 224
        self.MATRIX_SIZE = 100 # 1000
        self.SCALE_SENSOR_TO_CM = 100 # 100
        self.EPS_DISTANCE = 5 # cells


        # robot parameters
        self.x_pos = int(round(self.MATRIX_SIZE/2))
        self.y_pos = int(round(self.MATRIX_SIZE/2))

        # matrix
        self.ma_room = [[0 for i in range(self.MATRIX_SIZE)] for j in range(self.MATRIX_SIZE)]

        # set the robot into the room
        self.ma_room[self.x_pos][self.y_pos] = -1

        # sensor input
        self.distances = 0
        self.angleToNorth = 0
        self.picoAngle = 0

        self.motors = MotorControl()

        self.rangeSens = PicoFlexxSens(self)
        self.rangeSens.start()

        # starting side methods
        self.socketCo = SocketManager(self)
        self.socketCo.start()






    def startMapping(self):
        if 0: # Start Main routine
            # initialy get 360 view of the first position
            self.process360view()

            # store current distance
            dis = self.distances[round(len(self.distances)/2)]*self.SCALE_SENSOR_TO_CM

            # move forward approximately 1 meter
            self.runMotors(2)

            # update the robot position
            self.update_position(self.distances[round(len(self.distances)/2)]*self.SCALE_SENSOR_TO_CM - dis)

            # get 360 view of the second position
            self.process360view()

            # turn to left
            self.turnRobot(-90)

            # store current distance
            dis = self.distances[round(len(self.distances)/2)]*self.SCALE_SENSOR_TO_CM

            # move forward approximately 1 meter
            self.runMotors(2)

            # update the robot position
            self.update_position(self.distances[round(len(self.distances)/2)]*self.SCALE_SENSOR_TO_CM - dis)

            # get 360 view of the third position
            self.process360view()
        else: # Start Debug routine
            self.distances = [2,2,2]
            self.angleToNorth = math.pi
            self.update_matrix()

            self.update_position(0)

            print(np.array(self.ma_room))
            print(self.x_pos)
            print(self.y_pos)




    def update_matrix(self):
        for act_pos in range(len(self.distances)):
            print ("distance: " + str(self.distances[act_pos]*self.SCALE_SENSOR_TO_CM))
            d = self.distances[act_pos]*self.SCALE_SENSOR_TO_CM
            n = round(act_pos-math.floor(len(self.distances)/2))
            e1 = int(round(self.x_pos + math.sin(self.angleToNorth + self.picoAngle + n*self.LAMBDA/self.N_RASTERPOINTS)*d))
            e2 = int(round(self.y_pos + math.cos(self.angleToNorth + self.picoAngle + n*self.LAMBDA/self.N_RASTERPOINTS)*d))
            if e1 >= 0 and e1 < self.MATRIX_SIZE and e2 >= 0 and e2 < self.MATRIX_SIZE:
                self.ma_room[e1][e2] = 1
            self.socketCo.send(str(e1) + "," + str(e2) + "," + str(1))
            print ("sending targetted packet:" + str(e1) + "," + str(e2))

        #self.socketCo.sendMatrix()


    def update_position(self, distance_difference):
        self.ma_room[int(round(self.x_pos))][int(round(self.y_pos))] = 0
        self.x_pos = self.x_pos + math.sin(self.angleToNorth+self.picoAngle)*distance_difference
        self.y_pos = self.y_pos + math.cos(self.angleToNorth+self.picoAngle)*distance_difference
        self.ma_room[int(round(self.x_pos))][int(round(self.y_pos))] = -1




    def turnPico(self,angle):
        # extern
        return 0







    def runMotors(self,sec): # Run Motors for a defined amount of time
        self.motors.driveForward(sec)
        return 0


    def runMotorsForward(self): # Run Motors until stopped
        # extern
        return 0

    def stopMotors(self): # Stop Motors
        self.motors.stop()
        return 0

    def runMotorsBackwards(self):
        self.motors.driveBackward(2)
        return 0

    def turnRobot(self,angle):
        # extern
        return 0

    def turnRobotToAbsoluteAngle(self,absolute_angle):
        #extern
        return 0










    def process360view(self):
        for i in range(6):
            self.update_matrix()
            self.turnPico(60)

    def moveToPosition(self, x, y):
        # Need to distuingish different cases
        phi = -1
        if x-self.x_pos >= 0 and y-self.y_pos >= 0:
            phi = math.atan((x-self.x_pos)/(y-self.y_pos))
        elif x-self.x_pos >= 0 and y-self.y_pos <= 0:
            phi = math.atan((self.y_pos - y)/(x-self.x_pos)) + math.pi/2
        elif x-self.x_pos <= 0 and y-self.y_pos <= 0:
            phi = math.atan((self.x_pos - x)/(self.y_pos - y)) + math.pi
        elif x-self.x_pos <= 0 and y-self.y_pos >= 0:
            phi = math.atan((y-self.y_pos)/(self.x_pos-x)) + math.pi*270/360

        phi = phi*180/math.pi

        self.turnRobotToAbsoluteAngle(phi)
        last_position = np.array([self.x_pos,self.y_pos])
        self.runMotorsInf()
        while np.linalg.norm(np.array([x,y]) - np.array([self.x_pos,self.y_pos])) > self.EPS_DISTANCE:
            self.update_position(np.linalg.norm(np.array([self.x_pos,self.y_pos])-last_position))
            last_position = np.array([self.x_pos,self.y_pos])
            # sleep(100) # Needed?
        self.stopMotors()





start = Main()
#time.sleep(1)
#start.update_matrix()



