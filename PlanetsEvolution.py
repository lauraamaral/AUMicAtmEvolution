"""
This script produces the Figure 4 from Amaral+2025. The figure presents
the evolution of the planets AU Mic b, c, and d, using VPLANET's ATMESC,
STELLAR, and FLARE modules. Panel a is the XUV Flux hitting the planets,
Panel b is the Hydrogen envelope mass in the atmosphere of the AU Mic
planets, Panel c is the planetary radius evolution and Panel d is the
hydrogen mass loss rate over time.

Laura N. R. do Amaral, Arizona State University (2024)
Date:  October 17th 2024
"""
import os
import pathlib
import subprocess
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import LogLocator, FormatStrFormatter

import vplanet as vlt

try:
    import vplot as vpl
except:
    print("Cannot import vplot. Please install vplot.")

path = pathlib.Path(__file__).parents[0].absolute()
sys.path.insert(1, str(path.parents[0]))
from get_args import get_args


################# Defining the directory where the data is #################
run = [
    "./SourceFiles/NoFlares",
    "./SourceFiles/Flares_2.8Factor",
    "./SourceFiles/Flares_2.2Factor",
]

def run_vplanet(dir):
         print("\nRunning simulation in %s directory..." % dir)
         os.chdir(dir)
         subprocess.call(['vplanet', 'vpl.in'])
         # Return to top-level directory
         os.chdir(path)
         return dir 

for i in run:
   run_vplanet(i)


results = [
    "./SourceFiles/NoFlares/star.b.forward",
    "./SourceFiles/Flares_2.8Factor/star.b.forward",
    "./SourceFiles/Flares_2.2Factor/star.b.forward",

    "./SourceFiles/NoFlares/star.c.forward",
    "./SourceFiles/Flares_2.8Factor/star.c.forward",
    "./SourceFiles/Flares_2.2Factor/star.c.forward",
 
    "./SourceFiles/NoFlares/star.d.forward",
    "./SourceFiles/Flares_2.8Factor/star.d.forward",
    "./SourceFiles/Flares_2.2Factor/star.d.forward",

    "./SourceFiles/NoFlares/star.b_max.forward",
    "./SourceFiles/Flares_2.8Factor/star.b_max.forward",
    "./SourceFiles/Flares_2.2Factor/star.b_max.forward",

    "./SourceFiles/NoFlares/star.c_max.forward",
    "./SourceFiles/Flares_2.8Factor/star.c_max.forward",
    "./SourceFiles/Flares_2.2Factor/star.c_max.forward",
 
    "./SourceFiles/NoFlares/star.d_max.forward",
    "./SourceFiles/Flares_2.8Factor/star.d_max.forward",
    "./SourceFiles/Flares_2.2Factor/star.d_max.forward",

    "./SourceFiles/NoFlares/star.b_min.forward",
    "./SourceFiles/Flares_2.8Factor/star.b_min.forward",
    "./SourceFiles/Flares_2.2Factor/star.b_min.forward",

    "./SourceFiles/NoFlares/star.c_min.forward",
    "./SourceFiles/Flares_2.8Factor/star.c_min.forward",
    "./SourceFiles/Flares_2.2Factor/star.c_min.forward",
 
    "./SourceFiles/NoFlares/star.d_min.forward",
    "./SourceFiles/Flares_2.8Factor/star.d_min.forward",
    "./SourceFiles/Flares_2.2Factor/star.d_min.forward"
]

################################## Loading the data #########################
age = []
FXUV = []
PlanetRadius = []
EnvelopeMass = []
DEnvMassDt = []

range_folders = 3
for i in range(0, len(results)):#range_folders):
    age.append(np.genfromtxt(results[i], usecols=(4), unpack=True))
    PlanetRadius.append(np.genfromtxt(results[i], usecols=(2), unpack=True))
    EnvelopeMass.append(np.genfromtxt(results[i], usecols=(3), unpack=True))
    FXUV.append(np.genfromtxt(results[i], usecols=(1), unpack=True))
    DEnvMassDt.append(np.genfromtxt(results[i], usecols=(5), unpack=True)*-1)
 
############################## Plot #########################################
fig, axes = plt.subplots(nrows=2, ncols=2, sharex=True, figsize=(25,17))

time = age[0]/1e6

cmap = ['#FF9524', #gold
        '#A50C37', #red
        '#078AED' #blue
]
cmap = [i for i in cmap for _ in range(3)]

cmap_vertical = ['#FFC1CB', #pink
                 '#257E60' #green
]

# alpha value
a = 0.2
d = 0.99

# linewidth
b = 2

ls = ["-","--",":"]*3
panel = ['a','b','c','d']

list = ['a', 'b', 'c']

