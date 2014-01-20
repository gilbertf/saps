#!/usr/bin/env python3
import OrderedYaml
import yaml
import os
import sys
import random
import math
import copy
from collections import OrderedDict

class options():
    global Msg
            
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

    Plot2X = False
    Plot2EpsLatex = False
    Plot2EpsLatexShow = False
    PdfViewer = "acroread"
    
    #Actions
    Simulate = False
    View = False
    Plot = False
    Collect = False
    Delete = False

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
            self.Plot2X = int(self.Config["Saps"]["Plot2X"])
        except:
            None

        try:
            self.Plot2EpsLatex = int(self.Config["Saps"]["Plot2EpsLatex"])
        except:
            None
            
        try:
            self.Plot2EpsLatexShow = int(self.Config["Saps"]["Plot2EpsLatexShow"])
        except:
            None    

        try:
            self.PdfViewer = int(self.Config["Saps"]["PdfViewer"])
        except:
            None   
            
        if self.Plot2EpsLatex:
            try:
                self.DirPlot = os.path.expanduser(self.Config["Saps"]["DirPlot"])
            except:
                Msg.Error(1, "Saps -> DirPlot has to be defined in configfile, because Plot2EpsLatex is set.")
        
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
        
        
import os
import re

def ConstructNameFileResult(DirResults, Program, List):
    return os.path.join(DirResults, os.path.basename(Program), "_".join(List))

def ExecuteWrapper(Program, ListArgs, ListPrevCmd, ListCmd, DirResults):
    def ReadSignature(NameFile, NamePathFile, FunctionDef):
        f = open(NamePathFile)
        d = f.read()
        try:
            s = FunctionDef + "(.*)" + NameFile + "\((.*)\)"
            m = re.search(s, d)
            Sig = m.group(2)
            Ret = m.group(1)
        except:
            Msg.Error(2, "Parsing function definition failed for " + NamePathFile)
                
        if not Sig:
            Msg.Error(2, "Function signature can not be found in " + NamePathFile)
        else:
            Sig = Sig.replace(" ","").split(",")
        return [set(Sig), Ret]
        
    ProgramType = -1
    isPy = False
    isM = False
    if Program.endswith(".py"):
        isPy = True
        NameFile = os.path.basename(Program).strip(".py")
        [FunctionSignature, ReturnSignature] = ReadSignature(NameFile, Program, "def ")

    elif Program.endswith(".m"):
        isM = True
        NameFile = os.path.basename(Program).strip(".m")
        [FunctionSignature, ReturnSignature] = ReadSignature(NameFile, Program, "function ")
        if not ReturnSignature:
             Msg.Error(2, "Return signature can not be found in " + Program)
        else:
            ReturnSignature = ReturnSignature.replace(" ","").replace("[","").replace("]","").replace("=","").split(",")


    for Args in ListArgs:
        if isPy or isM:
            SapsSignature = set(Args.keys())
            Difference = FunctionSignature - SapsSignature
            if Difference != set():
                Msg.Error(2, "The following program parameters are not specified in the saps description: " + ", ".join(Difference))        
            
        l = []
        for Arg in Args.items():
            l.append("=".join(Arg))
            
        NameFileResult = ConstructNameFileResult(DirResults, Program, l)
        if os.path.isfile(NameFileResult):
            Msg.Notice(2, "Result file exists already, skipping job.")
            continue
        if isPy:
            Exe = "cd " + os.path.dirname(Program) + "; python -c \"from itpp import itsave; import " + NameFile + "; Vars = " + NameFile + "." + NameFile + "(" + ", ".join(l) + "); Vars['Complete'] = 1; itsave(\'" + NameFileResult + "\', Vars)\""
        elif isM:
            Exe = "cd " + os.path.dirname(Program) + "; octave -q --eval \"" + ";".join(l) + "; Complete = 1; [" + ", ".join(ReturnSignature) + "] = " + NameFile + "(" + ", ".join(Args.keys()) + "); itsave(\'" + NameFileResult + "\', Ber, Wer, Complete)\""
        else:
            l.append("=".join(["NameFileResult",NameFileResult]))
            Exe = Program + " " + " ".join(l)
        ListCmd.append(Exe)
    
    
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
            Msg.Error(0, "Scaner error at  line %s pos %s: \"%s\"" % (mark.line+1, mark.column+1, data.split("\n")[mark.line]))
        else:
            Msg.Error(0, "Scanner error.")
    except yaml.parser.ParserError as e:
        if hasattr(e, 'problem_mark'):
            mark = e.problem_mark
            Msg.Error(0, "Parser error at line %s pos %s: \"%s\"" % (mark.line+1, mark.column+1, data.split("\n")[mark.line]))
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

