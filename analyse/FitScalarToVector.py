def Extend(Scalar, Vector):
    Factor = int(len(Vector) / len(Scalar))
    if len(Scalar)*Factor != len(Vector):
        Msg.Error(3, "Length of both axis is not a multiple")

    Out = []
    for e in Scalar:
        Out.extend([e]*Factor)

    return Out


if len(AxisIn) != 2:
    Msg.Error(3, "Expecting two input axis")

Len0 = len(ValuesIn[0])
Len1 = len(ValuesIn[1])

if Len0 == Len1:
    Msg.Error(3, "Both Axis are of the same length already")

ValuesOut = []
if Len0 > Len1:
    ValuesOut.append(ValuesIn[0])
    ValuesOut.append(Extend(ValuesIn[1], ValuesIn[0]))
else:
    ValuesOut.append(Extend(ValuesIn[0], ValuesIn[1]))
    ValuesOut.append(ValuesIn[1])
