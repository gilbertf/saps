#Extract value at position "Index" of AxisIn and save to AxisOut
ValuesOut = list()

for RowValues in ValuesIn:
    NewRow = RowValues[int(Analyse["First"]):int(Analyse["Last"])]
    ValuesOut.append(NewRow)
