#!/usr/bin/env python

import subprocess

if __name__ == "__main__":

	subprocess.call(["/opt/ros/fuerte/bin/rostopic", 
		"pub", 
		"/sh_ffj0_mixed_position_velocity_controller/command", 
		"std_msgs/Float64", 
		"0.5"])

