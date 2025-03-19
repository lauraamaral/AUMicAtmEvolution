"""
This script produces Figure 2 from Amaral+2025,
using VPLANET's STELLAR and FLARE modules.
Flare Frequency Distribution used in the work.

@autor: Laura N.  R. do Amaral,  Arizona State University (2024)
@email: laura.nevesdoamaral@gmail.com
Date: October 2024
"""
import os
import pathlib
import subprocess
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from math import exp, expm1, log10, log
import matplotlib.style
import seaborn as sns
from scipy.interpolate import interp1d
import matplotlib as mpl
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import pandas as pd

try:
    import vplot as vpl
except:
    print('Cannot import vplot. Please install vplot.')



#Typical plot parameters that make for pretty plot
#mpl.style.use('classic')

mpl.rcParams['xtick.major.size'] = 7
mpl.rcParams['xtick.major.width'] = 1
mpl.rcParams['ytick.major.size'] = 7
mpl.rcParams['ytick.major.width'] = 1

mpl.rcParams['xtick.minor.size'] = 5
mpl.rcParams['xtick.minor.width'] = 1
mpl.rcParams['ytick.minor.size'] = 5
mpl.rcParams['ytick.minor.width'] = 1

mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.top'] = True
mpl.rcParams['xtick.bottom'] = True
mpl.rcParams['ytick.right'] = True

'''
path = pathlib.Path(__file__).parents[0].absolute()
sys.path.insert(1, str(path.parents[0]))
from get_args import get_args

# Defining the directory where the data is

def run_vplanet(dir):
         print("\nRunning simulation in %s directory..." % dir)
         os.chdir(dir)
         subprocess.call(['vplanet', 'vpl.in'])
         # Return to top-level directory
         os.chdir(path)
         return dir 

for i in run:
    run_vplanet(i)
'''
DataFlare2_2 = pd.read_csv("./SourceFiles/Flares_2.2Factor/star.star.forward", sep='\s+', header=None)
DataFlare2_8 = pd.read_csv("./SourceFiles/Flares_2.8Factor/star.star.forward", sep='\s+', header=None)
DataFlare2_2.columns = ['Time','Luminosity','LXUVTot','LXUVFlare','Age','FlareFreqMin','FlareFreqMax','FlareEnergyMin','FlareEnergyMax','LXUVStellar']  # Define your column names
DataFlare2_8.columns = ['Time','Luminosity','LXUVTot','LXUVFlare','Age','FlareFreqMin','FlareFreqMax','FlareEnergyMin','FlareEnergyMax','LXUVStellar']  # Define your column names

fig= plt.figure(figsize=(8,7))

cmap = ['#FF7500','#0079BB','turquoise']

def nu(alpha, beta, Energy):
    flarerate = (10**beta)*(Energy)**alpha
    return flarerate

a = 2
b = 6

AField = -0.74
Bfield = -0.31
AYoung = -0.61
BYoung = 1.38

FfdHAZMATYoung = []
FlareEnergyHAZMATYoung = [10**29.47712125472,10**32.1]

FfdHAZMATField = []
FlareEnergyHAZMATField = [10**27.69897,10**29.8451]

for i in range(2):
    FfdHAZMATYoung.append(nu(AYoung,BYoung,FlareEnergyHAZMATYoung[i]/1e30))
    FfdHAZMATField.append(nu(AField,Bfield,FlareEnergyHAZMATField[i]/1e30))

plt.plot(FlareEnergyHAZMATYoung,FfdHAZMATYoung, color= cmap[0], ls= '-',alpha=0.4, linewidth=b, label='t')
plt.plot(FlareEnergyHAZMATField, FfdHAZMATField, color= cmap[1], ls= '-',alpha=0.4, linewidth=b, label='t')


###########################################################

# AU Mic FFD (Tristan+2024)

E_Uband = [10**31.15606936416185, 10**33.213872832369944]
nu_Uband = [8.933474625132906, 0.2919484154422963]
E_SXR = [10**31.641618497109825, 10**33.398843930635834]
nu_SRX = [6.866488450042995, 0.3727593720314938]

plt.plot(E_Uband,nu_Uband, color = 'Teal', lw = 2)
plt.plot(E_SXR,nu_SRX, color = 'mediumturquoise', lw = 2)
############################################################

