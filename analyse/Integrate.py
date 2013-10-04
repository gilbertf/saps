import numpy
import scipy.integrate
    
if len(Values) == 1:
    print(Options.Indent, "Trapz integral of", Axis[0], "with equal stepsize assumed:", numpy.trapz(Values[0]))
elif len(Values) == 2:
    print(Options.Indent, "Trapz integral of", Axis[0] + ":", numpy.trapz(Values[0], Values[1]))
else:
    print("We expect one or two input variables")
