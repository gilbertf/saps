import os
import random

def WriteJobfile(Cmd, DirJob, NameJob):
    fn_jobfile = os.path.join(os.path.expanduser(DirJob), NameJob)
    if os.path.isfile(fn_jobfile):
        return(0)
    try:
        jobfile = open(fn_jobfile, 'w')
        jobfile.write(Cmd)
        jobfile.close()
    except:
        Error(2, "Could not write jobfile", fn_jobfile)
    return(1)

try:
    DirJob = Config["FilesystemCluster"]["DirJob"]
except:
    Error(1, "FilesystemCluster -> DirJob has to be defined in config file.")

try:
    os.makedirs(DirJob)
except:
    None
    
NumCreated = 0
for Args in ListArgs:
    NameJob = " ".join(Args)
    Cmd = " ".join([Program] + Args)
    NumCreated = NumCreated + WriteJobfile(Cmd, DirJob, NameJob)
    
print(Indent, "Simulating:", str(NumCreated) + "/" + str(len(ListArgs)) + " new jobfiles created.")
