import numpy as np

ValuesOut = list()

if len(ValuesIn) != 1:
    Msg.Error(3, "Number of input axis has to be one, when using moving average")

N = int(Analyse["N"])

W = np.convolve(ValuesIn[0], np.ones((N,))/N, mode='same')


ValuesOut = [W]

