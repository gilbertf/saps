#!/usr/bin/python
from itpp import itload
import sys

Cmd = sys.argv

f = open("/home/gilbert/Dissertation/libgjm/modulations/OptPsm6.inc","w")
if len(Cmd) == 2:
    try:
        Data = itload(Cmd[1])
        Symbol = Data["OptSymbols"]
    except:
        print "Could not find OptSymbols variable in results file"
        exit()
    M = len(Symbol)
    print M
    f.write("ivec labelling("+ str(M) + ");")
    f.write("for (int i=0;i<" + str(M) + ";i++) labelling(" + str(M-1) + "-i) = i;\n")

    f.write("cvec symbols = \"")
    for s in Symbol:
        x = s.item(0)
        s = "{0:.15f}".format(x)
        s = s.replace('j','i') + " "
        #s = str(x).replace('(','').replace(')','').replace('j','i') + " "
        f.write(s)
else:
    print "Syntax: " + Cmd[0] + " <filename>"

f.write("\";\n")
f.write("Modulator_2D mod(symbols, labelling);\nreturn mod;")
f.close()
