import math as m
import numpy as np

ValuesOut = [[]]

if len(ValuesIn) == 2:
    Cnt = 0
    if "Operator" in Analyse:
        if Analyse["Operator"] is "/":
            ValuesOut[0] = np.divide(ValuesIn[0], ValuesIn[1])
        elif Analyse["Operator"] is "+":
            ValuesOut[0] = np.add(ValuesIn[0], ValuesIn[1])
        elif Analyse["Operator"] == "subtract":
            ValuesOut[0] = np.subtract(ValuesIn[0], ValuesIn[1])
        else:
            Msg.Error(2, "Invalid operator ", Analyse["Operator"])

    else:
        Msg.Error(2, "Please specify one mathematical operatior using Operator:")
else:
    Msg.Error(2, "We expect two input variables")
