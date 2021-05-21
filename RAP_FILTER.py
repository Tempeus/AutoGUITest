import os

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

if __name__ == "__main__":
    FilterRapFile("test.txt")
