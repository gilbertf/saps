#Desciption: Generates a index vector of the length of the input vector
#  AxisIn: A0, A1, A2, .. (one or more vectors of equal length)
#  AxisOut: Index
#  Example:
#    A0 = 5 2 7 2 8
#    Index = 1 2 3 4 5


Len = len(ValuesIn[0])
for v in ValuesIn[1:]:
    if Len != len(v):
        Msg.Error(3, "Not all vectors are of equal length")
ValuesOut = [[i for i in range(Len)]]