def ExtractValues(s, DoExtract): #Always returns list of strs to make handling easier
    if type(s) == str and DoExtract:
        return(ParseFloatRange(s))
    else:
        return([Num2Str(s)])
            
def ExpandFigures(Tree):
    def ExpandValueNameFigure(Tree, Figure, NameFigure):
        global Msg
        if "%" in NameFigure:
            a = NameFigure.find("%")
            b = NameFigure[a+1:].find("%")
            VarName = NameFigure[a+1:a+b+1]
            
            DoExtract = False
            if len(VarName) > 1 and VarName[0] == "!" :
                VarName = VarName[1:]
                DoExtract = True

            try:
                if VarName in Figure:
                    VarValue = Figure[VarName]
                    isParameter = False
                elif "Parameter" in Figure and VarName in Figure["Parameter"]:
                    VarValue = Figure["Parameter"][VarName]
                    isParameter = True
            except:
                Msg.Error(2, "The variable " + VarName + " could not be found.")

            try:
                VarValue
            except:
                Msg.Error(2, "The value of " + VarName + " is undefined.")

            ExpandedValues = ExtractValues(VarValue, DoExtract)
            
            for ExpandedValue in ExpandedValues:
                TmpNameFigure = NameFigure[:a] + str(ExpandedValue) + NameFigure[a+b+2:]
                TmpFigure = copy.deepcopy(Figure) #Weil wir in ParseSet auch an Unterstrukturen, etwa Analyse Ersetzungen vornehmen
                if isParameter is False:
                    TmpFigure[VarName] = ExpandedValue
                else:
                    TmpFigure["Parameter"][VarName] = ExpandedValue
                ExpandValueNameFigure(Tree, TmpFigure, TmpNameFigure)

        else:
            Tree["Figure "+ NameFigure] = Figure
            
    if type(Tree) == Options.ydict:
        for t in Tree:
            if t.startswith("Figure ") and "%" in t:
                NameFigure = t.split("Figure ")[1]
                if NameFigure.count("%") % 2 != 0:
                    Msg.Error("Beginning and end of each variable has to be marked with \'%\'")
                ExpandValueNameFigure(Tree, Tree[t], NameFigure)
                del Tree[t]

def RemoveGroups(Tree, Parent, InGroup):
    if type(Tree) == Options.ydict:
        for t in Tree:
            if t.startswith("Group"):
                RemoveGroups(Tree[t], Tree, True)
                del Tree[t]
            elif t.startswith("Figure ") or t.startswith("Set "):
                RemoveGroups(Tree[t], None, False)
                
        Properties = Options.ydict()
        Opts = Options.ydict()
        FiguresSets = Options.ydict()
    
        if InGroup:
            for t in Tree:
                if t.startswith("Figure ") or t.startswith("Set "):
                    if type(Tree[t]) is not Options.ydict:
                        Msg.Error(0, "\"" + t + "\" does not have any properties defined,")
                    FiguresSets[t] = Tree[t]
                elif t == "PlotOpt" or t == "SapsOpt":
                    Opts[t] = Tree[t]
                else:
                    Properties[t] = Tree[t]
            for fs in FiguresSets:
                Parent[fs] = FiguresSets[fs]
                for p in Properties:
                    (Parent[fs])[p] = Properties[p]
                for o in Opts:
                    if fs.startswith("Figure "):
                        (Parent[fs])[o] = Opts[o]
                    elif fs.startswith("Set "):
                        Parent[o] = Opts[o]
                
