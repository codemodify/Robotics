#!/usr/bin/env python

import os

if __name__ == "__main__":
    f = open('inputdata.txt','w')

    x = 0
    while x <= 90:
        X1 = x+1
        X2 = x+2
        X3 = x+3
        X4 = x+4
        f.write(`x`  +" "+ `x`  +" "+ `x` +" ")
        f.write(`X1` +" "+ `X1` +" ")
        f.write(`X2` +" "+ `X2` +" ")
        f.write(`X3` +" "+ `X3` +" ")
        f.write(`X4` +" "+ `X4` +"\n")
        x += 5

    f.close()

