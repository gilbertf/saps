import numpy as np

if len(ValuesIn) == 1:
    Thres = float(Analyse["Threshold"])
    ValuesOut = [[]]
    for v in ValuesIn[0]:
        if v > Thres:
            ValuesOut[0].append(1)
        else:
            ValuesOut[0].append(0)
else:
    Msg.Error(2, "We expect one input variables")