def RestructureTree(Tree, inFigure, inSet, inRoot, RunRecursive):            
    global Options
    hasFigure = False
    hasSet = False
    Properties = Options.ydict()
    FiguresSets = Options.ydict()
    if type(Tree) == Options.ydict:
        #Seperate in two Groups: FigureSets and Properties.
        #Move PlotOpt and SapsOpt into the Figures but not into the Sets
        for t in Tree:
            if t.startswith("Figure ") or t.startswith("Set "):
                if type(Tree[t]) is not Options.ydict:
                    Msg.Error(0, "\"" + t + "\" does not have any properties defined.")
                FiguresSets[t] = Tree[t]
                if t.startswith("Figure "):
                    hasFigure = True
                elif t.startswith("Set "):
                    hasSet = True
            elif t.startswith("Figure") or t.startswith("Set"):
                Msg.Error(2, t + " without a name is not permitted")
            elif t == "PlotOpt" or t == "SapsOpt":
                if inSet:
                    Msg.Error(0, "Using " + t + " inside of set definitions is not allowed.")

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
            if fs.startswith("Figure ") or fs.startswith("Set "):
                if type(FiguresSets[fs]) == Options.ydict:
                    for p in Properties:
                        if not p in FiguresSets[fs]:
                            FiguresSets[fs][p] = Properties[p]
                        else:
                            Msg.Warning(0, "More specific value " + str(FiguresSets[fs][p]) + " for " + p + " overwrites " + str(Properties[p]) + ".")
                    if RunRecursive:
                        inFigure = False
                        inSet = False
                        if fs.startswith("Figure "):
                            inFigure = True
                        elif fs.startswith("Set "):
                            inSet = True
                        FiguresSets[fs] = RestructureTree(FiguresSets[fs], inFigure, inSet, False, RunRecursive)

        if len(FiguresSets) == 0:
            return(Properties) # In der tiefsten Ebene gibt es nur noch properties
        else:
            return(FiguresSets)
            

    
