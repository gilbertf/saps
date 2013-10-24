ValuesOut = list()

try:
    Len = Analyse["Len"]
    NumSteps = int(len(ValuesIn[0])/Len)
    if NumSteps != len(ValuesIn[0])/Len:
        Msg.Error(2, "Rounding, thats bad")
except:
    NumSteps = 1
    Len = len(ValuesIn[0])
    
if len(ValuesIn) == 1:
    for s in range(NumSteps):
        ValuesOut.append(sum(ValuesIn[0][s*Len:(s+1)*Len]))
else:
    print("We expect one variables")

ValuesOut = [ValuesOut]

