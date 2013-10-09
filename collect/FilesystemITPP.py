from itpp import itload
import numpy
import os

try:
    DirResults = Options.Config["FilesystemITPP"]["DirResults"]
except:
    Msg.Error(1, "FilesystemITPP -> DirResults has to be defined in config file.")
DirResults = os.path.expanduser(DirResults)

try:
    StopOnDefectResultFiles = Options.Config["FilesystemITPP"]["StopOnDefectResultFiles"]
except:
    StopOnDefectResultFiles = True
    
try:
    StopOnIncompleteResultFiles = Options.Config["FilesystemITPP"]["StopOnIncompleteResultFiles"]
except:
    StopOnIncompleteResultFiles = True
    
    
NumDefectResultsFiles = 0
NumCompleteResultsFiles = 0
NumResultsFiles = len(ListArgs)

DebugCollect = Options.DebugCollect

val = []
for i in range(NumAxis):
    val.append([])
for Args in ListArgs:
    NameFileResult = os.path.join(DirResults, Program.split("/").pop(), "_".join(Args))
    if DebugCollect:
        print("NameFileResult: " + NameFileResult)
    r = itload(NameFileResult)
    import numbers
    if r == "" or r == "defekt":
        NumDefectResultsFiles = NumDefectResultsFiles + 1
        Msg.Notice(2, "Defect result file " + NameFileResult)
        continue
    try:
        Complete = r["Complete"]
    except:
        Msg.Warning(2, "The Complete variable can not be found in the results file")
        continue
    if not isinstance(Complete, numbers.Number):
        Complete = float(Complete)
    if round(Complete, Options.RoundDigits) == 1:
        NumCompleteResultsFiles = NumCompleteResultsFiles + 1
        for i, a in enumerate(Axis):
            x = r[a]
            if isinstance(x, numbers.Number):
                val[i].append(float(x))
            else:
                if len(x) == 0: #For example if calculation is still running
                    x = [-1]
                for v in x:
                    val[i].append(float(v))
    else:
        if StopOnIncompleteResultFiles:
            Msg.Error(2, "Incomplete result file " + NameFileResult)
        else:
            Msg.Warning(2, "Incomplete result file " + NameFileResult)

Msg.Msg(2, "Collect:", str(NumCompleteResultsFiles) + "/" + str(NumResultsFiles) + " complete, " + str(NumDefectResultsFiles) + " defect")
if NumDefectResultsFiles > 0:
    if StopOnDefectResultFiles:
        Msg.Error(2, "Not all set files could be read.")
    else:
        Msg.Warning(2, "Not all set files could be read.")
Values = val
