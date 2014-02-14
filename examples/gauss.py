import numpy as np
from math import *

def gauss(x, Expectation, Variance):
    Sigma = sqrt(Variance);
    pdf = (1/(Sigma*sqrt(2*pi))) * exp(-(x-Expectation)**2/(2*Variance));
    cdf = 0.5 * (1+erf((x-Expectation)/sqrt(2*Variance)));

    Out = dict()
    Out['Sigma'] = Sigma
    Out['pdf'] = pdf
    Out['cdf'] = cdf
    return Out
