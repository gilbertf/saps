try:
    ShowNotice = Config["saps"]["ShowNotice"]
except:
    ShowNotice = False

try:
    ShowWarning = Config["saps"]["ShowWarning"]
except:
    ShowWarning = False

try:
    RoundDigits = int(Config["saps"]["RoundDigits"])
except:
    RoundDigits = 13

Indent = "   "

def Msg(i, notifier, msg):
    print(Indent*i + notifier + " " + msg)

def Notice(i, msg):
    if ShowNotice:
        Msg(i, "Notice:", msg)

def Warning(i, msg):
    if ShowWarning:
        Msg(i, "Warning:", msg)

def Error(i, msg):
    Msg(i, "Error:", msg)
    exit()
