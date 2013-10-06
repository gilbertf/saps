import numpy
import scipy.integrate

ValuesOut = list()
if len(ValuesIn) == 1:
    ValuesOut = numpy.trapz(ValuesIn[0])
    if Options.DebugAnalyse:
        print(Options.Indent, "Trapz integral of", AxisIn[0], "with equal stepsize assumed:", ValuesOut)
elif len(ValuesIn) == 2:
    ValuesOut = numpy.trapz(ValuesIn[0], ValuesIn[1])
    if Options.DebugAnalyse:
        print(Options.Indent, "Trapz integral of", AxisIn[0], "with steps", AxisIn[1], ":", ValuesOut)
else:
    print("We expect one or two input variables")
    
ValuesOut = [[float(ValuesOut)]]

