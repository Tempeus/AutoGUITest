import os

EVENT_LIST = []

class RapEvent:
    def __init__(self, msgid, paramL, paramH, time):
        self.msgid = msgid
        self.paramL = paramL
        self.paramH = paramH
        self.time = time


def FilterRapFile(rapfile):
    f = open("rapfiles/" + rapfile, "r")
    w = open("rapfiles/temp.txt", "w")
    lines = f.readlines()

    for index, line in enumerate(lines):
        if (index + 1 < len(lines) and index >= 0): #Check bounds
            if "* <XTAGLINE: RAPFILE " in line:
                w.write(line)
            elif "BUTTON" in line:
                if lines[index - 1].find("msgid=WM_MOUSEMOVE") == 1:
                    w.write(lines[index - 1])
                w.write(line)
            elif "KEY" in line:
                if lines[index - 1].find("msgid=WM_MOUSEMOVE") == 1:
                    w.write(lines[index - 1])
                w.write(line)

    f.close()
    w.close()

    os.replace(w.name, f.name)

def TranslateRapFile(rapfile):

    f = open("rapfiles/" + rapfile, "r")
    lines = f.readlines()
    #Split the csv
    line_split = lines.split(",")
    
    msgid = ""
    paramL = ""
    paramH = ""
    time = ""

    for var in line_split:
        temp = var.split('=')
        if(temp[0] == "msgid"):
            msgid = temp[1]
        elif(temp[0] == "paramL"):
            paramL = temp[1]
        elif(temp[0] == "paramH"):
            paramH = temp[1]
        elif(temp[0] == "time"):
            time = temp[1]

    EVENT_LIST.append(RapEvent(msgid, paramL, paramH, time))

if __name__ == "__main__":
    #Find all rapfiles in folder
    
    #Attempt to filter -- Look for a filter flag
    FilterRapFile("test.txt")
    
    #Translate and create python function for each test
    

    #Execute tests
    