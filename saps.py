#!/usr/bin/env python3
import OrderedYaml
import yaml
import os
import sys
import math
import copy
from collections import OrderedDict
import numpy as np
from colorama import Fore
import hashlib

class options():
    global Msg
            
    RoundDigits = 13
    ShowWarning = True
    ShowNotice = True
    
    Descriptionfile = None
    DescriptionFiles = list()
    Config = None
    Indent = " " * 2
    
    DebugRestructure = False
    DebugCollect = False
    DebugAnalyse = False
    DebugPlot = False

    Plot2X = False
    Plot2EpsLatex = False
    Plot2EpsLatexShow = False
    PdfViewer = "acroread"
    Plot2Tikz = False
    
    SimulateInstantaneous = False
    Valgrind = False
    Matlab = False
    ddd = False
    
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
            self.DebugRestructure = self.Config["Saps"]["DebugRestructure"]
        except:
            None
        try:
            self.DebugCollect = self.Config["Saps"]["DebugCollect"]
        except:
            None
        try:
            self.DebugAnalyse = self.Config["Saps"]["DebugAnalyse"]
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
            
        try:
            self.Plot2Tikz = int(self.Config["Saps"]["Plot2Tikz"])
        except:
            None    
            
        if self.Plot2EpsLatex or self.Plot2Tikz:
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
    def Msg(self, i, notifier, m, color = None):
        if color:
            print(color + Options.Indent*i + notifier + " " + m + Fore.RESET)
        else:
            print(Options.Indent*i + notifier + " " + m)
            
    def Notice(self, i, *m):
        if Options.ShowNotice:
            self.Msg(i, "Notice:", " ".join(m))
    
    def Warning(self, i, *m):
        if Options.ShowWarning:
            self.Msg(i, "Warning:", " ".join(m), Fore.RED)
    
    def Error(self, i, *m):
        self.Msg(i, "Error:", " ".join(m), Fore.RED)
        exit()
        
import re

def ListToNiceStr(List):
    Str = ", ".join(List)
    if len(List) > 1:
        Idx = Str.rfind(", ")
        Str = Str[0:Idx] + " and " + Str[Idx+2:]
    return Str

def ConstructNameFileResult(DirResults, Program, ArgStr):
    HashNameFileResult = True
    if HashNameFileResult:
        ArgStr = hashlib.sha224(bytes(ArgStr, 'utf8')).hexdigest()
    if len(ArgStr) > 255:
        Msg.Error(0, "NameFileResult", ArgStr, "is too long for most filesystems with", str(len(ArgStr)), "letters.")
    return os.path.join(DirResults, os.path.basename(Program), ArgStr)

def ArgsToStr(Args, Sep="_", Comb="="):
    l = []
    for Arg in Args.items():
        l.append(Comb.join(Arg))
    if len(l) == 0:
        l.append("NoParameters")
    return Sep.join(l)
            
