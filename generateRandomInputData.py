#!/usr/bin/env python

import os
from random import randrange

if __name__ == "__main__":
    f = open('inputdata.txt','w')

    iStart = 1
    iEnd   = 100 # nr of lines in file
    while iStart <= iEnd:
        X01 = randrange(90)
        X02 = randrange(90)
        X03 = randrange(90)
        X04 = randrange(90)
        X05 = randrange(90)
        X06 = randrange(90)
        X07 = randrange(90)
        X08 = randrange(90)
        X09 = randrange(90)
        X10 = randrange(90)
        X11 = randrange(90)
        f.write(`X01` +" "+ `X02`  +" "+ `X03` +" ")
        f.write(`X04` +" "+ `X05`  +" ")
        f.write(`X06` +" "+ `X07`  +" ")
        f.write(`X08` +" "+ `X09`  +" ")
        f.write(`X10` +" "+ `X11`  +"\n")
 
        iStart = iStart + 1

    f.close()

