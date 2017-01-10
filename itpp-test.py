#!/usr/bin/env python3

import numpy as np

from itpp import *


A = np.zeros((10,2))

A[7,1] = 5
A[2,1] = 5
A[3,0] = 2

print(A)
print("")

d = dict()
d["A"] = A
itsave("test.it", d)

X = itload("test.it")
print(X)
print(X["A"])
