import numpy as np

ValuesOut = list()
if len(ValuesIn) == 1:
    
    try:
        NumBins = Analyse["NumBins"]
    except:
        NumBins = 100
        
    try:
        Min = Analyse["Min"]
        Max = Analyse["Max"]
        Range = (Min, Max)
    except:
        Range = None
        
    x = np.histogram(ValuesIn[0], bins=NumBins, range=Range)
    a = x[0]
    b = x[1]
else:
    print("We expect one input variables")
    
b = b + (b[1]-b[0])*0.5 #Middle instead of edges
ValuesOut = [a, b[0:len(b)-1]]