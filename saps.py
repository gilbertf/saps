#!/usr/bin/python3
import OrderedYaml
import yaml
import os
import sys
import random
import math

class options():
    global Msg
            
    Collect = False
    
    RoundDigits = 13
    ShowWarning = True
    ShowNotice = True
    
    Descriptionfile = None
    Config = None
    Indent = "   "
    
    #Actions
    Simulate = False
    View = False
    Plot = False
    ydict = dict
    
    def ReadFileConfig(self, NameFileConfig):
        self.Config = ReadYaml(NameFileConfig, True)
        try:
            self.ShowNotice = self.Config["Saps"]["ShowNotice"]
        except:
            None
    
        try:
            self.ShowWarning = self.Config["Saps"]["ShowWarning"]
        except:
            None
        
        try:
            self.RoundDigits = int(self.Config["Saps"]["RoundDigits"])
        except:
            None
            
        try:
            self.SetDir = os.path.expanduser(self.Config["Saps"]["DirSet"])
        except:
            Msg.Error(1, "Saps -> DirSet has to be defined in configfile.")
            
        self.ydict = OrderedYaml.SetOrderedYaml()

    
class msg():
    global Options
    def Msg(self, i, notifier, m):
        print(Options.Indent*i + notifier + " " + m)
    
    def Notice(self, i, m):
        if Options.ShowNotice:
            self.Msg(i, "Notice:", m)
    
    def Warning(self, i, m):
        if Options.ShowWarning:
            self.Msg(i, "Warning:", m)
    
    def Error(self, i, m):
        self.Msg(i, "Error:", m)
        exit()

def ConstructFullPath(NameFile, DirSaps):
    if DirSaps:
        CompleteNameFile = os.path.join(os.path.split(__file__)[0], NameFile)
    else:
        CompleteNameFile = NameFile
    return CompleteNameFile

def ReadYaml(NameFile, DirSaps):
    global Msg     
    CompleteNameFile = os.path.expanduser(ConstructFullPath(NameFile, DirSaps))
    try:
        CompleteFile = open(CompleteNameFile, 'r')
        data = CompleteFile.read()
        CompleteFile.close()
        Tree = yaml.load(data)
        return(Tree)
    except:
        Msg.Error(0, "Unable to read yaml file " + CompleteNameFile)

    
def RunFileCode(NameFile, DirSaps, Env):
    CompleteNameFile = ConstructFullPath(NameFile, DirSaps)
    try:
        File = open(CompleteNameFile)
        Code = File.read()
        File.close()
    except:
        Msg.Error(0, "Unable to read python file " + CompleteNameFile)
    exec(Code, Env)
    
def Num2Str(i):
    try:
        i = round(float(i), Options.RoundDigits)
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
            Msg.Error(2,"Syntax error in " + t)
    return l 

