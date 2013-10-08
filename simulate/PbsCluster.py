import os
import random

try:
    DirResults = Options.Config["FilesystemITPP"]["DirResults"]
except:
    Msg.Error(1, "FilesystemITPP -> DirResults has to be defined in config file.")
DirResults = os.path.expanduser(DirResults)

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
    os.makedirs(DirJob)
except:
    None

try:
    os.makedirs(os.path.join(DirLog, "out"))
    os.makedirs(os.path.join(DirLog, "err"))
except:
    None


def Cluster(Cmd, DirJob, NameFileJob):
    ClusterCmd = "echo \"" + Cmd + "\" | qsub -o " + os.path.join(DirLog, "out", NameFileJob) + " -e " + os.path.join(DirLog, "err", NameFileJob) + " -l select=1:ncpus=1"
    #Msg.Msg(2, "Cluster", ClusterCmd)
    os.system(ClusterCmd)
    return(1)


NumCreated = 0
DirResults = DirResults + "/" + (Program.split("/")).pop()
for Args in ListArgs:
    NameFileResult = DirResults + "/" + "_".join(Args)
    if os.path.isfile(NameFileResult):
        Msg.Notice(1, "Result file exists already, skipping job.")
        continue
    NameFileJob = "_".join(Args)
    Cmd = " ".join([Program] + ["DirResults=" + DirResults] + Args)
    NumCreated = NumCreated + Cluster(Cmd, DirJob, NameFileJob)
    
Msg.Msg(1, "Simulating", str(NumCreated) + "/" + str(len(ListArgs)) + " new jobs send to pbs.")
