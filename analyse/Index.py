Len = len(ValuesIn[0])
for v in ValuesIn[1:]:
    if Len != len(v):
        Msg.Error(3, "Not all vectors are of equal length")
ValuesOut = [[i for i in range(Len)]]
