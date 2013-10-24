ValuesOut = list()

if len(AxisOut) != 1:
    Msg.Error(3, "Number of output axis has to be one, when using Integrate")

for RowValues in ValuesIn:
    NewRow = list()
    for Idx in range(int(Analyse["First"]), len(RowValues), Analyse["Repeat"]):
        for j in range(int(Analyse["Last"])-int(Analyse["First"])+1):
            p = Idx+j
            #print(p)
            NewRow.append(RowValues[p])
    ValuesOut.append(NewRow)
