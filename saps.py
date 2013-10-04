#!/usr/bin/python3
import OrderedYaml
import yaml
import os
import sys
import random
import math
import Helper
from Helper import *

class Options():
    Descriptionfile = None
    Config = None
    
    #Actions
    Simulate = False
    Collect = False
    View = False
    Plot = False
    ydict = dict

def ConstructFullPath(NameFile, DirSaps):
    if DirSaps:
        CompleteNameFile = os.path.join(os.path.split(__file__)[0], NameFile)
    else:
        CompleteNameFile = NameFile
    return CompleteNameFile

def ReadYaml(NameFile, DirSaps):        
    CompleteNameFile = os.path.expanduser(ConstructFullPath(NameFile, DirSaps))
    try:
        CompleteFile = open(CompleteNameFile, 'r')
        data = CompleteFile.read()
        CompleteFile.close()
        Tree = yaml.load(data)
        return(Tree)
    except:
        Error(0, "Unable to read yaml file " + CompleteNameFile)

    
def RunFileCode(NameFile, DirSaps, Env):
    CompleteNameFile = ConstructFullPath(NameFile, DirSaps)
    try:
        File = open(CompleteNameFile)
        Code = File.read()
        File.close()
    except:
        Error(0, "Unable to read python file " + CompleteNameFile)
    exec(Code, Env)
    
def Num2Str(i):
    try:
        i = round(float(i), Helper.RoundDigits)
    except:
        None
    return(i)
    
def ParseFloatRange(s):
    def FloatRange(start, stop , inc = 1.):
        if stop < start:
            start, stop = stop, start
        delta = stop-start
        cnt = math.ceil((delta/inc)+1)
        l = list()
        for i in range(0,int(cnt)):
            l.append(Num2Str(start + i*inc))
        return l
        
    ### ParseFloatRange ###
    l = list()
    for t in s.split('|'):
        u = t.split('..')
        if len(u) == 1:
            l = l + [ Num2Str(u[0]) ]
        elif len(u) == 2:
            l = l + FloatRange(float(u[0]),float(u[1]))
        elif len(u) == 3:
            l = l + FloatRange(float(u[0]),float(u[2]),float(u[1]))
        else:
            Error(2,"Syntax error in " + t)
    return l 

def RestructureTree(Tree, inFigure):
    Properties = Options.ydict()
    FiguresSets = Options.ydict()
    if type(Tree) == Options.ydict:
        #Seperate in two Groups: FigureSets and Properties. Move PlotSet into the Figures but not the Sets
        for t in Tree:
            if "Figure " in t or "Set " in t:
                FiguresSets[t] = Tree[t]
            elif t == "PlotSet":
                if inFigure:
                    FiguresSets[t] = Tree[t]
                else:
                    Properties[t] = Tree[t]
            else:
                Properties[t] = Tree[t]
        #Append all properties to all FigureSets
        for fs in FiguresSets:
            if "Figure " in fs or "Set " in fs:
                if type(FiguresSets[fs]) == Options.ydict:
                    for p in Properties:
                        if not p in FiguresSets[fs]:
                            FiguresSets[fs][p] = Properties[p]
                        else:
                            Warning(0, "More specific value " + str(FiguresSets[fs][p]) + " for " + p + " overwrites " + str(Properties[p]) + ".")
                    if "Figure " in fs:
                        inFigure = True
                    else:
                        inFigure = False
                    FiguresSets[fs] = RestructureTree(FiguresSets[fs], inFigure)
        if len(FiguresSets) == 0:
            return(Properties) # In der tiefsten Ebene gibt es nur noch properties
        else:
            return(FiguresSets)
            

    
