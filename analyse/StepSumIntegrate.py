import numpy
import scipy.integrate

ValuesOut = list()

try:
    Len = Analyse["StepLen"]
    NumSteps = int(len(ValuesIn[0])/Len)
    if NumSteps != len(ValuesIn[0])/Len:
        Msg.Error(2, "Rounding, thats bad")
except:
    NumSteps = 1
    Len = len(ValuesIn[0])
if len(ValuesIn) == 1:
    for s in range(NumSteps):
        ValuesOut.append(numpy.sum(ValuesIn[0][s*Len:(s+1)*Len])/Len)
    if Options.DebugAnalyse:
        print(Options.Indent, "Sum integral of", AxisIn[0], "with equal stepsize assumed:", ValuesOut)
else:
    print("We expect one input variables")

ValuesOut = [ValuesOut]

