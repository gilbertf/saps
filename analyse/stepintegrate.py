import numpy
import scipy.integrate

ValuesOut = list()

try:
    Len = Analyse["Len"]
    NumSteps = int(len(ValuesIn[0])/Len)
    if NumSteps != len(ValuesIn[0])/Len:
        Msg.Error(2, "Rounding, thats bad")
except:
    NumSteps = 1
    Len = len(ValuesIn[0])
if len(ValuesIn) == 1:
    for s in range(NumSteps):
        ValuesOut.append(numpy.trapz(ValuesIn[0][s*Len:(s+1)*Len]))
    if Options.DebugAnalyse:
        print(Options.Indent, "Trapz integral of", AxisIn[0], "with equal stepsize assumed:", ValuesOut)
elif len(ValuesIn) == 2:
    for s in range(NumSteps):
        ValuesOut.append(numpy.trapz(ValuesIn[0][s*Len:(s+1)*Len], ValuesIn[1][s*Len:(s+1)*Len]))
    if Options.DebugAnalyse:
        print(Options.Indent, "Trapz integral of", AxisIn[0], "with steps", AxisIn[1], ":", ValuesOut)
else:
    print("We expect one or two input variables")
print(ValuesOut)
ValuesOut = [ValuesOut]

