import numpy as np

if len(ValuesIn) == 1:
    ValuesOut = [[]]
    ValuesOut = np.mean(ValuesIn, axis = 0)
    ValuesOut = [ValuesOut.tolist()]
else:
    Msg.Error(2, "We expect one input variables")