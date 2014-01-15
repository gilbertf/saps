#Extract value at position "Index" of AxisIn and save to AxisOut
ValuesOut = list()

if len(AxisOut) != 1:
    Msg.Error(3, "Number of output axis has to be one, when using select")

for RowValues in ValuesIn:
    NewRow = list()
    NewRow.append(RowValues[int(Analyse["Index"])])
    ValuesOut.append(NewRow)
