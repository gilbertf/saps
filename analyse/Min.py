import numpy as np

try:
    Axis = Analyse["Axis"]
except:
    Axis = 0
    
if len(ValuesIn) == 1:
    ValuesOut = [[]]
    ValuesOut = np.min(ValuesIn, axis = Axis)
    ValuesOut = [ValuesOut.tolist()]
else:
    Msg.Error(2, "We expect one input variables")