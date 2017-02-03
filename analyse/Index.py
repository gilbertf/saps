Len = len(ValuesIn[0])
for v in ValuesIn[1:]:
    if Len != len(v):
        Msg.Error(3, "Not all vectors are of equal length")

if Len == 0:
        Msg.Error(3, "Empty vector")

if "Start" in Analyse:
    if "Stop" in Analyse:
        Start = float(Analyse["Start"])
        Stop = float(Analyse["Stop"])

        Step = (Stop - Start) / (Len - 1)
        ValuesOut = [[ (i * Step) + Start for i in range(Len) ]]
    else:
        Msg.Error(3, "Stop is missing")
else:
    ValuesOut = [[i for i in range(Len)]]

if "Stop" in Analyse and not "Start" in Analyse:
    Msg.Error(3, "Start is missing")