def ProcessTree(Tree, NameFigure = "", PlotList = [], GnuplotOptions = []):
    def ExtractValues(s, DoExtract): #Always returns list of strs to make handling easier
        if type(s) == str and DoExtract:
            return(ParseFloatRange(s))
        else:
            return([Num2Str(s)])
            
    def ParseSet(Set, NameFigure, NameSet, PlotList):
        def ExpandSet(Set, ListArgs, cmd = []):
            if len(Set) > 0:
                s = Set[0]
                V = ExtractValues(s[1], True)
                for v in V:
                    reccmd = cmd[:] #one method to copy lists
                    reccmd.append(s[0] + "=" + str(v))
                    ExpandSet(Set[1:], ListArgs, reccmd)
            else:
                ListArgs.append(cmd)
                
        def SplitComma(s):
            return s.replace(", ",",").split(",")
            
        ### ParseSet ###
        for s in Set: #escaping of @ is necessary for malab scripts
            if type(Set[s]) is str:
                Set[s] = Set[s].replace("\\","")

        try:
            Program = os.path.expanduser(Set.pop("Program"))
        except:
            Error(2, "Program property is missing")

        try:
            Axis = SplitComma(Set.pop("Axis"))
            NumAxis = len(Axis)
        except:
            Error(2, "Axis property is missing")

        try:
            PlotOpt = Set.pop("PlotOpt")
        except:
            PlotOpt = None
            
        try:
            Analyse = Set.pop("Analyse")
            Analyse = SplitComma(Analyse)
        except:
            Analyse = None

        Set = list(Set.items())
        Set.sort()

        ListArgs = []
        ExpandSet(Set, ListArgs)

        if Options.Simulate:
            try:
                Simulate = Options.Config["Simulate"]
            except:
                Error(1,"Simulate interface is not defined in configfile")
            Env = dict(ListArgs=ListArgs, Program=Program, Config=Options.Config, Indent=Helper.Indent)
            RunFileCode(os.path.join("Simulate", Simulate), True, Env)
            
        if Options.Collect or Options.View or Options.Plot:
            NameSetFile = Options.SetDir + "/" + NameFigure + "/" + NameSet

        if Options.Collect:
            try:
                Collect = Options.Config["Collect"]
            except:
                Error(1,"Collect interface is not defined in configfile")
            Env = dict(ListArgs=ListArgs, NameSetFile=NameSetFile, Axis = Axis, NumAxis=NumAxis, Program=Program, Config=Options.Config, Indent=Helper.Indent)
            RunFileCode(os.path.join("Collect", Collect), True, Env)
            try:
                Values = Env["Values"]
                Axis = Env["Axis"]
            except:
                Notice(2, "The collect module did not return a Values and Axis")
            
            if Analyse is not None:
                In = []
                AxisIn = []
                if len(Analyse) > 1:
                    ParamsPP = Analyse[1:]
                    for NameParam in ParamsPP:
                        try:
                            Idx = Axis.index(NameParam)
                        except:
                            Error(2, "The Analyse parameter " + NameParam + " is invalid.")
                        In.append(Values[Idx])
                        AxisIn.append(Axis[Idx])
                Env = dict(Values=In, Axis=AxisIn, CntAxis=len(AxisIn), Indent=Helper.Indent*3)
                RunFileCode(os.path.join("Analyse", Analyse[0]), True, Env)
                try:
                    Values = Env["Out"]
                except:
                    Notice(2, "The analyse module did not return a value")
                
            Values = Values.swapaxes(0,1)
            
            SetFile = open(NameSetFile, 'w')
            SetFile.write("#" + "\t".join([str(x) for x in Axis])+"\n")
            for v in Values:
                SetFile.write("\t".join([str(x) for x in v])+"\n")
            SetFile.close()

        if Options.View:
            SetFile = open(NameSetFile, 'r')
            view = SetFile.read()
            SetFile.close()
            for v in view.split("\n"):
                print(Helper.Indent*2, v)

        if Options.Plot:
            s = "\\\"" + NameSetFile + "\\\"" + " title " + "\\\"" + NameSet + "\\\" "
            if PlotOpt is not None:
                s = s + PlotOpt
            PlotList.append(s)

    def ExpandValue(Tree, NameFigure, NameSet, PlotList):
        if "%" in NameSet:
            a = NameSet.find("%")
            b = NameSet[a+1:].find("%")
            VarName = NameSet[a+1:a+b+1]
            
            
            DoExtract = False
            if len(VarName) > 1 and VarName[0] == "!" :
                VarName = VarName[1:]
                DoExtract = True
                
            try:
                VarValue = Tree[VarName]
            except:
                Error(2, "The variable " + VarName + " could not be found.")
                
            ExpandedValues = ExtractValues(VarValue, DoExtract)
            
            for ExpandedValue in ExpandedValues:
                TmpNameSet = NameSet[:a] + str(ExpandedValue) + NameSet[a+b+2:]
                TmpTree = Tree.copy()
                TmpTree[VarName] = ExpandedValue
                ExpandValue(TmpTree, NameFigure, TmpNameSet, PlotList)
        else:
            print(Helper.Indent, "Set", NameSet)
            ParseSet(Tree, NameFigure, NameSet, PlotList)
    ### ProcessTree ###
    if type(Tree) == Options.ydict:
        for t in Tree:
            if t == "PlotSet":
                GnuplotOptions.append(Tree[t])
            elif "Set " in t:
                NameSet = t.split("Set ")[1]
                if NameSet.count("%") % 2 != 0:
                    Error("Beginning and end of each variable has to be marked with \'%\'")
                ExpandValue(Tree[t], NameFigure, NameSet, PlotList)
            elif "Figure " in t:
                NameFigure = t.split("Figure ")[1]
                print("Figure", NameFigure)

                if Options.Collect:
                    if not os.path.exists(Options.SetDir + "/" + NameFigure):
                        os.makedirs(Options.SetDir + "/" + NameFigure)

                GnuplotOptions = []
                PlotList = []
                ProcessTree(Tree[t], NameFigure, PlotList, GnuplotOptions)
                if Options.Plot:
                    Notice(1, "Plotting")
                    PlotCmd = "gnuplot -p -e \"" + "".join([ "set " + str(g) + ";" for g in GnuplotOptions]) + "plot " + ", ".join(PlotList) + "\""
                    os.system(PlotCmd)


