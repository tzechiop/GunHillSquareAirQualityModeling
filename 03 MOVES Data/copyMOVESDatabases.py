# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 10:58:28 2016

This script is used to copy all of the input databases for an intersection
and rename it to a new intersection.

@author: thasegawa

"""

import os
import shutil

# Specify path for MySQL folder
mysqlpath = r'C:\ProgramData\MySQL\MySQL Server 5.7\Data'
os.chdir(mysqlpath)

# Specify months and times
mon_list = ['jan','apr','jul','oct']
time_list = ['am','md','pm','on']

# specify intersection names
baseintname = 'int2bd'
newintname_list = ['int2nb', 'int5627bd', 'int5627nb']


basedatabasename = 'ghs_v2_pm_int2bd_2019_0{0}0{1}_{2}{3}_2014b_in'

# Loop through months and times and copy database
for newintname in newintname_list:
    for mon_index, mon in enumerate(mon_list):
        for time_index, time in enumerate(time_list):
            # Specify database names
            databasename = basedatabasename.format(mon_index + 1, time_index + 1, mon, time)
            newdatabasename = databasename.replace(baseintname, newintname)

            # Copy database
            shutil.copytree(databasename, newdatabasename)