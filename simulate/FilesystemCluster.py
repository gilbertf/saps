import os
import random
from saps import ArgsToStr

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
        Msg.Error(2, "Could not write jobfile " + NameFileJob)
    return(1)

try:
    DirJob = Options.Config["FilesystemCluster"]["DirJob"]
except:
    Msg.Error(1, "FilesystemCluster -> DirJob has to be defined in configfile.")

try:
    DirJob = os.path.expanduser(DirJob)
    os.makedirs(DirJob)
except:
    None

NumCreated = 0
for Pos, Cmd in enumerate(ListCmd):
    NameFileJob = ArgsToStr(ListArgs[Pos])
    NumCreated = NumCreated + WriteJobfile(Cmd, DirJob, NameFileJob)
    
Msg.Msg(1, "Simulating", str(NumCreated) + "/" + str(len(ListArgs)) + " new jobfiles created.")