def ExecuteWrapper(Program, ListArgs, ListCmd, DirResults):
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
            Msg.Error(2, "Function signature can not be found in " + NamePathFile + ". It has to contain at least one variable name")
        else:
            Sig = Sig.replace(" ","").split(",")
        return [Sig, Ret]
     
    Program = os.path.abspath(Program)
    if not os.path.isfile(Program):
        Msg.Error(2, "Specified program " + Program + " does not exist")

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
    
    global SimNameFileResultList
    for Args in ListArgs:
        if isPy or isM:
            SapsSignature = set(Args.keys())
            Difference = set(FunctionSignature) - SapsSignature
            if Difference != set():
                Msg.Error(2, "The following program parameters are not specified in " + Options.Descriptionfile + ": " + ListToNiceStr(Difference))
            IncPaths = "\'{0}\',\'{1}\'".format(os.path.dirname(Program), os.path.dirname(__file__))
            
        NameFileResult = ConstructNameFileResult(DirResults, Program, ArgsToStr(Args))
        
        if NameFileResult not in SimNameFileResultList:
            Msg.Notice(2, "Simulating " + NameFileResult)
            SimNameFileResultList.append(NameFileResult)
            if os.path.isfile(NameFileResult):
                Msg.Notice(2, "Result file exists already, skipping job.")
                continue
            if isPy:
                VarsAppendArgs = ";".join([ "Vars['" + str(Arg) + "'] = " + str(Args[Arg]) for Arg in Args ])
                Exe = "python3 -c \"import sys\nsys.path.extend([" + IncPaths + "])\nfrom itpp import itsave\nimport " + NameFile + "\nVars = " + NameFile + "." + NameFile + "(" + ArgsToStr(Args, ", ") + ")\nVars['Complete'] = 1\n" + VarsAppendArgs + "\ntry:\n    itsave(\'" + NameFileResult + "\', Vars)\nexcept Exception as e:\n    print('" + Options.Indent*2 + "Error: Running python script " + Program + " failed with exception: ' + e)\""
            elif isM:
                TmpArgs = Args.copy() #Octave preferes strings in quotation marks
                for Arg in TmpArgs:
                    if not TmpArgs[Arg].replace(".","").replace("-","").isdigit():
                        TmpArgs[Arg]="\'" + TmpArgs[Arg] + "\'"
                if Options.Matlab:
                    Exe = "cd " + os.path.dirname(Program) + "; matlab -nodisplay -nosplash -nodesktop -nojvm -r \"" + ArgsToStr(TmpArgs, ";") + ";Complete=1;addpath(" + IncPaths + ");[" + ",".join(ReturnSignature) + "]=" + NameFile + "(" + ",".join(FunctionSignature) + ");itsave(\'" + NameFileResult + "\',Complete," + ",".join(ReturnSignature) + "," + ",".join(FunctionSignature) +  ");exit\""
                else:
                    Exe = "cd " + os.path.dirname(Program) + "; octave -q --eval \"" + ArgsToStr(TmpArgs, ";") + "; Complete = 1; addpath(" + IncPaths + "); [" + ", ".join(ReturnSignature) + "] = " + NameFile + "(" + ", ".join(FunctionSignature) + "); itsave(\'" + NameFileResult + "\', Complete, " + ", ".join(ReturnSignature) + ", " + ", ".join(FunctionSignature) +  ")\""
            else:
                TmpArgs = Args.copy()
                TmpArgs.update({"NameFileResult":NameFileResult})
                Exe = Program + " " + ArgsToStr(TmpArgs, " ")
                if Options.Valgrind:
                   Exe = "valgrind --leak-check=full " + Exe
                if Options.ddd:
                   Exe = "ddd --args " + Exe
            ListCmd.append(Exe)
        else:
            Msg.Notice(2, "Skipping duplicate simulation of " + NameFileResult)
    
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
                    Msg.Error(0, "Beginning and end of each variable has to be marked with \'%\'")
                ExpandValueNameFigure(Tree, Tree[t], NameFigure)
                del Tree[t]

def ParseIncludes(Tree):
    if type(Tree) == Options.ydict:
        for t in Tree:
            if t == "Include":
                x = ReadYaml(Tree[t] + ".saps", False)
                for e in x:
                    if e in Tree:
                        Msg.Error(2, "Double entry", e, "found when including", Tree[t]+".saps")
                    else:
                        Tree[e] = x[e]
                del Tree[t]
            else:
                Tree[t] = ParseIncludes(Tree[t])
    return Tree

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
            

