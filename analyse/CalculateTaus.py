import numpy as np

try:
    Axis = Analyse["Axis"]
except:
    Axis = 0
    
if len(ValuesIn) == 2:
    #Shift to zero and norm to one
    v = ValuesIn[1]
    t = ValuesIn[0]
    ValuesOut = v - np.min(v, axis = Axis)
    ValuesOut = ValuesOut / np.max(ValuesOut, axis = Axis)

    t0 = -1
    t1 = -1
    for idx, v in enumerate(ValuesOut):
        if v >=0.1 and t0 == -1:
            t0 = t[idx]
        if v >=0.9 and t1 == -1:
            t1 = t[idx]
    tr = t1-t0
    tau1 = tr/np.log(9)

    t2 = -1
    t3 = -1
    rValuesOut = ValuesOut[::-1]
    rt = t[::-1]

    for idx, v in enumerate(rValuesOut):
        if v >=0.1 and t2 == -1:
            t2 = rt[idx]
        if v >=0.9 and t3 == -1:
            t3 = rt[idx]
    tf = t2-t3
    tau2 = tf/np.log(9)


    ValuesOut = [tau1, tau2]
    print("Tau1:" + str(tau1))
    print("Tau2:" + str(tau2))

    print("BW rise:", np.log(9) / (2*np.pi*tr))
    print("BW fall:", np.log(9) / (2*np.pi*tf))
    print("BW:", np.log(9) / (np.pi*(tr+tf)))

else:
    Msg.Error(2, "We expect one input variables")
