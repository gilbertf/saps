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
    f.write("for (int i=0;i<" + str(M) + ";i++) labelling(" + str(M-1) + "-i) = i;")

    f.write("cvec symbols = \"")
    for s in Symbol:
        x = s.item(0)
        s = str(x.real)
        if x.imag > 0:
            s = s + "+" + str(x.imag) + "i "
        else:
            s = s + str(x.imag) + "i "

        f.write(s)
else:
    print "Syntax: " + Cmd[0] + " <filename>"

f.write("\";")
f.write("Modulator_2D mod(symbols, labelling); return mod;")
f.close()
