import os

try:
    DirResults = Options.Config["FilesystemITPP"]["DirResults"]
except:
    Error(1, "FilesystemITPP -> DirResults has to be defined in config file.")
DirResults = os.path.expanduser(DirResults)

for Args in ListArgs:
    Cmd = " ".join([Program] + ["DirResults=" + DirResults] + Args)
    print("Running: ", Cmd)
    os.system(Cmd)