range_folders = 3
for i in range(0,9):
    axes[1,1].plot(time, DEnvMassDt[i], color=cmap[i], alpha=d, lw=b, ls=ls[i])
    axes[1,0].plot(time, PlanetRadius[i], color=cmap[i], alpha=d, lw=b, ls=ls[i])
    axes[0,1].plot(time, EnvelopeMass[i], color=cmap[i], alpha=d, lw=b, ls=ls[i])
    axes[0,0].plot(time, FXUV[i], color=cmap[i], alpha=d, lw=b, ls=ls[i])

for i in range(0,3):
   axes[0,1].fill_between(time, EnvelopeMass[i*3+19], EnvelopeMass[i*3+9], color=cmap[i*3], alpha=a)
   axes[1,0].fill_between(time, PlanetRadius[i*3+19], PlanetRadius[i*3+9], color=cmap[i*3], alpha=a)
   axes[1,1].fill_between(time, DEnvMassDt[i*3+19], DEnvMassDt[i*3+9], color=cmap[i*3], alpha=a)

for j in range(0,2):
  for i in range(0,2):
    axes[i,j].tick_params(axis='x', labelsize=40)
    axes[i,j].tick_params(axis='y', labelsize=40)
    axes[i,j].set_xscale("log")
    axes[i,j].axvline(x = 23, linestyle = '-', color= cmap_vertical[0], alpha = 1, lw = 2,label ='AU Mic Age')
    axes[i,j].axvspan(20, 26, alpha=a, color= cmap_vertical[0])
    axes[i,j].axvline(x = 149, color = cmap_vertical[1], linestyle = '-', alpha = 1,lw = 2)
    axes[i,j].axvspan(130, 200, alpha=a, color= cmap_vertical[1])

axes[0,0].set_title(panel[0], x=0.95, y=1.0, fontsize = 55)
axes[0,1].set_title(panel[1], x=0.95, y=1.0, fontsize = 55)
axes[1,0].set_title(panel[2], x=0.95, y=1.0, fontsize = 55)
axes[1,1].set_title(panel[3], x=0.95, y=1.0, fontsize = 55)

axes[0,1].set_yscale("log")    
axes[1,1].set_yscale("log") 

axes[0,0].text(17.5,32, 'AU Mic Age', rotation=90, fontsize = 32, color = 'k')
axes[0,0].text(114,27, 'Saturation Time', rotation=90, fontsize = 33, color = 'k')

axes[0,0].set_ylim(-1,50)
axes[1,1].set_ylim(0.0,0.001)

axes[1,1].set_ylabel(r"Mass Loss Rate (M$_{\oplus}$/Myr)",fontsize = 39)
axes[1,0].set_ylabel(r"Planetary Radius (R$_{\oplus}$)",fontsize = 39)
axes[0,1].set_ylabel(r"Hydrogen Envelope Mass (M$_{\oplus}$)",fontsize = 39)
axes[0,0].set_ylabel(r"XUV Flux (W/m$^{2}$)",fontsize = 39)
axes[1,1].set_xlabel("Stellar Age (Myr)",fontsize =40)
axes[1,0].set_xlabel("Stellar Age (Myr)",fontsize =40)

##################################### Legend ###########################################

legend_elements = [Line2D([0], [0], color =  cmap[0], lw = 8, label=r'AU Mic b'),
                   Line2D([0], [0], color =  cmap[3], lw = 8, label=r'AU Mic c'),
                   Line2D([0], [0], color =  cmap[6], lw = 8, label=r'AU Mic d'),
                   Line2D([0], [0], color =  'k', ls= '-',  lw = 6,  label=r'No Flares'),
                   Line2D([0], [0], color =  'k', ls= '--', lw = 6, label=r'With Flares (factor 2.8)'),
                   Line2D([0], [0], color =  'k', ls= ':',  lw = 6,label=r'With Flares (factor 2.2)')
   
   ]

axes[0,1].legend(
    handles=legend_elements,
    loc='lower right',
    ncol=1,
    fontsize=23.0,
    frameon=False,
    
)


########################## Formating the axes ########################################

tick_values = [10,23, 50,149, 1000,5000]

for ax in axes.flatten():
    # Format x axis
    ax.set_xlim(time[0], 5000)
    # Set rasterization
    ax.set_rasterization_zorder(0)
    #ax.set_xticks(ticks=a)
    #ax.locator_params(axis='x', nbins=5)
    # Use LogLocator to place ticks at the specified locations
    ax.tick_params(which='major', width=1.0)
    ax.tick_params(which='major', length=8)
    ax.tick_params(which='minor', width=0.75)
    ax.tick_params(which='minor', length=5.5)
    ax.xaxis.set_major_locator(LogLocator(base=10, subs=(1.0,), numticks=10))
    ax.xaxis.set_minor_locator(LogLocator(base=10, subs='auto', numticks=10))

    # Use FormatStrFormatter to format tick labels as plain numbers
    ax.xaxis.set_major_formatter(FormatStrFormatter('%g'))


    # Customize the ticks
    ax.set_xticks(tick_values)
    
# Saving figure
plt.savefig("PlanetsEvolution.png", dpi = 200)