def RestructureTree(Tree, inFigure):
    global Options
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
                            Msg.Warning(0, "More specific value " + str(FiguresSets[fs][p]) + " for " + p + " overwrites " + str(Properties[p]) + ".")
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
        global Options
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
        global Options
        if Set is None:
            Msg.Error(2, "Empy sets are not allowed.")
        for s in Set: #escaping of @ is necessary for malab scripts
            if type(Set[s]) is str:
                Set[s] = Set[s].replace("\\","")

        try:
            Program = os.path.expanduser(Set.pop("Program"))
        except:
            Msg.Error(2, "Program property is missing")

        try:
            Axis = SplitComma(Set.pop("Axis"))
            NumAxis = len(Axis)
        except:
            Msg.Error(2, "Axis property is missing")

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
                Msg.Error(1,"Simulate interface is not defined in configfile")
            Env = dict(ListArgs=ListArgs, Program=Program, Options=Options, Msg=Msg)
            RunFileCode(os.path.join("Simulate", Simulate), True, Env)
            
        if Options.Collect or Options.View or Options.Plot:
            NameSetFile = Options.SetDir + "/" + NameFigure + "/" + NameSet

        if Options.Collect:
            try:
                Collect = Options.Config["Collect"]
            except:
                Msg.Error(1,"Collect interface is not defined in configfile")
            Env = dict(ListArgs=ListArgs, NameSetFile=NameSetFile, Axis = Axis, NumAxis=NumAxis, Program=Program, Options=Options, Msg=Msg)
            RunFileCode(os.path.join("Collect", Collect), True, Env)
            try:
                Values = Env["Values"]
                Axis = Env["Axis"]
            except:
                Msg.Notice(2, "The collect module did not return a Values and Axis")
            
            if Analyse is not None:
                In = []
                AxisIn = []
                if len(Analyse) > 1:
                    ParamsPP = Analyse[1:]
                    for NameParam in ParamsPP:
                        try:
                            Idx = Axis.index(NameParam)
                        except:
                            Msg.Error(2, "The Analyse parameter " + NameParam + " is invalid.")
                        In.append(Values[Idx])
                        AxisIn.append(Axis[Idx])
                Env = dict(Values=In, Axis=AxisIn, CntAxis=len(AxisIn), Options = Options, Msg=Msg)
                RunFileCode(os.path.join("Analyse", Analyse[0]), True, Env)
                try:
                    Values = Env["Out"]
                except:
                    Msg.Notice(2, "The analyse module did not return a value")
                
            #Values = Values.swapaxes(0,1)
            Values = zip(*Values[::1])

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
                print(Options.Indent*2, v)

        if Options.Plot:
            s = "\\\"" + NameSetFile + "\\\"" + " title " + "\\\"" + NameSet + "\\\" "
            if PlotOpt is not None:
                s = s + PlotOpt
            PlotList.append(s)

    def ExpandValue(Tree, NameFigure, NameSet, PlotList):
        global Msg
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
                Msg.Error(2, "The variable " + VarName + " could not be found.")
                
            ExpandedValues = ExtractValues(VarValue, DoExtract)
            
            for ExpandedValue in ExpandedValues:
                TmpNameSet = NameSet[:a] + str(ExpandedValue) + NameSet[a+b+2:]
                TmpTree = Tree.copy()
                TmpTree[VarName] = ExpandedValue
                ExpandValue(TmpTree, NameFigure, TmpNameSet, PlotList)
        else:
            print(Options.Indent, "Set", NameSet)
            ParseSet(Tree, NameFigure, NameSet, PlotList)
    ### ProcessTree ###
    if type(Tree) == Options.ydict:
        for t in Tree:
            if t == "PlotSet":
                GnuplotOptions.append(Tree[t])
            elif "Set " in t:
                NameSet = t.split("Set ")[1]
                if NameSet.count("%") % 2 != 0:
                    Msg.Error("Beginning and end of each variable has to be marked with \'%\'")
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
                    Msg.Notice(1, "Plotting")
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
    global Options
    for a in sys.argv[1:]:
        if a[0:1] == "--":
            for e in a[2:]:
                if e == "simulate":
                    Options.Simulate = True
                elif e == "collect":
                    Options.Collect = True
                elif e == "plot":
                    Options.Plot = True
                elif e == "view":
                    Options.View = True
                else:
                    Msg.Error(0, "Invalid command line option: ", e)
                    
        elif a[0] == "-":
            for e in a[1:]:
                if e == "s":
                    Options.Simulate = True
                elif e == "c":
                    Options.Collect = True
                elif e == "p":
                    Options.Plot = True
                elif e == "v":
                    Options.View = True
                else:
                    Msg.Error(0, "Invalid command line option: ", e)
        else:
            if Options.Descriptionfile is None:
                Options.Descriptionfile = a
            else:
                Msg.Error(0, "You are only allowed to specify one configuration file. I do not understand " + a)

    if Options.Descriptionfile is None:
        ShowSyntax()
        Msg.Error(0, "Please specifiy a saps configuration file")

    if (Options.Simulate + Options.Collect + Options.Plot + Options.View) == False:
        ShowSyntax()
        Msg.Error(0, "Please specify at least one action.")
    
def main():
    global Options, Msg
    
    Options = options()
    Msg = msg()
    Options.ReadFileConfig("saps.conf")
    ParseArgs()
    Tree = ReadYaml(Options.Descriptionfile, False)
    Tree = RestructureTree(Tree, False)

    try:
        os.makedirs(Options.SetDir)
    except:
        None
    
    ProcessTree(Tree)
    
if __name__ == "__main__":
    main()
