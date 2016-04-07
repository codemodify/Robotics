#!/usr/bin/env python

import rospy
import os
import time

from std_msgs.msg import Float64

if __name__ == "__main__":

    # { Setup pipes }
    pipename01 = "thumbTopPipe"
    pipename02 = "thumbMiddlePipe"
    pipename03 = "thumbBasePipe"

    pipename04 = "pointerTopPipe"
    pipename05 = "pointerBasePipe"

    pipename06 = "middleTopPipe"
    pipename07 = "middleBasePipe"

    pipename08 = "ringTopPipe"
    pipename09 = "ringBasePipe"

    pipename10 = "smallTopPipe"
    pipename11 = "smallBasePipe"

    os.remove(pipename01) if os.path.exists(pipename01) else None
    os.remove(pipename02) if os.path.exists(pipename02) else None
    os.remove(pipename03) if os.path.exists(pipename03) else None
    os.remove(pipename04) if os.path.exists(pipename04) else None
    os.remove(pipename05) if os.path.exists(pipename05) else None
    os.remove(pipename06) if os.path.exists(pipename06) else None
    os.remove(pipename07) if os.path.exists(pipename07) else None
    os.remove(pipename08) if os.path.exists(pipename08) else None
    os.remove(pipename09) if os.path.exists(pipename09) else None
    os.remove(pipename10) if os.path.exists(pipename10) else None
    os.remove(pipename11) if os.path.exists(pipename11) else None

    os.mkfifo(pipename01)
    os.mkfifo(pipename02)
    os.mkfifo(pipename03)
    os.mkfifo(pipename04)
    os.mkfifo(pipename05)
    os.mkfifo(pipename06)
    os.mkfifo(pipename07)
    os.mkfifo(pipename08)
    os.mkfifo(pipename09)
    os.mkfifo(pipename10)
    os.mkfifo(pipename11)

    # { write to pipes }
    raw_input("Press [Enter] to send data")

    inputdata = open( "inputdata.txt", "r" )
    for line in inputdata:

        # { Format: Thumb -> Small : a a a b b c c d d e e }
        degrees = line.rstrip('\n').split(" ")

        ###### { Uncoment for debug }
        ######print(degrees)

        thumbTopPipe    = open(pipename01, 'w')
        thumbMiddlePipe = open(pipename02, 'w')
        thumbBasePipe   = open(pipename03, 'w')

        pointerTopPipe  = open(pipename04, 'w')
        pointerBasePipe = open(pipename05, 'w')

        middleTopPipe   = open(pipename06, 'w')
        middleBasePipe  = open(pipename07, 'w')

        ringTopPipe     = open(pipename08, 'w')
        ringBasePipe    = open(pipename09, 'w')

        smallTopPipe    = open(pipename10, 'w')
        smallBasePipe   = open(pipename11, 'w')

        thumbTopPipe.write(str(degrees[0]))
        thumbMiddlePipe.write(str(degrees[1]))
        thumbBasePipe.write(str(degrees[2]))

        pointerTopPipe.write(str(degrees[3]))
        pointerBasePipe.write(str(degrees[4]))

        middleTopPipe.write(str(degrees[5]))
        middleBasePipe.write(str(degrees[6]))

        ringTopPipe.write(str(degrees[7]))
        ringBasePipe.write(str(degrees[8]))

        smallTopPipe.write(str(degrees[9]))
        smallBasePipe.write(str(degrees[10]))

        thumbTopPipe.close()
        thumbMiddlePipe.close()
        thumbBasePipe.close()

        pointerTopPipe.close()
        pointerBasePipe.close()

        middleTopPipe.close()
        middleBasePipe.close()

        ringTopPipe.close()
        ringBasePipe.close()

        smallTopPipe.close()
        smallBasePipe.close()

        time.sleep(5)

    inputdata.close()

