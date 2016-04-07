#!/usr/bin/env python

import rospy
import os
import thread
import time

from std_msgs.msg import Float64

#degreeToPoints = {"30": 0.2, "60": 0.5, "90": 0.8}

def degreeToPoints(degreeAsString):
    degreeAsInt = float(degreeAsString)
    return degreeAsInt / (200 - degreeAsInt)

def sendDataToRobot(pipe, publisher):

    while 1:
        degree = pipe.read()
        if degree:
            ##### { Uncoment for debug }
            #####print "Data: " + degree + " -> " + `Float64(degreeToPoints(degree))`
            publisher.publish(Float64(degreeToPoints(degree)))
            rospy.sleep(1)
        time.sleep(1)

if __name__ == "__main__":

    # { Setup link to Robot }
    rospy.init_node('test', anonymous=True)

    thumbTop        = rospy.Publisher('sh_thj1_mixed_position_velocity_controller/command', Float64, latch=False)
    thumbMiddle     = rospy.Publisher('sh_thj2_mixed_position_velocity_controller/command', Float64, latch=False)
    thumbBase       = rospy.Publisher('sh_thj4_mixed_position_velocity_controller/command', Float64, latch=False)

    pointerTop      = rospy.Publisher('sh_ffj0_mixed_position_velocity_controller/command', Float64, latch=False)
    pointerBase     = rospy.Publisher('sh_ffj3_mixed_position_velocity_controller/command', Float64, latch=False)

    middleTop       = rospy.Publisher('sh_mfj0_mixed_position_velocity_controller/command', Float64, latch=False)
    middleBase      = rospy.Publisher('sh_mfj3_mixed_position_velocity_controller/command', Float64, latch=False)

    ringTop         = rospy.Publisher('sh_rfj0_mixed_position_velocity_controller/command', Float64, latch=False)
    ringBase        = rospy.Publisher('sh_rfj3_mixed_position_velocity_controller/command', Float64, latch=False)

    smallTop        = rospy.Publisher('sh_lfj0_mixed_position_velocity_controller/command', Float64, latch=False)
    smallBase       = rospy.Publisher('sh_lfj3_mixed_position_velocity_controller/command', Float64, latch=False)

    rospy.sleep(2)

    # { Setup pipes }
    thumbTopPipe    = open("thumbTopPipe", 'r')
    thumbMiddlePipe = open("thumbMiddlePipe", 'r')
    thumbBasePipe   = open("thumbBasePipe", 'r')

    pointerTopPipe  = open("pointerTopPipe", 'r')
    pointerBasePipe = open("pointerBasePipe", 'r')

    middleTopPipe   = open("middleTopPipe", 'r')
    middleBasePipe  = open("middleBasePipe", 'r')

    ringTopPipe     = open("ringTopPipe", 'r')
    ringBasePipe    = open("ringBasePipe", 'r')

    smallTopPipe    = open("smallTopPipe", 'r')
    smallBasePipe   = open("smallBasePipe", 'r')

    # { Setup threads to read from pipes }
    thread.start_new_thread(sendDataToRobot, (thumbTopPipe, thumbTop))
    thread.start_new_thread(sendDataToRobot, (thumbMiddlePipe, thumbMiddle))
    thread.start_new_thread(sendDataToRobot, (thumbBasePipe, thumbBase))

    thread.start_new_thread(sendDataToRobot, (pointerTopPipe, pointerTop))
    thread.start_new_thread(sendDataToRobot, (pointerBasePipe, pointerBase))

    thread.start_new_thread(sendDataToRobot, (middleTopPipe, middleTop))
    thread.start_new_thread(sendDataToRobot, (middleBasePipe, middleBase))

    thread.start_new_thread(sendDataToRobot, (ringTopPipe, ringTop))
    thread.start_new_thread(sendDataToRobot, (ringBasePipe, ringBase))

    thread.start_new_thread(sendDataToRobot, (smallTopPipe, smallTop))
    thread.start_new_thread(sendDataToRobot, (smallBasePipe, smallBase))

    while 1:
       pass

