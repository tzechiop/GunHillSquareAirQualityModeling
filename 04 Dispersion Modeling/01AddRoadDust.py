import csv

MOVESpath = "C:/Users/thasegawa/Documents/28 Gun Hill Square Air Quality Modeling/11 CAL3QHCR PM Dispersion/Input"
MOVESprefix = "ghs_int"
MOVESsuffix = "_pm_results.csv"

outputpath = "C:/Users/thasegawa/Documents/28 Gun Hill Square Air Quality Modeling/11 CAL3QHCR PM Dispersion/Input/Road Dust"
outputprefix = "ghs_int"
outputsuffix = "_pm_results_roaddust.csv"

RoadDust = 0.25*(0.10**0.91)*(3**1.02) # g/(veh*mile)

inter_list = ['2','56']
scenario_list = ['bd','nb']
month_list = ['jan','apr','jul','oct']
time_list = ['am','md','pm','on']

emissions_col = 6

for inter in inter_list:
    for scenario in scenario_list:
        for month in month_list:
            for time in time_list:
                inputfilename = MOVESpath + "/" + MOVESprefix + inter + scenario + "_2018" + month + time + MOVESsuffix
                outputfilename = outputpath + "/" + outputprefix + inter + scenario + "_2018" + month + time + outputsuffix

                writelist = []
                
                with open(inputfilename, 'rb') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar = "|")
                    for row in spamreader:
                        writelist.append(row)
                        for writelist_index in range(len(writelist[-1])):
                            writelist[-1][writelist_index] = writelist[-1][writelist_index][1:-1]
                        writelist[-1][emissions_col] = float(writelist[-1][-1])
                        writelist[-1][emissions_col] += RoadDust

                with open(outputfilename, 'wb') as csvfile:
                    spamwriter = csv.writer(csvfile)
                    spamwriter.writerows(writelist)
                    

                
