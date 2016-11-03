class LinkVertex(object):
    def __init__(self, fid, intnum, linkid, startx, starty, width, linknum=0, endx=0, endy=0):
        self.fid = fid
        self.intnum = intnum
        self.linkid = linkid
        self.linknum = linknum
        self.startx = startx
        self.starty = starty
        self.width = width
        self.endx = endx
        self.endy = endy

class Link(object):
    def __init__(self, linkid, traffic_am=0, emissions_am=0, traffic_md=0, emissions_md=0, traffic_pm=0, emissions_pm=0, traffic_on=0, emissions_on=0):
        self.linkid = linkid
        self.traffic_am = traffic_am
        self.emissions_am = emissions_am
        self.traffic_md = traffic_md
        self.emissions_md = emissions_md
        self.traffic_pm = traffic_pm
        self.emissions_pm = emissions_pm
        self.traffic_on = traffic_on
        self.emissions_on = emissions_on


import arcpy
import csv
from math import log10
from math import floor

def CreateInputFile(intnum, scenario_num, month_num, year_num,
                    receptor_shp, linkvertex_shp,
                    traffictable_path, traffictable_prefix, traffictable_suffix,
                    emissionstable_path, emissionstable_prefix, emissionstable_suffix,
                    surfacestation_num, upperstation_num,
                    outputfile_path, outputfile_prefix):

    averagingtime = "60.00"
    surfaceroughness = "321.000"
    settlingvelocity = "0.00"
    depositionvelocity = "0.00"
    conversionfactor = "1.0000"
    outputunitflag = "2"
    PrintFlags = "0 0 'U'"
    TierFlags = " 2 'P'"
    WeekFlags = " 1 1 1 1 1 1 1"

    surfacestation_year = year_num
    upperstation_year = year_num

    receptor_fields = ["FID", "Int_Num", "ET_X", "ET_Y"]
    linkvertex_fields = ["FID", "Int_Num", "Link_ID", "X_COORD", "Y_COORD","Width_1"]

    scenario_listupper = ['BD','NB']
    scenario_listlower = ['bd','nb']
    month_list = ['jan','apr','jul','oct']
    monthnum_list = [1, 4, 7, 10]
    enddate_list = [31, 30, 30, 31]
    time_list = ['am','md','pm','on']
    timenum_list = [[7,8,9],[10,11,12,13,14,15,16],[17,18,19],[20,21,22,23,24,1,2,3,4,5,6]]

    writelist = []

    outputfile_fullpath = outputfile_path + "/" + outputfile_prefix + scenario_listupper[scenario_num] + "_" + month_list[month_num] + str(year_num)+ ".INP"

    # Write header lines
    writelist.append("'Int" + str(2) + "_" + scenario_listupper[scenario_num] + "' ")
    writelist[0] += str(averagingtime) + " " + surfaceroughness + " " + settlingvelocity + " " + depositionvelocity + " "

    writelist.append(str(monthnum_list[month_num]) + " 1 " + str(year_num) + " " + str(monthnum_list[month_num]+2) + " " + str(enddate_list[month_num]) + " " + str(year_num))
    writelist.append(str(surfacestation_num) + " " + str(surfacestation_year) + " " + str(upperstation_num) + " " + str(upperstation_year))
    writelist.append(PrintFlags)

    # Write receptor lines
    recepcount = 0
    with arcpy.da.SearchCursor(receptor_shp, receptor_fields) as cursor:
        for row in cursor:
            if row[1] in intnum:
                recepcount += 1
                if row[0] == 0:
                    digitnum = 1
                else:
                    digitnum = floor(log10(row[0])) + 1

                zeros = "00000"
                index = 0
                while index < digitnum:
                    zeros = zeros[:-1]
                    index += 1

                writelist.append("'R_" + zeros + str(row[0]) + "                                 ' " + '%.2f' % row[2] + " " + '%.2f' % row[3] + "   1.80")

    # Continue writing first line header
    writelist[0] += str(recepcount) + " " + conversionfactor + " " + outputunitflag

    # Write pattern flags
    writelist.append(TierFlags)
    writelist.append(WeekFlags)
    writelist.append("'CAL3QHCR RUN' ")

    # Write Links
    linknum_row = len(writelist)
    linkcount = 0
    link_list = []
    link_sublist = []
	uniqlink_list = []
    with arcpy.da.SearchCursor(linkvertex_shp, linkvertex_fields, sql_clause = (None, "ORDER BY FID")) as cursor:
        for row in cursor:
            if row[1] in intnum:
                link_list.append(LinkVertex(fid=row[0], intnum=row[1], linkid=row[2], startx=row[3], starty=row[4], width=row[5]))
				uniqlink_list.append(row[2])
	uniqlink_list = list(set(uniqlink_list))

    for linka in link_list:
        for linkb in link_list:
            if (linkb.linkid == linka.linkid) and (linkb.fid == linka.fid + 1):
                linka.endx = linkb.startx
                linka.endy = linkb.starty

                linkcount += 1
                linka.linknum = linkcount

                linksubcount = 1
                for link_sub in link_list:
                    if (link_sub.linkid == linka.linkid)and (link_sub.fid < linka.fid):
                        linksubcount += 1
                
                spacing = "                                 "
                digitnum = floor(log10(linka.linkid)) + 1
                index = 0
                while index < digitnum:
                    spacing = spacing[:-1]
                    index += 1

                digitnum = floor(log10(linksubcount)) + 1
                index = 0
                while index < digitnum:
                    spacing = spacing[:-1]
                    index += 1

                writelist.append("    " + str(linkcount) + " 1")
                writelist.append("'Link_"+ str(linka.linkid) + "_" + str(linksubcount) + spacing + "' 'AG' " + '%.2f' % linka.startx + " " + '%.2f' % linka.starty + " " + '%.2f' % linka.endx + " " + '%.2f' % linka.endy + "    0.00    " + '%.2f' % linka.width)

                break
    writelist[linknum_row-1] += str(linkcount)
                
    # Write traffic/emissions data
    linkinput_list = []
    for time in time_list:
        traffictable_fullpath = traffictable_path + "/" + traffictable_prefix + month_list[month_num] + time + traffictable_suffix
        with open(traffictable_fullpath, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter = ",")
            for row in spamreader:
                if time == 'am':
                    linkinput = Link(linkid=row[0])
                    linkinput_list.append(linkinput)
                else:
                    for linkinput in linkinput_list:
                        if linkinput.linkid == row[0]:
                            break

                trafficattribute = 'traffic_' + time
                traffic = row[5]
                setattr(linkinput, trafficattribute, traffic)

        emissionstable_fullpath = emissionstable_path + "/" + emissionstable_prefix + month_list[month_num] + time + emissionstable_suffix
        with open(emissionstable_fullpath, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter = ",")
            for row in spamreader:
                for linkinput in linkinput_list:
                    if linkinput.linkid == row[4]:
                        break

                emissionsattribute = 'emissions_' + time
                emissions = row[6]
                setattr(linkinput, emissionsattribute, emissions)

            
    for hour in range(1,24+1):
        for timenum in range(4):
            if hour in timenum_list[timenum]:
                time = time_list[timenum]
                trafficattribute = 'traffic_' + time
                emissionsattribute = 'emissions_' + time
                break
            
        spacing = "      "
        digitnum = floor(log10(hour)) + 1
        index = 0
        while index < digitnum:
            spacing = spacing[:-1]
            index += 1
            
        writelist.append(str(hour) + spacing + "0.00")
        for linknum in range(1,linkcount+1):
            for link in link_list:
                if link.linknum == linknum:
                    break

            for linkinput in linkinput_list:
                if int(linkinput.linkid) == link.linkid:
                    traffic = float(getattr(linkinput, trafficattribute))
                    emissions = float(getattr(linkinput, emissionsattribute))
                    break

            spacing1 = "       "
            digitnum = floor(log10(linknum)) + 1
            index = 0
            while index < digitnum:
                spacing1 = spacing1[:-1]
                index += 1
           
            spacing2 = "      "
            digitnum = floor(log10(traffic)) + 1
            index = 0
            while index < digitnum:
                spacing2 = spacing2[:-1]
                index += 1
            
            writelist.append(spacing1 + str(linknum) + spacing2 + '%.2f' % traffic + " " + '%.9f' % emissions)

    # Write text file
    f = open(outputfile_fullpath, "w")
    for write in writelist:
        f.write(write)
        f.write("\n")

    f.close()
