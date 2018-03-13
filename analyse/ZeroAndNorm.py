import numpy as np

try:
    Axis = Analyse["Axis"]
except:
    Axis = 0
    
if len(ValuesIn) == 1:
    ValuesIn = ValuesIn[0]
    ValuesOut = ValuesIn - np.min(ValuesIn, axis = Axis)
    ValuesOut = [ValuesOut / np.max(ValuesOut, axis = Axis)]
else:
    Msg.Error(2, "We expect one input variables")
