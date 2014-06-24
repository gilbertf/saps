import numpy
import scipy.integrate

ValuesOut = list()


StepLen = Analyse["StepLen"]
NumSteps = int(numpy.floor(len(ValuesIn[0])/StepLen))
if NumSteps != len(ValuesIn[0])/StepLen:
    Msg.Error(2, "Rounding " + str(len(ValuesIn[0])/StepLen) + " to " + str(NumSteps) + ", thats bad")

if len(ValuesIn) == 1:
    for s in range(NumSteps):
        ValuesOut.append(numpy.sum(ValuesIn[0][s*StepLen:(s+1)*StepLen])/StepLen)
    if Options.DebugAnalyse:
        print(Options.Indent, "Sum integral of", AxisIn[0], "with equal stepsize assumed:", ValuesOut)
else:
    print("We expect one input variables")

ValuesOut = [ValuesOut]
#print("Out",ValuesOut)
#print("In", ValuesIn)

