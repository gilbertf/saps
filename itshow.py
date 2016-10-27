#!/usr/bin/env python3
import os
from itpp import itload
import sys
import numpy as np
import scipy.io

def ShowSyntax():
    print("Syntax: itshow.py <NameFile> (-l) (-sVarName)")
    print("   -l           List all variable names")
    print("   -sVarName    Show value of variable VarName")
    print("   -eVarName    Export value of variable VarName to export.mat")
    print("   -fFileName   Export filename")
    exit()

#np.set_printoptions(threshold=np.nan)

ShowNames = True
ShowValues = True
ExportValues = True
NameFile = None
NameFilter = []
ExportFilter = []
ExportTxtFilter = []
ExportFilename = "export.mat"

Args = sys.argv

for Arg in Args[1:]:
    if Arg == "-l":
        ShowValues = False
    elif Arg.startswith("-s"):
        VarName = Arg[2:]
        if len(VarName) == 0:
            print("Invalid variable name")
            ShowSyntax()
        else:
            NameFilter.append(Arg[2:])
    elif Arg.startswith("-e"):
        VarName = Arg[2:]
        if len(VarName) == 0:
            print("Invalid variable name")
            ShowSyntax()
        else:
            ExportFilter.append(Arg[2:])
    elif Arg.startswith("-g"):
        VarName = Arg[2:]
        if len(VarName) == 0:
            print("Invalid variable name")
            ShowSyntax()
        else:
            ExportTxtFilter.append(Arg[2:])
    elif Arg.startswith("-f"):
        ExportFileName = Arg[2:]
        if len(ExportFileName) == 0:
            print("Invalid export filename")
            ShowSyntax()
    else:
        if NameFile == None:
            NameFile = Arg
            if not os.path.isfile(NameFile):
                print(NameFile, "is no file. Please specify exactly one filename.")
                ShowSyntax()
        else:
            print("Invalid command: " + Arg)
            ShowSyntax()
         
if NameFile == None:
    ShowSyntax()
    
Data = itload(NameFile)
if Data == "defekt":
    print("Invalid itpp data file. STOP!")
    exit()

for d in Data:
    if NameFilter == [] or d in NameFilter:
        print(d)
        if ShowValues:
            print(Data[d])
            print()
    if d in ExportFilter:
        scipy.io.savemat(ExportFileName, mdict={d : Data[d]})
    if d in ExportTxtFilter:
        f = open(ExportFileName, 'w')
        print(type(Data[d]))
        for l in list(Data[d]):
            f.write(str(l), "\n")
        f.close()
