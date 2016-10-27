# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 10:34:55 2016

This script reads the extracted HCS spreadsheet data output by ReadHCSSpreadsheets.py.
This script then calculates the following parameters for each intersection:
- total traffic volumes
- total heavy duty volumes
- total delay

To run this script on path data, use the following command:
python OrganizeHCSData.py _%%E -i "Organized Data" -o "Summed Data"

@author: thasegawa
"""

import os
import argparse
import pandas as pd

# Function to calculate traffic volumes for each intersection
def calculate_traffic(suffix, indir, outdir):
    # Read volumes data
    infile = os.path.join(indir, 'vol{0}.xlsx'.format(suffix))
    data = pd.read_excel(infile)
    
    vols = pd.DataFrame(data.sum(axis = 1))      # Sum data       
    
    #Output data
    outfile = os.path.join(outdir, 'vol_summed{0}.xlsx'.format(suffix))
    vols.to_excel(outfile, index = False, header = False)      # Output

# Function to calculate heavy duty traffic volumes for each intersection
def calculate_heavyduty(suffix, indir, outdir):
    # Read volumes data    
    infile = os.path.join(indir, 'vol{0}.xlsx'.format(suffix))
    vol = pd.read_excel(infile)
    
    # Read bus data    
    infile = os.path.join(indir, 'busvol{0}.xlsx'.format(suffix))
    bus = pd.read_excel(infile)
    
    # Read hdperc data
    infile = os.path.join(indir, 'hdperc{0}.xlsx'.format(suffix))
    hdperc = pd.read_excel(infile)
    
    # Calculate heavy duty vehicles
    hdvol = vol*hdperc/100 + bus
    hdvol = hdvol.applymap(round)
    hdvol = pd.DataFrame(hdvol.sum(axis = 1))
    
    # Output data
    outfile = os.path.join(outdir, 'hdvol_summed{0}.xlsx'.format(suffix))
    hdvol.to_excel(outfile, index = False, header = False)      # Output

# Function to calculate delay for each intersection
def calculate_delay(suffix, indir, outdir):
    # Read adjusted volumes data    
    infile = os.path.join(indir, 'adjvol{0}.xlsx'.format(suffix))
    adjvol = pd.read_excel(infile)
    
    # Read delay data    
    infile = os.path.join(indir, 'delay{0}.xlsx'.format(suffix))
    delay = pd.read_excel(infile)
    
    # Calculate delay data
    prod = adjvol*delay
    prodsum = prod.sum(axis = 1)
    volsum = adjvol.sum(axis = 1)
    delaytot = pd.DataFrame(prodsum / volsum)
    
    # Output data
    outfile = os.path.join(outdir, 'delay_summed{0}.xlsx'.format(suffix))
    delaytot.to_excel(outfile, index = False, header = False)      # Output  
        
# =============================================================================

print('Running OrganizeHCSData.py...')

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('suffix')
parser.add_argument('-i', '--indir', default='', type=str, help="input directory")
parser.add_argument('-o', '--outdir', default='', type=str, help="output directory")
args = vars(parser.parse_args())
suffix, indir, outdir = args['suffix'], args['indir'], args['outdir']

print('Reading data with suffix {0}'.format(suffix))
if outdir != '':
    print('Output directory: {0}'.format(outdir))

# Read and sum volume data
print('Calculating traffic...')
calculate_traffic(suffix, indir, outdir)
print('Calculating heavy duty traffic...')
calculate_heavyduty(suffix, indir, outdir)
print('Calculating delay...')
calculate_delay(suffix, indir, outdir)

print('Finished!!!\n')