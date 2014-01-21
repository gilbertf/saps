import os
import random
from saps import ArgsToStr

try:
    DirLog = Options.Config["PbsCluster"]["DirLog"]
except:
    Msg.Error(1, "PbsCluster -> DirLog has to be defined in config file.")
DirLog = os.path.expanduser(DirLog)

try:
    DirJob = Options.Config["PbsCluster"]["DirJob"]
except:
    Msg.Error(1, "PbsCluster -> DirJob has to be defined in configfile.")
DirJob = os.path.expanduser(DirJob)


try:
    Walltime = Options.Config["PbsCluster"]["Walltime"]
except:
    Walltime = None
    
try:
    DirWork = Options.Config["PbsCluster"]["DirWork"]
except:
    DirWork = None

try:
    Queue = Options.Config["PbsCluster"]["Queue"]
except:
    Queue = None
    
try:
    Resources = Options.Config["PbsCluster"]["Resources"]
except:
    Resources = None

try:
    os.makedirs(DirJob)
except:
    None

try:
    os.makedirs(os.path.join(DirLog, "out"))
    os.makedirs(os.path.join(DirLog, "err"))
except:
    None


def Cluster(Cmd, DirJob, NameFileJob):
    Options = list()
    #Options.append("-o " + os.path.join(DirLog, "out", NameFileJob))
    #Options.append("-e " + os.path.join(DirLog, "err", NameFileJob))
    if Resources:
        Options.append("-l " + ":".join(Resources))
    if Queue:
        Options.append("-q " + Queue)
    if Walltime:
        if type(Walltime) is not str:
            Msg.Error(1, "Walltime has to be given as string")
        Options.append("-l walltime=" + Walltime)
    #Options.append("-N \"" + Cmd[0:13] + "\"")
    ClusterCmd = "echo \"" + Cmd.replace("\"","\\\"") + "\" | qsub " + " ".join(Options)
    if DirWork:
        ClusterCmd = "cd " + DirWork + ";" + ClusterCmd

    #Msg.Msg(2, "Cluster", ClusterCmd)
    ret = os.system(ClusterCmd)
    if ret != 0:
        Msg.Error(1, "qsub execution failed.")
    return(1)


NumCreated = 0
for Pos, Cmd in enumerate(ListCmd):
    if Cmd not in ListPrevCmd:
        NameFileJob = ArgsToStr(ListArgs[Pos])
        NumCreated = NumCreated + Cluster(Cmd, DirJob, NameFileJob)
        ListPrevCmd.append(Cmd)
    
Msg.Msg(1, "Simulating", str(NumCreated) + "/" + str(len(ListArgs)) + " new jobs send to pbs.")