def ProcessTree(Tree, NameFigure = "", ListPlot = [], ListSapsOpt = [], ListPlotOpt = [], ViewMode = False):          
    def RemoveLatexChars(s):
        return s.replace('{','').replace('}','').replace('_','').replace('$','').replace('\\','').replace('textrm','')
        
    def ParseSet(Set, NameFigure, NameSet, ListPlot, ViewMode = False):
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
        
        def ConstructValueIndices(Value, Indices):
            for i in range(len(Indices)):
                if type(Indices[i]) is float: #ExpandValues puts floats
                    Indices[i] = int(Indices[i])
            Indices = [str(e) for e in Indices]
            return str(Value) + "[" + "#".join(Indices) + "]"
            
        def ExtractValueAndIndices(a, toInt=False):
            if type(a) is str:
                BracketOpen = "["
                BracketClose = "]"
                NumBracketsOpen = a.count(BracketOpen)
                NumBracketsClose = a.count(BracketClose)
                SplitArrayIdx = None
                
                if NumBracketsOpen == 1 and NumBracketsClose == 1:
                    ArrayIdx = a[a.find(BracketOpen)+1:a.find(BracketClose)]
                    Msg.Notice(2, "Array index: " + ArrayIdx)
                    SplitArrayIdx = ArrayIdx.split("#")
                    if len(SplitArrayIdx) == 1 or len(SplitArrayIdx) == 2:
                        if toInt:
                            for Idx in range(len(SplitArrayIdx)):
                                if SplitArrayIdx[Idx] == "":
                                    SplitArrayIdx[Idx] = -1
                                else:
                                    try:
                                        SplitArrayIdx[Idx] = int(SplitArrayIdx[Idx])  
                                    except:
                                        Msg.Error(2, "Invalid indexing with: " + str(ArrayIdx))
                    else:
                        Msg.Error(2, "Invalid index: " + ArrayIdx)
    
                    Value = a[:a.find(BracketOpen)]
                    if len(Value) == 0:
                        Msg.Error(2, "Failed to extract value")
                elif NumBracketsOpen == 0 and NumBracketsClose == 0:
                    Value = a
                else:
                    Msg.Error(2, "Invalid indexing brackets in " + a)
    
                return [Value, SplitArrayIdx]
            else:
                return [a, None]
                
                
        def ReplaceParameterByValue(Set, Parameter):
            for s in Set:
                Value = Set[s]
                if type(Value) is Options.ydict:
                    ReplaceParameterByValue(Value, Parameter)
                else:
                    if type(Value) is not list:
                        [extValue, extIndices] = ExtractValueAndIndices(Value)
                        if extIndices != None:
                            Changed = False
                            for i in range(len(extIndices)):
                                if extIndices[i] in Parameter:
                                    Changed = True
                                    extIndices[i] = Parameter[extIndices[i]]
                            if Changed:
                                Set[s] = ConstructValueIndices(extValue, extIndices)
                        elif Value in Parameter:
                            Set[s] = Parameter[Value]
                    else:
                        Msg.Error(1, "Invalid value type " + str(type(Value)) + " for " + s)
                        
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
            Plot = Set.pop("Plot")
        except:
            Plot = None

        try:
            Parameter = Set.pop("Parameter")
        except:
            Parameter = {}
        ReplaceParameterByValue(Set, Parameter)

        try:
            Axis = SplitComma(Set.pop("Axis"))
        except:
            Msg.Error(2, "Axis property is missing")
            
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
            global DeleteNameFileResultList
            for Args in ListArgs:
                NameFileResult = ConstructNameFileResult(DirResults, Program, ArgsToStr(Args))
                if NameFileResult not in DeleteNameFileResultList:
                    DeleteNameFileResultList.append(NameFileResult)
                    if os.path.isfile(NameFileResult):
                            os.remove(NameFileResult)
                            Msg.Notice(2, "Deleting result file " + NameFileResult)
                else:
                    Msg.Notice(2, "Skipping duplicat delete of " + NameFileResult)
           
        if Options.Simulate:
            if Options.SimulateInstantaneous:
                Simulate = "RunOnline.py"
            else:
                try:
                    Simulate = Options.Config["Simulate"]
                except:
                    Msg.Error(1,"Simulate interface is not defined in configfile")

            #Create results program folder
            ResultsProgram = os.path.join(DirResults, os.path.basename(Program))
            if not os.path.isdir(ResultsProgram):
                os.makedirs(ResultsProgram)
                
            #Simulate
            ListCmd = list()
            ExecuteWrapper(Program, ListArgs, ListCmd, DirResults)

            Env = dict(ListCmd=ListCmd, ListArgs=ListArgs, Program=Program, Options=Options, Msg=Msg)
            RunFileCode(os.path.join("simulate", Simulate), True, Env)          
            
        if Options.Collect or Options.View or Options.Plot:
            NameFileSet = os.path.join(Options.SetDir, Options.Descriptionfile, NameFigure, RemoveLatexChars(NameSet).replace('/','')) #Slashes in Setname indicate subdirs

        #Liste der zu sammelnden "Axen" zusammenstellen
        if Options.Collect:
            CollectAxis = list()
            NotCollectAxis = list()
            for AnalyseName in DictAnalyse:
                if type(DictAnalyse[AnalyseName]) is not Options.ydict:
                    Msg.Error(2, "We expect the Analyse option to be a list of parameters.")
                Analyse =  DictAnalyse[AnalyseName]
                
                try:
                    InAxis = SplitComma(Analyse["AxisIn"])
                except:
                    Msg.Error(2, "AxisIn is required for", str(AnalyseName))
                    
                for InAx in InAxis:
                    if InAx not in NotCollectAxis and InAx not in CollectAxis:
                        CollectAxis.append(InAx)
                        
                try:
                    OutAxis = SplitComma(Analyse["AxisOut"])
                except:
                    Msg.Error(2, "AxisOut is required for", str(AnalyseName))

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
                    CollectValues = CollectValues + ValuesOut
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
                    if np.isscalar(v):
                        Msg.Error(2, "Axis " + Axis[idx] + " is of type scalar. This is not allowed at the moment.")
                    Start = len(v)
                else:
                    if Start != len(v):
                        Msg.Error(2, "Number of elements per axis does not match. " + Axis[0] + " has " + str(Start) + " while " + Axis[idx] + " has " + str(len(v)) + " elements.")
            
            #Check for Nan
            for v in Values:
                for s in v:
                    if np.isnan(s):
                        Msg.Warning(2, "Nan values are not allowed!")
                        
            #Save results to Setfiles
            zValues = zip(*Values[::1])
            SetFile = open(NameFileSet, 'w')
            
            SetFile.write("#" + "\t".join([str(x) for x in Axis])+"\n")
            LastVal = ""
            for v in zValues:
                if len(v) == 3:
                    if v[0] != LastVal: #for 3d plots
                        SetFile.write("\n")
                        LastVal = v[0]
                SetFile.write("\t".join([str(x) for x in v])+"\n")
            SetFile.close()
            
        if Options.View or Options.Plot:
            SetFile = open(NameFileSet, 'r')
            data = SetFile.read().split("\n")
            SetFile.close()
            if len(data) < 3:
                Msg.Warning(2, "Empty set file, skipping.")
                return      

        if Options.View or (ViewMode and (Options.View or Options.Plot)):
            Msg.Msg(2, "View:", "", Fore.YELLOW)
            
            from prettytable import PrettyTable
            t = PrettyTable(data[0][1:].split("\t"))
            for v in data[1:]:
                if len(v) > 0:
                    t.add_row(v.split("\t"))
            Msg.Msg(3, t.get_string().replace("\n","\n" + Options.Indent*3), "", Fore.YELLOW)

        if Options.Plot and not ViewMode:
            s = "\"" + NameFileSet + "\""
            if Plot is not None:
                if type(Plot) is list:
                    First = True
                    for e in Plot:
                        if "every" in e:
                            if not First:
                                Msg.Error(2, "Every has to be the first Plot option")
                        First = False
                    Plot = " ".join(Plot)
                s = s + Plot
            s = s + " title " + "\"" + NameSet + "\" "
            ListPlot.append(s)

    def ExpandValue(Tree, NameFigure, NameSet, ListPlot, ViewMode = False):
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
                ExpandValue(TmpTree, NameFigure, TmpNameSet, ListPlot, ViewMode)

        else:
            Msg.Msg(1, "Set:", Fore.CYAN + RemoveLatexChars(NameSet) + Fore.RESET)
            ParseSet(Tree, NameFigure, NameSet, ListPlot, ViewMode)
            
    def EscapeGnuplot(s):
        return s.replace('\\','\\\\').replace('$','\$').replace('\"','\\\"')
        
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
                ExpandValue(Tree[t], NameFigure, NameSet, ListPlot, ViewMode)
            elif t.startswith("Figure "):
                LatexNameFigure = t.split("Figure ")[1]
                NameFigure = RemoveLatexChars(LatexNameFigure)
                print("Figure:", Fore.BLUE + NameFigure + Fore.RESET)

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

                try:
                    if "view" in (Tree[t])["SapsOpt"]:
                        ViewMode = True
                    else:
                        ViewMode = False
                except:
                    ViewMode = False   
  
                ProcessTree(Tree[t], NameFigure, ListPlot, ListSapsOpt, ListPlotOpt, ViewMode)

                if Options.Plot and not ViewMode:
                    TitleIsSet = False
                    for s in ListPlotOpt:
                        if "title " in s:
                            TitleIsSet = True

                    PlotType = None
                    Size = "9.5,6"
                    
                    for s in ListSapsOpt:
                        if s == "notitle":
                            TitleIsSet = True
                        elif s == "view":
                            Options.Plot = False
                            Options.View = True
                        elif "size " in s:
                            Size = s[5:]
                        elif s == "3d" or s == "2d":
                            if PlotType is None:
                                if s == "3d":
                                    PlotType = "splot"
                                elif s == "2d":
                                    PlotType = "plot"
                            else:
                                Msg.Error(2, "You are allowed to set SapsOpt to 3d or 2d but not both the same time")
                        else:
                            Msg.Error(2, "Invalid SapsOpt command " + str(s))

                    Size = Size.replace(" ", "").split(",")
                    RatioSize = float(Size[0])/float(Size[1])
                    PaperSize = Size[0] + "cm," + Size[1] + "cm"
                    ScreenSize = "1000," + str(1000/RatioSize) 
                            
                    if PlotType is None:
                        Msg.Notice(2, "No PlotType was set in SapsOpt, default value 2d is used")
                        PlotType = "plot"
                    
                            
                    if not TitleIsSet:
                        ListPlotOpt.append("title \"" + LatexNameFigure + "\"")
                    
                    if not Options.Plot2X and not Options.Plot2EpsLatex and not Options.Plot2Tikz:
                        Msg.Error(2, "Please enable Plot2X or Plot2EpsLatex if you want to use the plot action.")
                        
                    if len(ListPlot) == 0:
                        Msg.Warning(2, "Can not plot since no data could be collected.")
                        continue


                    if Options.DebugPlot:
                        print(Options.Indent*2 + "ListPlotOpt: " + str(ListPlotOpt))
                        print(Options.Indent*2 + "ListSapsOpt: " + str(ListSapsOpt))
                        print(Options.Indent*2 + "ListPlot: " + str(ListPlot))

                    
                    if Options.Plot2X:
                        print(Options.Indent*2 + "Plotting to X11 using Gnuplot")
                        
                        CurListPlotOpt = ["terminal qt size " + ScreenSize] + ListPlotOpt

                        PlotCmd = "gnuplot -e \"" + "".join([ "set " + EscapeGnuplot(RemoveLatexChars(str(PlotOpt))) + ";" for PlotOpt in CurListPlotOpt]) + PlotType + " " + ", ".join([EscapeGnuplot(RemoveLatexChars(str(Plot))) for Plot in ListPlot]) + "; pause mouse close; exit" + "\"" + "&"
                        if Options.DebugPlot:
                            print(Options.Indent*2 + "PlotCmd: " + str(PlotCmd))
                        ret = os.system(PlotCmd)
                        if ret != 0:
                            Msg.Error(1,"Running gnuplot failed")
                        
                        
                    if Options.Plot2EpsLatex:
                        EscapedNameFigure = NameFigure.replace(" ","").replace(".","").replace('~','').replace('/','')
                        DirPlot = os.path.join(Options.DirPlot, Options.Descriptionfile, EscapedNameFigure)
                        try:
                            os.makedirs(DirPlot)
                        except:
                            None
                        NameFilePdfFigure = os.path.join(DirPlot, EscapedNameFigure)
                        CurListPlotOpt = ["terminal epslatex color standalone solid size " + PaperSize, "output \"" + NameFilePdfFigure + ".tex\""] + ListPlotOpt
                        print(Options.Indent*2 + "Plotting to pdfs using Gnuplot+Latex")

                        PlotCmd = "gnuplot -e \"" + "".join([ "set " + EscapeGnuplot(str(PlotOpt)) + ";" for PlotOpt in CurListPlotOpt]) + PlotType + " " + ", ".join([EscapeGnuplot(str(Plot)) for Plot in ListPlot]) + "\""                      
                        if Options.DebugPlot:
                            print(Options.Indent*2 + "PlotCmd: " + str(PlotCmd))
                        ret = os.system(PlotCmd)
                        if ret != 0:
                            Msg.Error(1,"Running gnuplot failed")

                        LatexCmd = "cd "+ DirPlot + "; sed -i 's/usepackage{color}/usepackage{color}\\n\\\\usepackage{units}/g' " + NameFilePdfFigure + ".tex; pdflatex -shell-escape " + NameFilePdfFigure + ".tex > /dev/null"
                        if Options.DebugPlot:
                            print(Options.Indent*2 + "LatexCmd: " + str(LatexCmd))
                        os.system(LatexCmd)

                        if Options.Plot2EpsLatexShow:                        
                            os.system(Options.PdfViewer + " " + NameFilePdfFigure + ".pdf 2> /dev/null &")
                    
                    
                    if Options.Plot2Tikz:
                        EscapedNameFigure = NameFigure.replace(" ","").replace(".","").replace('~','').replace('/','')
                        DirPlot = os.path.join(Options.DirPlot, Options.Descriptionfile, EscapedNameFigure)
                        try:
                            os.makedirs(DirPlot)
                        except:
                            None
                        NameFileTikzFigure = os.path.join(DirPlot, EscapedNameFigure)

                        CurListPlotOpt = ["terminal tikz size " + PaperSize, "output \"" + NameFileTikzFigure + ".tikz\""] + ListPlotOpt
                        print(Options.Indent*2 + "Plotting to tikz using Gnuplot")

                        PlotCmd = "gnuplot -persist -e \"" + "".join([ "set " + EscapeGnuplot(str(PlotOpt)) + ";" for PlotOpt in CurListPlotOpt]) + PlotType + " " + ", ".join([EscapeGnuplot(str(Plot)) for Plot in ListPlot]) + "\""                      
                        if Options.DebugPlot:
                            print(Options.Indent*2 + "PlotCmd: " + str(PlotCmd))
                        ret = os.system(PlotCmd)
                        if ret != 0:
                            Msg.Error(1,"Running gnuplot failed")

