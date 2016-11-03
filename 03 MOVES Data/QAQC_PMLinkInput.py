# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 10:35:17 2016

This script can be used to QAQC the link and linksourcetypehour input into MOVES.
This script was written to operate on the link and linksourcetypehour tables created
by createSQLQuery_ExportLinks.py. This script was written to QAQC inputs to
the PM analysis. QAQC for the CO analysis can be done by hand, because of the
small number of tables.

The basetables, which the MOVES tables will be compared against, should be organized
by time.

@author: thasegawa
"""

import os
import pandas as pd

# Specify paths and int name
intname = 'int2nb'
sheetname = 'Links_NB #2'
basebasepath = r'C:\ProgramData\MySQL\MySQL Server 5.7\Data\Input Tables\PM'
movespath = r'C:\ProgramData\MySQL\MySQL Server 5.7\Data\QAQC tables\Links_{0}'.format(intname)

# Specify months and times
mon_list = ['jan','apr','jul','oct']
time_list = ['am','md','pm','on']

# Specify base names for tables
basevol = 'Links_MOVESInput.xlsx'
basetyp = 'LinkSource_MOVESInput.xlsx'
MOVESvol = 'vol_0{0}0{1}_{2}{3}.csv'
MOVEStyp = 'typ_0{0}0{1}_{2}{3}.csv'

# Loop through months and times and check volume and source type hour
for mon_index, mon in enumerate(mon_list):
    for time_index, time in enumerate(time_list):
        # Read base data
        basepath = os.path.join(basebasepath, time.upper())
        basevoldata = pd.read_excel(os.path.join(basepath, basevol), sheetname = sheetname)
        basetypdata = pd.read_excel(os.path.join(basepath, basetyp), sheetname = sheetname)
        
        # Read moves data
        movesvoldata = pd.read_csv(os.path.join(movespath, MOVESvol.format(mon_index + 1, time_index + 1, mon, time)), header = None)
        movestypdata = pd.read_csv(os.path.join(movespath, MOVEStyp.format(mon_index + 1, time_index + 1, mon, time)), header = None)
        
        # Check data against each other
        voldiff_max = (basevoldata['linkVolume'] - movesvoldata[5]).max()
        typdiff_max = (basetypdata['sourceTypeHourFraction'] - movestypdata[2]).max()
        
        if voldiff_max > 0.1:
            print('Difference detected in volume data for 0{0}0{1}_{2}{3}'.format(mon_index + 1, time_index + 1, mon, time))
        if voldiff_max > 0.0001:
            print('Difference detected in source type data for 0{0}0{1}_{2}{3}'.format(mon_index + 1, time_index + 1, mon, time))
        break
    break
        