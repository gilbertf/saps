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
    
NumMissingResultFiles = 0
NumDefectResultsFiles = 0
NumCompleteResultsFiles = 0
NumResultsFiles = len(ListArgs)

DebugCollect = Options.DebugCollect

import math
def ReadableTime(s):
    Seconds = math.floor(s % 60)
    m = math.floor(s/60)
    Minutes = m % 60
    h = math.floor(m/60)
    Hours = h % 24
    Days = math.floor(h/24)
    if Days == 0:
        ret = str(Hours) + "h " + str(Minutes) + "min " + str(Seconds) + "sec"
    else:
        ret = str(Days)+"d " + str(Hours) + "h " + str(Minutes) + "min " + str(Seconds) + "sec"
    return ret

val = []
for i in range(NumAxis):
    val.append([])
for Args in ListArgs:
    NameFileResult = os.path.join(DirResults, Program.split("/").pop(), "_".join(Args))
    if DebugCollect:
        print(Options.Indent*2 + "NameFileResult: " + NameFileResult)
    if not os.path.isfile(NameFileResult):
        NumMissingResultFiles = NumMissingResultFiles + 1
        Msg.Notice(2, "Missing result file " + NameFileResult)
        continue
    r = itload(NameFileResult)
    import numbers
    if r == "" or r == "defekt":
        NumDefectResultsFiles = NumDefectResultsFiles + 1
        Msg.Notice(2, "Defect result file " + NameFileResult)
        continue
    try:
        Duration = r["Duration"]
    except:
        Duration = 0

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
        msg = str(Complete*100) + " % complete, estimating " + ReadableTime((1-Complete)*Duration) + " min further to wait for " + "_".join(Args)
        if StopOnIncompleteResultFiles:
            Msg.Error(2, msg)
        else:
            Msg.Warning(2, msg)


Msg.Msg(2, "Collect:", str(NumCompleteResultsFiles) + "/" + str(NumResultsFiles) + " complete, " + str(NumMissingResultFiles) + " missing and " + str(NumDefectResultsFiles) + " defect.")
if NumDefectResultsFiles > 0:
    msg = "Not all set files could be read."
    if StopOnDefectResultFiles:
        Msg.Error(2, msg)
    else:
        Msg.Warning(2, msg)
Values = val
