import os
for Args in ListArgs:
    Cmd = " ".join([Program] + Args)
    print("Running: ", Cmd)
    os.system(Cmd)