def ShowSyntax():
    print("saps command line utility")
    print(sys.argv[0], "<action> <saps configuration file>")
    print("<action>:")
    print("\t-s\tSimulate")
    print("\t-c\tCollect")
    print("\t-v\tView")
    print("\t-p\tPlot")

def ParseArgs():
    for a in sys.argv[1:]:
        if a == "-scp":
            Options.Simulate = True
            Options.Collect = True
            Options.Plot = True
        elif a == "-sc":
            Options.Simulate = True
            Options.Collect = True
        elif a == "-cp":
            Options.Collect = True
            Options.Plot = True
        elif a == "-cvp":
            Options.Collect = True
            Options.View = True
            Options.Plot = True
        elif a == "-cv":
            Options.Collect = True
            Options.View = True
        elif a == "--simulate" or a == "-s":
            Options.Simulate = True
        elif a == "--collect" or a == "-c":
            Options.Collect = True
        elif a == "--view" or a == "-v":
            Options.View = True
        elif a == "--plot" or a == "-p":
            Options.Plot = True
        else:
            Options.Descriptionfile = a

    if Options.Descriptionfile is None:
        ShowSyntax()
        Error(0, "Please specifiy a saps configuration file")

    if (Options.Simulate + Options.Collect + Options.Plot + Options.View) == False:
        ShowSyntax()
        Error(0, "Please specify at least one action.")
    
def main():
    Options.ydict = OrderedYaml.SetOrderedYaml()
    ParseArgs()
    Options.Config = ReadYaml("saps.conf", True) 
    
    try:
        Options.SetDir = os.path.expanduser(Options.Config["Saps"]["DirSet"])
    except:
        Error(1, "Saps -> DirSet has to be defined in configfile.")
        
    Tree = ReadYaml(Options.Descriptionfile, False)
    Tree = RestructureTree(Tree, False)

    try:
        os.makedirs(Options.SetDir)
    except:
        None
    
    ProcessTree(Tree)
    
if __name__ == "__main__":
    main()