#!/usr/bin/env python3
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
    Indent = " " * 2
    
    DebugAnalyse = False
    DebugCollect = False
    DebugRestructure = False
    DebugPlot = False

    Plot2Pdf = False
    Plot2X = False
    
    #Actions
    Simulate = False
    View = False
    Plot = False
    ydict = dict
    
    def ReadFileConfig(self, NameFileConfig):
        self.Config = ReadYaml(NameFileConfig, True)
        
        #Debug Parameters
        try:
            self.DebugAnalyse = self.Config["Saps"]["DebugAnalyse"]
        except:
            None
        try:
            self.DebugCollect = self.Config["Saps"]["DebugCollect"]
        except:
            None
        try:
            self.DebugRestructure = self.Config["Saps"]["DebugRestructure"]
        except:
            None
        try:
            self.DebugPlot = self.Config["Saps"]["DebugPlot"]
        except:
            None
            
        #Msg Parameters
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
            self.RoundDigits = int(self.Config["Saps"]["RoundDigits"])
        except:
            None
            
        #Plot configuration
        try:
            self.Plot2Pdf = int(self.Config["Saps"]["Plot2Pdf"])
        except:
            None
            
        try:
            self.Plot2X = int(self.Config["Saps"]["Plot2X"])
        except:
            None
            
        if self.Plot2Pdf:
            try:
                self.DirPlot = os.path.expanduser(self.Config["Saps"]["DirPlot"])
            except:
                Msg.Error(1, "Saps -> DirPlot has to be defined in configfile, because Plot2Pdf is set.")
        
        #Collect configuration
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
        try:
            Tree = yaml.load(data)
        except OrderedYaml.DuplicateKeyError as e:
            Msg.Error(0, "Duplicate enty. Please remove one of \"" + e.key + "\"")
        return(Tree)
    except FileNotFoundError:
        Msg.Error(0, "The description file " + CompleteNameFile + " does not exist.")
    except yaml.scanner.ScannerError as e:
        if hasattr(e, 'problem_mark'):
            mark = e.problem_mark
            Msg.Error(0, "Scaner error at position %s:%s: \"%s\"" % (mark.line+1, mark.column+1, data.split("\n")[mark.line]))
        else:
            Msg.Error(0, "Scanner error.")
    except yaml.parser.ParserError as e:
        if hasattr(e, 'problem_mark'):
            mark = e.problem_mark
            Msg.Error(0, "Parser error at position %s:%s: \"%s\"" % (mark.line+1, mark.column+1, data.split("\n")[mark.line]))
        else:
            Msg.Error(0, "Parser error.")
    except:
        raise
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

def RestructureTree(Tree, inFigure, inRoot):
    global Options
    hasFigure = False
    hasSet = False
    Properties = Options.ydict()
    FiguresSets = Options.ydict()
    if type(Tree) == Options.ydict:
        #Seperate in two Groups: FigureSets and Properties. Move PlotSet into the Figures but not the Sets
        for t in Tree:
            if "Figure " in t or "Set " in t:
                if type(Tree[t]) is not Options.ydict:
                    Msg.Error(0, "\"" + t + "\" does not have any properties defined,")
                FiguresSets[t] = Tree[t]
                if "Figure " in t:
                    hasFigure = True
                elif "Set " in t:
                    hasSet = True
            elif t == "PlotSet":
                if inFigure:
                    FiguresSets[t] = Tree[t]
                else:
                    Properties[t] = Tree[t]
            else:
                Properties[t] = Tree[t]
                
        #Check for correct structure
        if inFigure and not hasSet:
            Msg.Error(0, "A figure has to contain at least one \"Set <name>:\" definition.")
        if inRoot and not hasFigure:
            Msg.Error(0, "You have to specify at least one \"Figure <name>:\" block.")
            
        #Append all properties to all FigureSets
        for fs in FiguresSets:
            if "Figure " in fs or "Set " in fs:
                if type(FiguresSets[fs]) == Options.ydict:
                    for p in Properties:
                        if not p in FiguresSets[fs]:
                            FiguresSets[fs][p] = Properties[p]
                        else:
                            Msg.Warning(0, "More specific value " + str(FiguresSets[fs][p]) + " for " + p + " overwrites " + str(Properties[p]) + ".")
                    inFigure = False
                    if "Figure " in fs:
                        inFigure = True
                    FiguresSets[fs] = RestructureTree(FiguresSets[fs], inFigure, False)

        if len(FiguresSets) == 0:
            return(Properties) # In der tiefsten Ebene gibt es nur noch properties
        else:
            return(FiguresSets)
            

    
