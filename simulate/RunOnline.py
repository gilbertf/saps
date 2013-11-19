import os

try:
    DirResults = Options.Config["FilesystemITPP"]["DirResults"]
except:
    Error(1, "FilesystemITPP -> DirResults has to be defined in config file.")
DirResults = os.path.expanduser(DirResults)

for Args in ListArgs:
    Executable = Program.split("/").pop()
    NameFileResult = os.path.join(DirResults, Executable, "_".join(Args))
    if os.path.isfile(NameFileResult):
        Msg.Notice(2, "Result file exists already, skipping job.")
        continue
    NameFileJob = Executable + "_".join(Args)
    Cmd = " ".join([Program] + ["NameFileResult=" + NameFileResult] + Args)
    print("Running: ", Cmd)
    os.system(Cmd)
