# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 10:28:55 2016

This script creates queries that can be used in MySQL Workbench to output
the tables link and linksourcetypehour. The output csvs can then be used to
QAQC the values in those tables.

@author: thasegawa
"""

# Specify months and times
intname_list = ['int2bd', 'int2nb', 'int5627bd', 'int5627nb']
mon_list = ['jan','apr','jul','oct']
time_list = ['am','md','pm','on']

# Print queries
for intname in intname_list:
    path = 'C:\ProgramData\MySQL\MySQL Server 5.7\Data\Results PM\\'
    path = path.replace('\\', '/')
    for mon_index, mon in enumerate(mon_list):
        for time_index, time in enumerate(time_list):
            base1 = """SELECT * FROM ghs_v2_pm_""" + intname + """_2019_0{0}0{1}_{2}{3}_2014b_out.pm25_grams_per_veh_mile INTO OUTFILE '""" + path + """/pm25_""" + intname + """_0{0}0{1}_{2}{3}.csv' FIELDS TERMINATED BY ',';"""
            #base2 = """SELECT * FROM ghs_v2_pm_""" + intname + """_2019_0{0}0{1}_{2}{3}_2014b_out.linksourcetypehour INTO OUTFILE '""" + path + """/typ_0{0}0{1}_{2}{3}.csv' FIELDS TERMINATED BY ',';"""
            query1 = base1.format(mon_index + 1, time_index + 1, mon, time)
            print(query1)
            #query2 = base2.format(mon_index + 1, time_index + 1, mon, time)
            #print(query2)