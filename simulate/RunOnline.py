import os

try:
    DebugSimulate = Options.Config["Saps"]["DebugSimulate"]
except:
    DebugSimulate = None

for Cmd in ListCmd:
    if DebugSimulate:
        print("Simulate: ", Cmd)
    os.system(Cmd)