def ProcessTree(Tree, NameFigure = "", ListPlot = [], ListSapsOpt = [], ListPlotOpt = []):          
    def RemoveLatexChars(s):
        if '\\' in s:
            Msg.Error(2, "Backslash is not allowed in " + s)
        return s.replace('{','').replace('}','').replace('_','').replace('$','')
        
    def ParseSet(Set, NameFigure, NameSet, ListPlot):
        global Options
        def ExpandSet(Set, ListArgs, cmd = OrderedDict()):
            if len(Set) > 0:
                s = Set[0]
                V = ExtractValues(s[1], True)
                for v in V:
                    reccmd = cmd.copy() 
                    reccmd[s[0]] = str(v)
                    ExpandSet(Set[1:], ListArgs, reccmd)
            else:
                ListArgs.append(cmd)
                
        def SplitComma(s):
            return s.replace(", ",",").split(",")
            
        def ReplaceParameterByValue(Set, Parameter):
            for s in Set:
                Value = Set[s]
                if type(Value) is Options.ydict:
                    ReplaceParameterByValue(Value, Parameter)
                else:
                    if Value in Parameter:
                        Set[s] = Parameter[Value]
                        
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
        except:
            Msg.Error(2, "Axis property is missing")

        try:
            Plot = Set.pop("Plot")
        except:
            Plot = None
            
        #Used in ExpandValue, dropping here
        try:
            Parameter = Set.pop("Parameter")
        except:
            Parameter = {}
            
        ReplaceParameterByValue(Set, Parameter)

        DictAnalyse = Options.ydict()
        for s in Set:
            if "Analyse" in s: #Akzeptiere auch Analysen ohne Eigenname, deshalb kein Leerzeichen
                DictAnalyse[s] = Set.pop(s)

        #Check that parameters do not contain "forbidden" stuff
        for s in Set:
            if " " in s:
                Msg.Error(2, "The space character is not allowed for variable names. Please modify: " + str(s))
                
        #Puting the parameters in a list                
        Set = list(Set.items())
        Set.sort()
        ListArgs = list()
        ExpandSet(Set, ListArgs)

        try:
            DirResults = Options.Config["FilesystemITPP"]["DirResults"]
        except:
            Msg.Error(1, "FilesystemITPP -> DirResults has to be defined in config file.")
        DirResults = os.path.expanduser(DirResults)
    
        if Options.Delete:
            for Args in ListArgs:
                l = []
                for Arg in Args.items():
                    l.append("=".join(Arg))
                NameFileResult = ConstructNameFileResult(DirResults, Program, l)

                if os.path.isfile(NameFileResult):
                        os.remove(NameFileResult)
                        Msg.Notice(1, "Deleting result file " + NameFileResult)
           
        if Options.Simulate:
            try:
                Simulate = Options.Config["Simulate"]
            except:
                Msg.Error(1,"Simulate interface is not defined in configfile")
                
            #Create results program folder
            ResultsProgram = os.path.join(DirResults, os.path.basename(Program))
            if not os.path.isdir(ResultsProgram):
                os.makedirs(ResultsProgram)
                
            #Simulate
            global ListPrevCmd
            ListCmd = list()
            ExecuteWrapper(Program, ListArgs, ListPrevCmd, ListCmd, DirResults)
            print(ListCmd)
            exit()
            Env = dict(ListCmd=ListCmd, ListArgs=ListArgs, Program=Program, Options=Options, Msg=Msg, ListPrevCmd=ListPrevCmd)
            RunFileCode(os.path.join("simulate", Simulate), True, Env)
            
        if Options.Collect or Options.View or Options.Plot:
            NameFileSet = os.path.join(Options.SetDir, Options.Descriptionfile, NameFigure, RemoveLatexChars(NameSet).replace('/','')) #Slashes in Setname indicate subdirs

        #Liste der zu sammelnden "Axen" zusammenstellen
        if Options.Collect:
            CollectAxis = list()
            NotCollectAxis = list()
            for Analyse in DictAnalyse:
                if type(DictAnalyse[Analyse]) is not Options.ydict:
                    Msg.Error(2, "We expect the Analyse option to be a list of parameters.")
                Analyse =  DictAnalyse[Analyse]
                InAxis = SplitComma(Analyse["AxisIn"])
                for InAx in InAxis:
                    if InAx not in NotCollectAxis and InAx not in CollectAxis:
                        CollectAxis.append(InAx)
                OutAxis = SplitComma(Analyse["AxisOut"])
                for OutAx in OutAxis:
                    if OutAx in CollectAxis:
                        Msg.Error(2, OutAx + " should be a unique.")
                    if OutAx not in NotCollectAxis:
                        NotCollectAxis.append(OutAx)
            for Ax in Axis:
                if Ax not in NotCollectAxis and Ax not in CollectAxis:
                    CollectAxis.append(Ax)
            if Options.DebugAnalyse:                    
                print("Collecting: " +  str(CollectAxis) + " and ignoring " + str(NotCollectAxis))
                        
            #Axenwerte aus den Ergebnisdateien auslesen         
            try:
                Collect = Options.Config["Collect"]
            except:
                Msg.Error(1,"Collect interface is not defined in configfile")
            Env = dict(ListArgs=ListArgs, Axis = CollectAxis, NumAxis=len(CollectAxis), Program=Program, Options=Options, Msg=Msg)
            RunFileCode(os.path.join("collect", Collect), True, Env)
            try:
                CollectValues = Env["Values"]
                CollectAxis = Env["Axis"]
            except:
                Msg.Notice(2, "The collect module did not return Values and Axis")
            
            #Analysen durchführen
            for Analyse in DictAnalyse:
                Pos = Analyse.find(" ")
                if Pos == -1:
                    NameAnalyse = "Unnames analysis"
                else:
                    NameAnalyse = Analyse[Pos+1:]

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
                    if axis not in CollectAxis:
                        Msg.Error(3, "Analyse AxisIn definition " + str(axis) + " is invalid. Available are: " + str(CollectAxis))
                    idx = CollectAxis.index(axis)
                    if len(CollectValues[idx]) == 0:
                        Msg.Error(3, "Axis " + axis + " does not contain any data")
                    AxisIn.append(CollectAxis[idx])
                    ValuesIn.append(CollectValues[idx])
                    
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
                    CollectAxis = CollectAxis + AxisOut
                    CollectValues = CollectValues+ ValuesOut
                except:
                    Msg.Notice(2, "The analyse module did not return the values correctly.")                
                    
                if Options.DebugAnalyse:
                    print(Options.Indent*3 + "Axis: " + str(CollectAxis) + "\n" + Options.Indent*3 + "Values: " + str(CollectValues))

            Values = []
            #Select Axis for plot
            for axis in Axis:
                idx = CollectAxis.index(axis)
                Values.append(CollectValues[idx])

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
            
        if Options.View or Options.Plot:
            SetFile = open(NameFileSet, 'r')
            data = SetFile.read().split("\n")
            SetFile.close()
            if len(data) < 3:
                Msg.Warning(2, "Empty set file, skipping.")
                return

        if Options.View:
            for v in data:
                Msg.Msg(2, "", v)

        if Options.Plot:
            s = "\"" + NameFileSet + "\"" + " title " + "\"" + NameSet + "\" "
            if Plot is not None:
                if type(Plot) is list:
                    Plot = " ".join(Plot)
                s = s + Plot
            ListPlot.append(s)

    def ExpandValue(Tree, NameFigure, NameSet, ListPlot):
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
                if VarName in Tree:
                    VarValue = Tree[VarName]
                    isParameter = False
                elif VarName in Tree["Parameter"]:
                    VarValue = Tree["Parameter"][VarName]
                    isParameter = True
            except:
                Msg.Error(2, "The variable " + VarName + " could not be found.")
            
            ExpandedValues = ExtractValues(VarValue, DoExtract)
            
            for ExpandedValue in ExpandedValues:
                TmpNameSet = NameSet[:a] + str(ExpandedValue) + NameSet[a+b+2:]
                TmpTree = copy.deepcopy(Tree) #Weil wir in ParseSet auch an Unterstrukturen, etwa Analyse Ersetzungen vornehmen
                
                if isParameter is False:
                    TmpTree[VarName] = ExpandedValue
                else:
                    TmpTree["Parameter"][VarName] = ExpandedValue
                ExpandValue(TmpTree, NameFigure, TmpNameSet, ListPlot)

        else:
            Msg.Msg(1, "Set:", NameSet)
            ParseSet(Tree, NameFigure, NameSet, ListPlot)
            
    def EscapeGnuplot(s):
        return s.replace('$','\$').replace('\"','\\\"')
        
    ### ProcessTree ###
    if type(Tree) == Options.ydict:
        for t in Tree:
            if t == "PlotOpt":
                if type(Tree[t]) is  list:
                    ListPlotOpt.extend(Tree[t])
                else:
                    ListPlotOpt.append(Tree[t])
            elif t == "SapsOpt":
                if type(Tree[t]) is  list:
                    ListSapsOpt.extend(Tree[t])
                else:
                    ListSapsOpt.append(Tree[t])
            elif t.startswith("Set "):
                NameSet = t.split("Set ")[1]
                if NameSet.count("%") % 2 != 0:
                    Msg.Error(2, "Beginning and end of each variable has to be marked with \'%\'")
                ExpandValue(Tree[t], NameFigure, NameSet, ListPlot)
            elif t.startswith("Figure "):
                LatexNameFigure = t.split("Figure ")[1]
                NameFigure = RemoveLatexChars(LatexNameFigure)
                print("Figure:", NameFigure)

                if Options.Collect:
                    try:
                        os.removedirs("/".join([Options.SetDir, Options.Descriptionfile, NameFigure]))
                    except:
                        None
                    try:
                        os.makedirs("/".join([Options.SetDir, Options.Descriptionfile, NameFigure]))
                    except:
                        None

                ListPlotOpt = []
                ListSapsOpt = []
                ListPlot = []

                ProcessTree(Tree[t], NameFigure, ListPlot, ListSapsOpt, ListPlotOpt)

                if Options.Plot:
                    TitleIsSet = False
                    for s in ListPlotOpt:
                        if "title " in s:
                            TitleIsSet = True

                    PlotType = None
                    for s in ListSapsOpt:
                        if "notitle" in s:
                            TitleIsSet = True
                        elif s == "3d" or s == "2d":
                            if PlotType is None:
                                if s == "3d":
                                    PlotType = "splot"
                                elif s == "2d":
                                    PlotType = "plot"
                            else:
                                Msg.Error(2, "You are allowed to set SapsOpt to 3d or 2d but not both the same time")
                        else:
                            Msg.Error(2, "Invalid SapsOpt command " + s)

                    if PlotType is None:
                        Msg.Notice(2, "No PlotType was set in SapsOpt, default value 2d is used")
                        PlotType = "plot"
                    
                            
                    if not TitleIsSet:
                        ListPlotOpt.append("title \"" + LatexNameFigure + "\"")
                    
                    if not Options.Plot2X and not Options.Plot2EpsLatex:
                        Msg.Error(2, "Please enable Plot2X or Plot2EpsLatex if you want to use the plot action.")
                        
                    if len(ListPlot) == 0:
                        Msg.Warning(2, "Can not plot since no data could be collected.")
                        continue

                    if Options.DebugPlot:
                        print(Options.Indent + "ListPlotOpt: " + str(ListPlotOpt))
                        print(Options.Indent + "ListSapsOpt: " + str(ListSapsOpt))
                        print(Options.Indent + "ListPlot: " + str(ListPlot))

                    if Options.Plot2X:
                        print(Options.Indent + "Plotting to X11 using Gnuplot")
                        PlotCmd = "gnuplot -persist -e \"" + "".join([ "set " + EscapeGnuplot(RemoveLatexChars(str(PlotOpt))) + ";" for PlotOpt in ListPlotOpt]) + PlotType + " " + ", ".join([EscapeGnuplot(RemoveLatexChars(str(Plot))) for Plot in ListPlot]) + "\""
                        if Options.DebugPlot:
                            print(Options.Indent + "PlotCmd: " + str(PlotCmd))
                        os.system(PlotCmd)
                        
                    if Options.Plot2EpsLatex:
                        EscapedNameFigure = NameFigure.replace(" ","SPACE").replace(".","DOT")
                        DirPlot = os.path.join(Options.DirPlot, Options.Descriptionfile, EscapedNameFigure)
                        try:
                            os.makedirs(DirPlot)
                        except:
                            None
                        NameFilePdfFigure = os.path.join(DirPlot, EscapedNameFigure)
                        ListPlotOpt = ["terminal epslatex color standalone solid size 29.7cm,21cm","output \"" + NameFilePdfFigure + ".tex\""] + ListPlotOpt
                        print(Options.Indent + "Plotting to pdfs using Gnuplot+Latex")

                        PlotCmd = "gnuplot -persist -e \"" + "".join([ "set " + EscapeGnuplot(str(PlotOpt)) + ";" for PlotOpt in ListPlotOpt]) + PlotType + " " + ", ".join([EscapeGnuplot(str(Plot)) for Plot in ListPlot]) + "\""                      
                        if Options.DebugPlot:
                            print(Options.Indent + "PlotCmd: " + str(PlotCmd))
                        os.system(PlotCmd)

                        LatexCmd = "cd "+ DirPlot + "; pdflatex -shell-escape " + NameFilePdfFigure + ".tex > /dev/null"
                        if Options.DebugPlot:
                            print(Options.Indent + "LatexCmd: " + str(LatexCmd))
                        os.system(LatexCmd)

                        if Options.Plot2EpsLatexShow:                        
                            os.system(Options.PdfViewer + " " + NameFilePdfFigure + ".pdf 2> /dev/null &")
                    


