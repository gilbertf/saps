#!/usr/bin/env python3
import os
from itpp import itload
import sys

def ShowSyntax():
    print("Syntax: itshow.py <NameFile> (-l) (-sVarName)")
    print("   -l           List all variable names")
    print("   -sVarName    Show value of variable VarName")
    exit()
    
ShowNames = True
ShowValues = True
NameFile = None
NameFilter = []

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
for d in Data:
    if NameFilter == [] or d in NameFilter:
        print(d)
        if ShowValues:
            print(Data[d])
            print("")
