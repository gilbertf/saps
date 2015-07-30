import numpy as np

ValuesOut = list()


StepLen = Analyse["StepLen"]
try:
    Axis = Analyse["Axis"]
except:
    Axis = 0
    
NumSteps = int(len(ValuesIn[0])/StepLen)
if NumSteps != len(ValuesIn[0])/StepLen:
    Msg.Error(2, "Rounding, thats bad. Len" + str(len(ValuesIn[0])))

#V = np.reshape(ValuesIn, [StepLen, NumSteps])
V = np.reshape(ValuesIn, [NumSteps, StepLen])

W = np.mean(V, axis=Axis)

ValuesOut = [W]

