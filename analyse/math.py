ValuesOut = [[]]

if len(ValuesIn) == 1:
    for v in ValuesIn[0]:
        if "Multiply" in Analyse:
            ValuesOut[0].append(v*Analyse["Multiply"])
        elif "Add" in Analyse:
            ValuesOut[0].append(v+Analyse["Add"])
        else:
            Msg.Error(2, "Please specify one mathematical operation")
else:
    Msg.Error(2, "We expect one input variables")
