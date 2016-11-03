# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 18:29:40 2016

@author: thasegawa
"""

import os

path = r'C:\ProgramData\MySQL\MySQL Server 5.7\Data\copy'
os.chdir(path)

oldintname = 'int5627bd'
newintname = 'int5627nb'

filename_list = os.listdir()
for filename in filename_list:
    os.rename(filename, filename.replace(oldintname, newintname))
        