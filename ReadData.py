import numpy as np

def ReadData(Filename, Cols, Rows):
    a = np.loadtxt(Filename, ndmin=2)
    Out=dict()
    Out["data"] = a
    if Cols != -1 and Rows == -1:
       for c in range(int(Cols)):
           Out["col" + str(c)] = a[:, c]

    if Rows != -1 and Cols == -1:
       for r in range(int(Rows)):
           Out["row" + str(r)] = a[r, :]

    return Out
