#!/usr/bin/env python3
import os
from itpp import itload
import sys
import numpy as np
import scipy.io

def ShowSyntax():
    print("Syntax: itshow.py <NameFile> (-l) (-a) (-sVarName)")
    print("   -l           List all variable names")
    print("   -a           Print full arrays")
    print("   -sVarName    Show value of variable VarName")
    print("   -eVarName    Export value of variable VarName in matlab format")
    print("   -gVarName    Export value of variable VarName in text format")
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
    elif Arg == "-a":
        np.set_printoptions(threshold=np.nan)
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
        if not ShowValues:
            print(d)
        else:
            print(d, " (", str(type(Data[d])), ")", str(np.shape(Data[d])))
            print(Data[d])
            print()
    if d in ExportFilter:
        scipy.io.savemat(ExportFileName, mdict={d : Data[d]})
    if d in ExportTxtFilter:
        np.savetxt(ExportFileName, Data[d])
