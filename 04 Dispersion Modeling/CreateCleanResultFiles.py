import numpy
import os.path

prepath = r"C:\Users\thasegawa\Documents\28 Gun Hill Square Air Quality Modeling\11 CAL3QHCR PM Dispersion\Rev1\newmet"
intarray = ['2','56']
scenarioarray = ['BD','NB']
montharray = ['jan','apr','jul','oct']
yeararray = ['10','11','12','13','14']

intnum = len(intarray)
scenarionum = len(scenarioarray)
monthnum = len(montharray)
yearnum = len(yeararray)

receparray = [310,548]
outfolder = r"C:\Users\thasegawa\Documents\28 Gun Hill Square Air Quality Modeling\11 CAL3QHCR PM Dispersion\Rev1\newmet\Cleaned"

# Check if all files exist
for intindex in range(0,intnum):
    intersection = intarray[intindex]
    recepnum = receparray[intindex]
    for yearindex in range(0,yearnum):
        year = yeararray[yearindex]
        folder = prepath
        for scenarioindex in range(0,scenarionum):
            scenario = scenarioarray[scenarioindex]
            for monthindex in range(0,monthnum):
                month = montharray[monthindex]                            
                filename = "Int" + intersection + "_" + scenario + "_" + month + year + ".OUT"
                filepath = folder + "\\" + filename
                if ~os.path.isfile(filepath):
                    print("File does not exist: %s" % (filepath))
    

for intindex in range(0,intnum):
    intersection = intarray[intindex]
    recepnum = receparray[intindex]
    for yearindex in range(0,yearnum):
        year = yeararray[yearindex]
        folder = prepath
        for scenarioindex in range(0,scenarionum):
            scenario = scenarioarray[scenarioindex]
            for monthindex in range(0,monthnum):
                month = montharray[monthindex]                            
                filename = "Int" + intersection + "_" + scenario + "_" + month + year + ".OUT"
                filepath = folder + "\\" + filename
                out1filename = "Annual_" + filename[:-4] + ".txt"
                out1filepath = outfolder + "\\" + out1filename
                out2filename = "Hour24_" + filename[:-4] + ".txt"
                out2filepath = outfolder + "\\" + out2filename
                                
                f = open(filepath,"rb")
                f1 = open(out1filepath, "w")
                f2 = open(out2filepath, "w")
                trigger1 = 0
                trigger2 = 0
                for line in f:
                    if line[13:19] == "Number":
                        trigger1 = 1
                    elif trigger1 == 1:
                        if line[14:16] == '  ':
                            trigger1 = 0
                        else:
                            while line[-1:] in ["\n", "\r"]:
                                    line = line[:-1]
                            f1.write(line + "\n")

                    if line[12:22] == "No.   Conc":
                        trigger2 = 1
                    elif trigger2 == 1:
                        if len(line) > 5:
                            if (line[13:15] == '  ') or (line[9:12] == "THE"):
                                trigger2 = 0
                            elif (line[13:15] == str(recepnum)):
                                while line[-1:] in ["\n", "\r"]:
                                    line = line[:-1]
                                f2.write(line + "\n")
                                print line
                                trigger2 = 0
                            else:
                                while line[-1:] in ["\n", "\r"]:
                                    line = line[:-1]
                                f2.write(line + "\n")
                                              
                f.close()
                f1.close()
                f2.close()
