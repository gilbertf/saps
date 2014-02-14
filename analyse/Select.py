#Extract value at position "Index" of AxisIn and save to AxisOut
ValuesOut = list()

if len(AxisOut) != 1:
    Msg.Error(3, "Number of output axis has to be one, when using select")

for RowValues in ValuesIn:
    NewRow = list()
    Index = Analyse["Index"]
    if Index != round(Index):
        Msg.Error(3, "Index has to be a non negative natural number")
        Index = int(Index)
    if Index > len(RowValues)-1:
        Msg.Error(3, "Index out of range")
    NewRow.append(RowValues[int(Analyse["Index"])])
    ValuesOut.append(NewRow)
