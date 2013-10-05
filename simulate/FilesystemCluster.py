import os
import random

try:
    DirResults = Options.Config["FilesystemITPP"]["DirResults"]
except:
    Error(1, "FilesystemITPP -> DirResults has to be defined in config file.")
DirResults = os.path.expanduser(DirResults)

def WriteJobfile(Cmd, DirJob, NameFileJob):
    NameFileJob = os.path.join(os.path.expanduser(DirJob), NameFileJob)
    if os.path.isfile(NameFileJob):
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
for Args in ListArgs:
    NameFileJob = "_".join(Args)
    DirResults = DirResults + "/" + (Program.split("/")).pop()
    Cmd = " ".join([Program] + ["DirResults=" + DirResults] + Args)
    NumCreated = NumCreated + WriteJobfile(Cmd, DirJob, NameFileJob)
    
print(Options.Indent, "Simulating:", str(NumCreated) + "/" + str(len(ListArgs)) + " new jobfiles created.")