def ShowSyntax():
    print("SAPS Command Line Utility")
    print(sys.argv[0], "<action> <saps configuration file>\n")
    print("<action>:")
    print("\t-s\t--simulate\tSimulate")
    print("\t-c\t--collect\tCollect")
    print("\t-v\t--view\t\tView")
    print("\t-p\t--plot\t\tPlot")
    print("\t-i\t--instant\tInstant simulation")
    print("\t\ŧ--matlab\tUse evil software package")
    print("\t\t--valgrind\tInvoke valgrind")
    print("\t\t--ddd\tInvoke ddd")
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
            elif e == "instant":
                Options.SimulateInstantaneous = True
            elif e == "valgrind":
                Options.Valgrind = True
            elif e == "matlab":
                Options.Matlab = True
            elif e == "ddd":
                Options.ddd = True
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
                elif e == "i":
                    Options.SimulateInstantaneous = True
                else:
                    Msg.Error(0, "Invalid command line option: " + e)
        else:
            if "_" in a:
                Msg.Error(0, "Please do not use the _ character in description file names.")
            Options.DescriptionFiles.append(a)

    if len(Options.DescriptionFiles) == 0:
        ShowSyntax()
        Msg.Error(0, "Please specifiy a saps configuration file")

    if (Options.Simulate + Options.Collect + Options.Plot + Options.View + Options.Delete) == False:
        ShowSyntax()
        Msg.Error(0, "Please specify at least one action.")

    if not Options.SimulateInstantaneous and Options.Valgrind:
        Msg.Error(0, "Valgrind is only allowd in interactive mode")

    if not Options.SimulateInstantaneous and Options.ddd:
        Msg.Error(0, "ddd is only allowd in interactive mode")
    
def main():
    global Options, Msg, SimNameFileResultList, DeleteNameFileResultList
    SimNameFileResultList = []
    DeleteNameFileResultList = []
    
    Options = options()
    Msg = msg()
    Options.ReadFileConfig("saps.conf")
    ParseArgs()
    for LoopDescriptionfile in Options.DescriptionFiles:
        Options.Descriptionfile = LoopDescriptionfile
        Tree = ReadYaml(Options.Descriptionfile, False)

        Tree = ParseIncludes(Tree)

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
    if sys.version_info >= (3,2):
         main()
    else:
         print("Invalid python version, at least 3.2 is required")
