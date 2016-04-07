#!/usr/bin/env python

import rospy

from std_msgs.msg import Float64

if __name__ == "__main__":

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

    for i in range(1,5):
        x = 1.0;
        if i % 2 == 0:
            x = 0.0

        #print x

        thumbTop.publish(Float64(x))
        thumbMiddle.publish(Float64(x))
        thumbBase.publish(Float64(x))

        pointerTop.publish(Float64(x))
        pointerBase.publish(Float64(x))

        middleTop.publish(Float64(x))
        middleBase.publish(Float64(x))

        ringTop.publish(Float64(x))
        ringBase.publish(Float64(x))

        smallTop.publish(Float64(x))
        smallBase.publish(Float64(x))

        rospy.sleep(5)

    print "done !"