def ShowSyntax():
    print("SAPS Command Line Utility")
    print(sys.argv[0], "<action> <saps configuration file>\n")
    print("<action>:")
    print("\t-s\t--simulate\tSimulate")
    print("\t-c\t--collect\tCollect")
    print("\t-v\t--view\t\tView")
    print("\t-p\t--plot\t\tPlot")
    print("\t\t--delete\tDelete result files\n")

def ParseArgs():
    global Options
    for a in sys.argv[1:]:
        if a[0:2] == "--":
            e = a[2:]
            if e == "simulate":
                Options.Simulate = True
            elif e == "collect":
                Options.Collect = True
            elif e == "plot":
                Options.Plot = True
            elif e == "view":
                Options.View = True
            elif e == "delete":
                Options.Delete = True
            else:
                Msg.Error(0, "Invalid command line option: " + e)
                    
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
                if "_" in a:
                    Msg.Error(0, "Please do not use the _ character in description file names.")
                Options.Descriptionfile = a
            else:
                Msg.Error(0, "You are only allowed to specify one configuration file. I do not understand " + a)

    if Options.Descriptionfile is None:
        ShowSyntax()
        Msg.Error(0, "Please specifiy a saps configuration file")

    if (Options.Simulate + Options.Collect + Options.Plot + Options.View + Options.Delete) == False:
        ShowSyntax()
        Msg.Error(0, "Please specify at least one action.")
    
def main():
    global Options, Msg, ListPrevCmd
    ListPrevCmd = []
    
    Options = options()
    Msg = msg()
    Options.ReadFileConfig("saps.conf")
    ParseArgs()
    Tree = ReadYaml(Options.Descriptionfile, False)
    
    #Remove Groups
    RemoveGroups(Tree, None, False)

    #Move Properties into Figures to prepare ExpandFigure
    Tree = RestructureTree(Tree, False, False, True, False)
    
    ExpandFigures(Tree)
    
    #Now move into fuill depth
    Tree = RestructureTree(Tree, False, False, True, True)
    
    if Options.DebugRestructure:
        print(yaml.dump(Tree, default_flow_style=False))
    try:
        os.makedirs(Options.SetDir)
    except:
        None
    
    ProcessTree(Tree)
    
if __name__ == "__main__":
    main()
