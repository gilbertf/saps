import os
import random

try:
    DirResults = Options.Config["FilesystemITPP"]["DirResults"]
except:
    Msg.Error(1, "FilesystemITPP -> DirResults has to be defined in config file.")
DirResults = os.path.expanduser(DirResults)

def WriteJobfile(Cmd, DirJob, NameFileJob):
    NameFileJob = os.path.join(os.path.expanduser(DirJob), NameFileJob)
    if os.path.isfile(NameFileJob):
        Msg.Notice(2, "Job file was created before, skipping.")
        return(0)
    try:
        FileJob = open(NameFileJob, 'w')
        FileJob.write(Cmd)
        FileJob.close()
    except:
        Msg.Error(2, "Could not write jobfile", NameFileJob)
    return(1)

try:
    DirJob = Options.Config["FilesystemCluster"]["DirJob"]
except:
    Msg.Error(1, "FilesystemCluster -> DirJob has to be defined in configfile.")

try:
    os.makedirs(DirJob)
except:
    None

NumCreated = 0
DirResults = DirResults + "/" + (Program.split("/")).pop()
for Args in ListArgs:
    NameFileResult = DirResults + "/" + "_".join(Args)
    if os.path.isfile(NameFileResult):
        Msg.Notice(2, "Result file exists already, skipping job.")
        continue
    NameFileJob = "_".join(Args)
    Cmd = " ".join([Program] + ["DirResults=" + DirResults] + Args)
    NumCreated = NumCreated + WriteJobfile(Cmd, DirJob, NameFileJob)
    
Msg.Msg(1, "Simulating", str(NumCreated) + "/" + str(len(ListArgs)) + " new jobfiles created.")