def ProcessTree(Tree, NameFigure = "", ListPlotOpt = [], ListPlotSet = []):
    def ExtractValues(s, DoExtract): #Always returns list of strs to make handling easier
        if type(s) == str and DoExtract:
            return(ParseFloatRange(s))
        else:
            return([Num2Str(s)])
            
    def ParseSet(Set, NameFigure, NameSet, ListPlotOpt):
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

        DictAnalyse = Options.ydict()
        for s in Set:
            if "Analyse" in s: #Akzeptiere auch Analysen ohne Eigenname, deshalb kein Leerzeichen
                DictAnalyse[s] = Set.pop(s)

        #Check that parameters do not contain "forbidden" stuff
        for s in Set:
            if " " in s:
                Msg.Error(2, "The space character is not allowed for parameter names. Please modify: " + str(s))
                
        #Puting the parameters in a list                
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
            RunFileCode(os.path.join("simulate", Simulate), True, Env)
            
        if Options.Collect or Options.View or Options.Plot:
            NameFileSet = "/".join([Options.SetDir, Options.Descriptionfile, NameFigure, NameSet])

        if Options.Collect:
            try:
                Collect = Options.Config["Collect"]
            except:
                Msg.Error(1,"Collect interface is not defined in configfile")
            Env = dict(ListArgs=ListArgs, Axis = Axis, NumAxis=NumAxis, Program=Program, Options=Options, Msg=Msg)
            RunFileCode(os.path.join("collect", Collect), True, Env)
            try:
                Values = Env["Values"]
                Axis = Env["Axis"]
            except:
                Msg.Notice(2, "The collect module did not return Values and Axis")
            
            for Analyse in DictAnalyse:                  
                NameAnalyse = Analyse[Analyse.find(" ")+1:]
                if type(DictAnalyse[Analyse]) is not Options.ydict:
                    Msg.Error(2, "We expect the Analyse option to be a list of parameters.")
                Analyse =  DictAnalyse[Analyse].copy() #Restructure may put references in the Tree, we only want to modify a copy+
                Msg.Msg(2, "Analyse:", NameAnalyse)
                try:
                    FunctionAnalyse = Analyse.pop("Function")
                except:
                    Msg.Error(3, "Analyse " + NameAnalyse + " is missing Function definition")
                try:
                    AxisInAnalyse = SplitComma(Analyse.pop("AxisIn"))
                except:
                    Msg.Error(3, "Analyse " + NameAnalyse + " is missing AxisIn definition")
                try:
                    AxisOutAnalyse = SplitComma(Analyse.pop("AxisOut"))
                except:
                    Msg.Error(3, "Analyse " + NameAnalyse + " is missing AxisOut definition")

                AxisIn = list()
                ValuesIn = list()
                for axis in AxisInAnalyse:
                    if axis not in Axis:
                        Msg.Error(3, "Analyse AxisIn definition " + str(axis) + " is invalid. Available are: " + str(Axis))
                    idx = Axis.index(axis)
                    AxisIn.append(Axis.pop(idx))
                    ValuesIn.append(Values.pop(idx))
                    
                if Options.DebugAnalyse:
                    print(Options.Indent*3 + "AxisIn: " + str(AxisIn) + "\n" + Options.Indent*3 + "ValuesIn: " + str(ValuesIn))

                Env = dict(ValuesIn=ValuesIn, AxisIn=AxisIn, AxisOut=AxisOutAnalyse, Options=Options, Msg=Msg, Analyse=Analyse)
                RunFileCode(os.path.join("analyse", FunctionAnalyse + ".py"), True, Env)
                
                #Put analyse results back to file
                try:
                    ValuesOut = Env["ValuesOut"]
                    AxisOut = Env["AxisOut"]
                    if Options.DebugAnalyse:
                        print(Options.Indent*3 + "AxisOut: " + str(AxisOut) + "\n" + Options.Indent*3 + "ValuesOut: " + str(ValuesOut))
                    for axis in AxisOut:
                        Axis.append(AxisOut.pop())
                        Values.append(ValuesOut.pop())
                except:
                    Msg.Notice(2, "The analyse module did not return the values correctly.")                
                    
                if Options.DebugAnalyse:
                    print(Options.Indent*3 + "Axis: " + str(Axis) + "\n" + Options.Indent*3 + "Values: " + str(Values))

            ##Check if all axis contain the same number of Elements
            Start = None
            for idx, v in enumerate(Values):
                if Start is None:
                    Start = len(v)
                else:
                    if Start != len(v):
                        Msg.Error(2, "Number of elements per axis does not match. " + Axis[0] + " has " + str(Start) + " while " + Axis[idx] + " has " + str(len(v)) + " elements.")
            
            #Save results to Setfiles
            Values = zip(*Values[::1])
            SetFile = open(NameFileSet, 'w')
            SetFile.write("#" + "\t".join([str(x) for x in Axis])+"\n")
            for v in Values:
                SetFile.write("\t".join([str(x) for x in v])+"\n")
            SetFile.close()

        if Options.View:
            SetFile = open(NameFileSet, 'r')
            view = SetFile.read()
            SetFile.close()
            for v in view.split("\n"):
                Msg.Msg(2, "", v)

        if Options.Plot:
            s = "\\\"" + NameFileSet + "\\\"" + " title " + "\\\"" + NameSet + "\\\" "
            if PlotOpt is not None:
                if type(PlotOpt) is list:
                    PlotOpt = " ".join(PlotOpt)
                s = s + PlotOpt
            ListPlotOpt.append(s)

    def ExpandValue(Tree, NameFigure, NameSet, ListPlotOpt):
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
                ExpandValue(TmpTree, NameFigure, TmpNameSet, ListPlotOpt)
        else:
            Msg.Msg(1, "Set", NameSet)
            ParseSet(Tree, NameFigure, NameSet, ListPlotOpt)
            
    ### ProcessTree ###
    if type(Tree) == Options.ydict:
        for t in Tree:
            if t == "PlotSet":
                if type(Tree[t]) is  list:
                    ListPlotSet.extend(Tree[t])
                else:
                    ListPlotSet.append(Tree[t])
            elif "Set " in t:
                NameSet = t.split("Set ")[1]
                if NameSet.count("%") % 2 != 0:
                    Msg.Error("Beginning and end of each variable has to be marked with \'%\'")
                ExpandValue(Tree[t], NameFigure, NameSet, ListPlotOpt)
            elif "Figure " in t:
                NameFigure = t.split("Figure ")[1]
                print("Figure", NameFigure)

                if Options.Collect:
                    try:
                        os.makedirs("/".join([Options.SetDir, Options.Descriptionfile, NameFigure]))
                    except:
                        None

                ListPlotSet = []
                ListPlotOpt = []
                ProcessTree(Tree[t], NameFigure, ListPlotOpt, ListPlotSet)
                if Options.Plot:
                    if Options.Plot2X:
                        print(Options.Indent + "Plotting to X11 using Gnuplot")
                        PlotCmd = "gnuplot -p -e \"" + "".join([ "set " + str(g) + ";" for g in ListPlotSet]) + "plot " + ", ".join(ListPlotOpt) + "\""
                        os.system(PlotCmd)
                        
                    if Options.Plot2Pdf:
                        DirPlot = os.path.join(Options.DirPlot, Options.Descriptionfile, NameFigure.replace(" ","_"))
                        try:
                            os.makedirs(DirPlot)
                        except:
                            None
                        NameFilePdfFigure = os.path.join(DirPlot, NameFigure.replace(" ","_"))
                        ListPlotSet = ["terminal postscript eps enhanced color solid size 7,7","output \\\"" + NameFilePdfFigure + ".eps\\\""] + ListPlotSet
                        print(Options.Indent + "Plotting to pdfs using Gnuplot")
                        PlotCmd = "gnuplot -p -e \"" + "".join([ "set " + str(g) + ";" for g in ListPlotSet]) + "plot " + ", ".join(ListPlotOpt) + "\""
                        os.system(PlotCmd)
                        os.system("ps2pdf " + NameFilePdfFigure + ".eps " + NameFilePdfFigure + ".pdf")
                        os.system("rm " + NameFilePdfFigure + ".eps")
                        os.system("acroread " + NameFilePdfFigure + ".pdf")
                    if Options.DebugPlot:
                        print(Options.Indent + "ListPlotSet: " + str(ListPlotSet))
                        print(Options.Indent + "ListPlotOpt: " + str(ListPlotOpt))


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
                    Msg.Error(0, "Invalid command line option: " + e)
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
    Tree = RestructureTree(Tree, False, True)
    if Options.DebugRestructure:
        print(yaml.dump(Tree, default_flow_style=False))
    try:
        os.makedirs(Options.SetDir)
    except:
        None
    
    ProcessTree(Tree)
    
if __name__ == "__main__":
    main()
