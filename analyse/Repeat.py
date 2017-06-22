import numpy as np

try:
    Axis = Analyse["Axis"]
except:
    Axis = 0
    
try:
    OF = Analyse["OF"]
except:
    OF = 1

if len(ValuesIn) == 1:
    ValuesOut = [[]]
    ValuesOut = np.repeat(ValuesIn[0], OF, axis = Axis)
    ValuesOut = [ValuesOut.tolist()]
else:
    Msg.Error(2, "We expect one input variables")