FFD = [DataFlare2_2[DataFlare2_2['Age'] == 4.0000000000e+07]['FlareFreqMin'],
        DataFlare2_2[DataFlare2_2['Age'] == 4.0000000000e+07]['FlareFreqMax'],
        DataFlare2_2[DataFlare2_2['Age'] == 5.0000000000e+09]['FlareFreqMin'],
        DataFlare2_2[DataFlare2_2['Age'] == 5.0000000000e+09]['FlareFreqMax'],
        DataFlare2_8[DataFlare2_8['Age'] == 4.0000000000e+07]['FlareFreqMin'],
        DataFlare2_8[DataFlare2_8['Age'] == 4.0000000000e+07]['FlareFreqMax'],
        DataFlare2_8[DataFlare2_8['Age'] == 5.0000000000e+09]['FlareFreqMin'],
        DataFlare2_8[DataFlare2_8['Age'] == 5.0000000000e+09]['FlareFreqMax']
        ]

FlareEnergy = [DataFlare2_2[DataFlare2_2['Age'] == 4.0000000000e+07]['FlareEnergyMin']*2.181518,
        DataFlare2_2[DataFlare2_2['Age'] == 4.0000000000e+07]['FlareEnergyMax']*2.181518,
        DataFlare2_2[DataFlare2_2['Age'] == 5.0000000000e+09]['FlareEnergyMin']*2.181518,
        DataFlare2_2[DataFlare2_2['Age'] == 5.0000000000e+09]['FlareEnergyMax']*2.181518,
        DataFlare2_8[DataFlare2_8['Age'] == 4.0000000000e+07]['FlareEnergyMin']*2.802369997628342,
        DataFlare2_8[DataFlare2_8['Age'] == 4.0000000000e+07]['FlareEnergyMax']*2.802369997628342,
        DataFlare2_8[DataFlare2_8['Age'] == 5.0000000000e+09]['FlareEnergyMin']*2.802369997628342,
        DataFlare2_8[DataFlare2_8['Age'] == 5.0000000000e+09]['FlareEnergyMax']*2.802369997628342
        ]

plt.plot(FlareEnergy[0:2], FFD[0:2], color= cmap[0], ls= ':', linewidth=a, label='t')
plt.plot(FlareEnergy[2:4], FFD[2:4], color= cmap[1], ls= ':', linewidth=a, label='t')
plt.plot(FlareEnergy[4:6], FFD[4:6], color= cmap[0], ls= '--', linewidth=a, label='t')
plt.plot(FlareEnergy[6:8], FFD[6:8], color= cmap[1], ls= '--', linewidth=a, label='t')

########################################## Legend ######################################################

legend_elements = [
                   Line2D([0], [0], color = cmap[0], lw=5, label=r'40 Myr | This work'),
                   Line2D([0], [0], color = cmap[1], lw=5, label=r'5 Gyr | This work'),
                   Line2D([0], [0], color =  cmap[0], lw=8,alpha = 0.4, label=r'FUV | HAZMAT (40 Myr) | Loyd+2018a'),
                   Line2D([0], [0], color =  cmap[1], lw=8,alpha = 0.4, label=r'FUV | MUSCLES (Field Age) | Loyd+2018b'),
                   Line2D([0], [1], color =  'k', ls= ':',lw=2.5, label=r'XUV | With Flares (factor 2.2)'),
                   Line2D([0], [1], color =  'k', ls= '--',lw=1.5, label=r'XUV | With Flares (factor 2.8)'),
                   Line2D([0], [1], color =  'Teal', ls= '-',lw=5, label=r'NUV | AU Mic | Tristan+2023'),
                   Line2D([0], [1], color =  'mediumturquoise', ls= '-',lw=5, label=r'SXR | AU Mic | Tristan+2023')]

plt.legend(handles=legend_elements, ncol=1,loc='lower left',frameon=False, fontsize = 15.8)

########################################## Ticks and labels #############################################

plt.ylim(3e-5,6e2)
#plt.xlim(1e26,2e35)
a = [1e26,1e28,1e30,1e32,1e34]
plt.xscale('log')
plt.xticks(ticks=a)
plt.locator_params(axis='x', nbins=len(a))
d = 25

plt.xlabel(r"Flare Energy (ergs)",fontsize=d)
plt.ylabel(r'Cumulative Flare Freq (d$^{-1}$)',fontsize=d)
plt.xticks(fontsize=d)
plt.yticks(fontsize=d)
plt.yscale('log')

########################################## Saving Figure #################################################

fig.savefig('FFD.png', bbox_inches="tight", dpi=600)
