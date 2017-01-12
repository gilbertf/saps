import numpy as np

ValuesOut = [[]]

try:
    Axis = Analyse["Axis"]
except:
    Axis = 0
    
if len(ValuesIn) == 1:
    ValuesOut = [[]]
    Max = 1
    if "Max" in Analyse:
        Max = float(Analyse["Max"])
    ValuesOut[0] = np.array(ValuesIn[0]) / (np.max(ValuesIn[0]) / Max)
else:
    Msg.Error(2, "We expect one input variables")
