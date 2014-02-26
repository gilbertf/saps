ValuesOut = list()

if len(AxisOut) != 1:
    Msg.Error(3, "Number of output axis has to be one, when using slice")

for RowValues in ValuesIn:
    NewRow = list()
    for Idx in range(int(Analyse["First"]), len(RowValues), int(Analyse["Repeat"])):
        for j in range(int(Analyse["Last"])-int(Analyse["First"])+1):
            p = Idx+j
            NewRow.append(RowValues[p])
    ValuesOut.append(NewRow)
