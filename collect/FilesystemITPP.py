from itpp import itload
import numpy
import os

try:
    DirResults = Options.Config["FilesystemITPP"]["DirResults"]
except:
    Msg.Error(1, "FilesystemITPP -> DirResults has to be defined in config file.")
DirResults = os.path.expanduser(DirResults)

try:
    StopOnDefectSetFiles = Options.Config["FilesystemITPP"]["StopOnDefectSetFiles"]
except:
    StopOnDefectSetFiles = False
    
NumDefectResultsFiles = 0
NumCompleteResultsFiles = 0
NumResultsFiles = len(ListArgs)

DebugCollect = False

val = []
for i in range(NumAxis):
    val.append([])
for Args in ListArgs:
    NameFileResult = "_".join(Args)
    NameFileResult = DirResults + "/" + (Program.split("/")).pop() + "/" + NameFileResult
    if DebugCollect:
        print("NameFileResult: " + NameFileResult)
    r = itload(NameFileResult)
    import numbers
    if r == "" or r == "defekt":
        NumDefectResultsFiles = NumDefectResultsFiles + 1
        Warning(2, "Defect results file " + NameFileResult)
        continue
    try:
        Complete = r["Complete"]
    except:
        Warning(2, "The Complete variable can not be found in the results file")
        continue
    if not isinstance(Complete, numbers.Number):
        Complete = float(Complete)
    if Complete == -1:
        Msg.Notice(2, "The Complete variable is not updated by your program")
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

Msg.Msg(2, "Collect:", str(NumCompleteResultsFiles) + "/" + str(NumResultsFiles) + " complete, " + str(NumDefectResultsFiles) + " defect")
if NumDefectResultsFiles > 0:
    if StopOnDefectSetFiles is True:
        Msg.Error(2, "Not all set files could be read.")

Values = val
