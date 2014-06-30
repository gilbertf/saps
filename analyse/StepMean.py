import numpy as np

ValuesOut = list()


StepLen = Analyse["StepLen"]
NumSteps = int(len(ValuesIn[0])/StepLen)
if NumSteps != len(ValuesIn[0])/StepLen:
    Msg.Error(2, "Rounding, thats bad")

#V = np.reshape(ValuesIn, [StepLen, NumSteps])
V = np.reshape(ValuesIn, [NumSteps, StepLen])


W = np.mean(V, axis=0)

ValuesOut = [W]

