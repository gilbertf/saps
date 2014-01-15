#!/usr/bin/python
from itpp import itload
import sys

Cmd = sys.argv

if len(Cmd) == 2:
    Data = itload(Cmd[1])
    for d in Data:
        print d + ":"
        print Data[d]
        print ""
else:
    print "Syntax: " + Cmd[0] + " <filename>"
