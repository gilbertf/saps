ValuesOut = [[]]

if len(ValuesIn) == 1:
    for v in ValuesIn[0]:
        Cnt = 0
        if "Multiply" in Analyse:
            ValuesOut[0].append(v*Analyse["Multiply"])
            Cnt = Cnt + 1
        if "Divide" in Analyse:
            ValuesOut[0].append(v/Analyse["Divide"])
            Cnt = Cnt + 1
        if "Add" in Analyse:
            ValuesOut[0].append(v+Analyse["Add"])
            Cnt = Cnt + 1
        if Cnt != 1:
            Msg.Error(2, "Please specify one mathematical operation")
else:
    Msg.Error(2, "We expect one input variables")
