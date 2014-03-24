import numpy as np

if len(AxisOut) != 1:
    Msg.Error(3, "Number of output axis has to be one, when using numpy")

if len(AxisIn) != 1:
    Msg.Error(3, "Number of input axis has to be one, when using numpy")

Func = Analyse["Routine"]
ValuesOut = list()
for RowValues in ValuesIn:
    ValuesOut.append([eval('np.'+Func+'(RowValues)')])
#ValuesOut.append([np.mean([1,2,3,4])])
