import os

try:
    DebugSimulate = Options.Config["Saps"]["DebugSimulate"]
except:
    DebugSimulate = None

for Cmd in ListCmd:
    if DebugSimulate:
        print("Simulate: ", Cmd)
    ret = os.system(Cmd)
    if ret != 0:
        Msg.Error(1, "Simulation cmd failed. Stopping here! Last command:\n\t\t" + Cmd)
