from itpp import itload
import numpy as np
import os
from saps import ConstructNameFileResult
from saps import ArgsToStr
from colorama import Fore

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
    ArgsStr = ArgsToStr(Args)
    NameFileResult = ConstructNameFileResult(DirResults, Program, ArgsStr)
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
    if round(Complete, Options.RoundDigits) > 0.99:
        NumCompleteResultsFiles = NumCompleteResultsFiles + 1
        
        for i, a in enumerate(Axis):
            BracketOpen = "["
            BracketClose = "]"
            NumBracketsOpen = a.count(BracketOpen)
            NumBracketsClose = a.count(BracketClose)
            SplitArrayIdx = None
            
            if NumBracketsOpen == 1 and NumBracketsClose == 1:
                ArrayIdx = a[a.find(BracketOpen)+1:a.find(BracketClose)]
                Msg.Notice(2, "Array index: " + ArrayIdx)
                #if not "#" in ArrayIdx:
                #    Msg.Error(2, "Seperator for array indexing required in " + ArrayIdx)
                SplitArrayIdx = ArrayIdx.split("#")
                if len(SplitArrayIdx) == 1 or len(SplitArrayIdx) == 2:
                    for Idx in range(len(SplitArrayIdx)):
                        if SplitArrayIdx[Idx] == "":
                            SplitArrayIdx[Idx] = -1
                        else:
                            try:
                                SplitArrayIdx[Idx] = int(SplitArrayIdx[Idx])  
                            except:
                                Msg.Error(2, "Invalid indexing with: " + str(ArrayIdx))
                else:
                    Msg.Error(2, "Invalid index: " + ArrayIdx)

                a = a[:a.find(BracketOpen)]
            elif NumBracketsOpen == 0 and NumBracketsClose == 0:
                Msg.Notice(2, "No indexing specified")
            else:
                Msg.Error(2, "Invalid indexing brackets in " + a)

            try:
                x = r[a]
            except:
                Msg.Error(2, "Axis " + a + " does not exist in results file! Valid are: " + ", ".join(r))

            if SplitArrayIdx is None:
                if np.isscalar(x):
                    val[i].append(float(x))
                #elif type(x) is np.matrix:
                #    Msg.Error(2, "Matrix is not supported without using indexing brackets")
                else:
                    if len(x) == 0: #For example if calculation is still running
                        x = [-1]
                    for v in x:
                        val[i].append(float(v))
            else:
                if np.isscalar(x):
                    Msg.Error(2, "Scalars can not be indexed")
                elif type(x) is np.matrix:
                    if len(SplitArrayIdx) == 2:
                        if SplitArrayIdx[0] == -1 and SplitArrayIdx[1] != -1:
                            x = x[:, SplitArrayIdx[1]]
                        elif SplitArrayIdx[0] != -1 and SplitArrayIdx[1] == -1:
                            x = x[SplitArrayIdx[0], :].T
                        elif SplitArrayIdx[0] != -1 and SplitArrayIdx[1] != -1:
                            x = [ x[SplitArrayIdx[0],SplitArrayIdx[1]] ]
                        else:
                            Msg.Error(2, "Invalid indexing format " + ArrayIdx)
                        if len(x) == 0: #For example if calculation is still running
                            x = [-1]
                        for v in x:
                            val[i].append(float(v))
                    else:
                        Msg.Error(2, "Invalid indices count for matrix indexing")
                else:
                    if len(SplitArrayIdx) == 1:
                        val[i].append(float(x[SplitArrayIdx[0]]))
                    else:
                        Msg.Error(2, "Indexing failed")

    else:
        msg = str(Complete*100) + " % complete, estimating " + ReadableTime((1-Complete)*Duration) + " min further to wait for " + ArgsStr
        print("Compl", Complete)
        if StopOnIncompleteResultFiles:
            Msg.Error(2, msg)
        else:
            Msg.Warning(2, msg)


str_missing = str(NumMissingResultFiles)
if NumMissingResultFiles > 0:
    str_missing = Fore.RED + str_missing + " missing" + Fore.RESET
    
Msg.Msg(2, "Collect:", str(NumCompleteResultsFiles) + "/" + str(NumResultsFiles) + " complete, " + str_missing + " and " + str(NumDefectResultsFiles) + " defect.")
if NumDefectResultsFiles > 0:
    msg = "Not all set files could be read."
    if StopOnDefectResultFiles:
        Msg.Error(2, msg)
    else:
        Msg.Warning(2, msg)
Values = val
