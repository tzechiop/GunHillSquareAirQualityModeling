import numpy



folder = "C:/Users/thasegawa/Documents/28 Gun Hill Square Air Quality Modeling/11 CAL3QHCR PM Dispersion/Rev1/newmet/Cleaned"
input1prefix = "Annual_"
input2prefix = "Hour24_"

intarray = ['2','56']
scenarioarray = ['BD','NB']
montharray = ['jan','apr','jul','oct']
yeararray = ['10','11','12','13','14']

intnum = len(intarray)
scenarionum = len(scenarioarray)
monthnum = len(montharray)
yearnum = len(yeararray)

receparray = [310,548]

for intindex in range(0,intnum):
    intersection = intarray[intindex]
    recepnum = receparray[intindex]
    data1 = numpy.zeros((recepnum, monthnum,yearnum,scenarionum))
    data2 = numpy.zeros((recepnum, monthnum,yearnum,scenarionum))
    outdata1 = numpy.zeros((recepnum,1,yearnum+1,scenarionum))
    outdata2 = numpy.zeros((recepnum,monthnum+1,1,scenarionum))
    for yearindex in range(0,yearnum):
        year = yeararray[yearindex]
        for scenarioindex in range(0,scenarionum):
            scenario = scenarioarray[scenarioindex]
            for monthindex in range(0,monthnum):
                month = montharray[monthindex]
                
                filename1 = input1prefix + "Int" + intersection + "_" + scenario + "_" + month + year + ".txt"
                filepath1 = folder + "/" + filename1
                filename2 = input2prefix + "Int" + intersection + "_" + scenario + "_" + month + year + ".txt"
                filepath2 = folder + "/" + filename2
                
                f1 = open(filepath1,"rb")
                recepindex = 0
                for line in f1:
                    data1[recepindex, monthindex, yearindex, scenarioindex] = float(line[27:33])
                    recepindex = recepindex + 1
                f1.close()

                f2 = open(filepath2,"rb")
                recepindex = 0
                for line in f2:
                    data2[recepindex, monthindex, yearindex, scenarioindex] = float(line[17:24])
                    recepindex = recepindex + 1
                f2.close()

    for scenarioindex in range(0,scenarionum):
        for recepindex in range(0, recepnum):
            for yearindex in range(0,yearnum):
                outdata1[recepindex,0,yearindex,scenarioindex] = numpy.mean(data1[recepindex, :, yearindex, scenarioindex])
            outdata1[recepindex,0,yearnum,scenarioindex] = numpy.mean(outdata1[recepindex,0,0:yearnum,scenarioindex])

    for scenarioindex in range(0,scenarionum):
        for recepindex in range(0, recepnum):
            for monthindex in range(0,monthnum):
                outdata2[recepindex,monthindex,0,scenarioindex] = numpy.mean(data2[recepindex,monthindex,0:yearnum,scenarioindex])
            outdata2[recepindex,monthnum,0,scenarioindex] = numpy.max(outdata2[recepindex,0:monthnum,0,scenarioindex])

    cleanedfilename1 = "CleanedData_" + "Int" + intersection + "_Annual.txt"
    cleanedfilepath1 = folder + "/" + cleanedfilename1
    cleanedfilename2 = "CleanedData_" + "Int" + intersection + "_Hour24.txt"
    cleanedfilepath2 = folder + "/" + cleanedfilename2

    outputfilename3 = "Output_" + "Int" + intersection + "_Annual.txt"
    outputfilepath3 = folder + "/" + outputfilename3
    outputfilename4 = "Output_" + "Int" + intersection + "_Hour24.txt"
    outputfilepath4 = folder + "/" + outputfilename4

    f3 = open(cleanedfilepath1, "w")
    f3.write("Receptor,Intersection,Scenario,Year,Jan-Mar,Apr-Jun,Jul-Sep,Oct-Dec,AnnualAverage\n")
    for scenarioindex in range(0,scenarionum):
        scenario = scenarioarray[scenarioindex]
        for recepindex in range(0, recepnum):
            for yearindex in range(0,yearnum):
                year = yeararray[yearindex]
                writeline = str(recepindex + 1) + "," + intersection + "," + scenario + "," + year + ","
                for monthindex in range(0,monthnum):
                    month = montharray[monthindex]
                    writeline = writeline + str(data1[recepindex, monthindex, yearindex, scenarioindex]) + ","
                writeline = writeline + str(outdata1[recepindex,0,yearindex,scenarioindex]) + "\n"
                f3.write(writeline)
    f3.close()

    f4 = open(cleanedfilepath2, "w")
    f4.write("Receptor,Intersection,Scenario,Year,Jan-Mar,Apr-Jun,Jul-Sep,Oct-Dec\n")
    for scenarioindex in range(0,scenarionum):
        scenario = scenarioarray[scenarioindex]
        for recepindex in range(0, recepnum):
            for yearindex in range(0,yearnum):
                year = yeararray[yearindex]
                writeline = str(recepindex + 1) + "," + intersection + "," + scenario + "," + year + ","
                for monthindex in range(0,monthnum):
                    month = montharray[monthindex]
                    writeline = writeline + str(data2[recepindex, monthindex, yearindex, scenarioindex])
                    if monthindex != monthnum-1:
                        writeline = writeline + ","
                    else:
                        writeline = writeline + "\n"
                f4.write(writeline)
    f4.close()
    
    f5 = open(outputfilepath3, "w")
    f5.write("Receptor,Intersection,Scenario,AnnualPM2.5\n")
    for scenarioindex in range(0,scenarionum):
        scenario = scenarioarray[scenarioindex]
        for recepindex in range(0, recepnum):
            writeline = str(recepindex + 1) + "," + intersection + "," + scenario + "," + str(outdata1[recepindex, 0, yearnum,scenarioindex]) + "\n"
            f5.write(writeline)
    f5.close()

    f6 = open(outputfilepath4, "w")
    f6.write("Receptor,Intersection,Scenario,24HourPM2.5\n")
    for scenarioindex in range(0,scenarionum):
        scenario = scenarioarray[scenarioindex]
        for recepindex in range(0, recepnum):
            writeline = str(recepindex + 1) + "," + intersection + "," + scenario + "," + str(outdata2[recepindex, monthnum, 0 ,scenarioindex]) + "\n"
            f6.write(writeline)
    f6.close()
    
