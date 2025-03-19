"""
This script produces a version of the Figure 6 from Amaral+2025,
using VPLANET's STELLAR and FLARE modules. Panel a is the XUV
flux hitting the AU Mic d when placed at different distances
from its host star.

Laura N. R. do Amaral, Arizona State University (2024)
Date: October 14th 2024
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


# Defining the directory where the data is
run = [
    "./SourceFiles/NoFlaresDiffFlux",
    "./SourceFiles/FlaresDiffFlux" 
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


folders = [
    "./SourceFiles/NoFlaresDiffFlux/stellar.closein.forward",
    "./SourceFiles/NoFlaresDiffFlux/stellar.d.forward",
    "./SourceFiles/NoFlaresDiffFlux/stellar.HZ.forward",
    "./SourceFiles/NoFlaresDiffFlux/stellar.innerlimit.forward",
    "./SourceFiles/NoFlaresDiffFlux/stellar.max.forward",
    "./SourceFiles/NoFlaresDiffFlux/stellar.outerlimit.forward",
    "./SourceFiles/FlaresDiffFlux/flare.closein.forward",
    "./SourceFiles/FlaresDiffFlux/flare.d.forward",
    "./SourceFiles/FlaresDiffFlux/flare.HZ.forward",
    "./SourceFiles/FlaresDiffFlux/flare.innerlimit.forward",
    "./SourceFiles/FlaresDiffFlux/flare.max.forward",
    "./SourceFiles/FlaresDiffFlux/flare.outerlimit.forward"
    ]


############################### Loading the data ##############################
age = []
FXUV = []
EnvelopeMass = []

for i in range(0, len(folders)):
    EnvelopeMass.append(np.genfromtxt(folders[i], usecols=(3), unpack=True))
    FXUV.append(np.genfromtxt(folders[i], usecols=(1), unpack=True))
    age.append((np.genfromtxt(folders[i], usecols=(4), unpack=True))/1e6)


############################## Plot ##############################
fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(11,16))

time = age[0]

cmap = ['#E40303','#FF8C00','#008026','#FFED00','#004CFF','#732982']*2
cmap2 = ['#FFC1CB','#257E60']


# alpha value
a = 0.6
d = 0.99
e = 3.5
f = 3
# linewidth
b = 4
c = 2

ls = ["-","-","-","-","-","-","--","--","--","--","--","--"
panel = ['a','b','c','d']
lw = [4,4,4,4,4,4]*2
alpha = [1,1,1,1,1,1]*2

for i in range(0,len(folders)):
    axes[1].plot(time, EnvelopeMass[i], color=cmap[i], alpha=alpha[i], ls=ls[i],lw =lw[i])
    axes[0].plot(time, FXUV[i]        , color=cmap[i], alpha=alpha[i], ls=ls[i],lw =lw[i])

for i in range(0,2):
    axes[i].tick_params(axis='x', labelsize=23)
    axes[i].tick_params(axis='y', labelsize=28)
    axes[i].set_xscale("log")
    axes[i].set_xlim(10,25)
    axes[i].axvline(x = 23, linestyle = '-', color=cmap2[0], alpha = 1, lw = 2,label ='AU Mic Age')
    axes[i].axvspan(20, 26, alpha=0.3, color=cmap2[0])
    axes[i].axvline(x = 149, color = cmap2[1], linestyle = '-', alpha = 1,lw = 2)
    axes[i].axvspan(130, 200, alpha=0.3, color=cmap2[1])
    axes[i].set_title(panel[i], x=0.95, y=1.0, fontsize = 40)
    
axes[1].set_xlabel("Stellar Age (Myr)",fontsize =30)
axes[1].set_yscale("log")    
axes[0].set_yscale("log") 
axes[0].set_ylim(0,100000000)
axes[1].set_ylabel(r"Hydrogen Envelope Mass (M$_{\oplus}$)",fontsize = 28)
axes[0].set_ylabel(r"XUV Flux (W/m$^{2}$)",fontsize = 30)

############################### Legend ##############################
legend_elements = [Line2D([0], [0], color = cmap[0], lw = b, label=r'0.01 AU | Close-in'),
                   Line2D([0], [0], color = cmap[1], lw = b, label=r'0.0853 AU | Current Position'),
                   Line2D([0], [0], color = cmap[3], lw = b, label=r'0.28771 AU | HZ Inner Limit'),
                   Line2D([0], [0], color = cmap[2], lw = b, label=r'0.2935 AU | 1 AU Equivalent'),
                   Line2D([0], [0], color = cmap[4], lw = b, label=r'0.365 AU | Total Atmospheric Loss Limit'),
                   Line2D([0], [0], color = cmap[5], lw = b, label=r'0.538 AU | HZ Outer Limit'),
                   Line2D([0], [0], color = 'k', ls= '-', lw = b, label=r'No Flares'),
                   Line2D([0], [0], color = 'k', ls='--', lw = b, label=r'With Flares')
                   ]
axes[0].legend(
    handles=legend_elements,
    loc='upper right',
    ncol=1,
    fontsize=17.5,
    frameon=False,
    
)


tick_1 = [10,23,50,149,1000,5000]

# Format all axes
for ax in axes.flatten():
    # Format x axis
    ax.set_xlim(time[0], 5000)
    # Set rasterization
    ax.set_rasterization_zorder(0)
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
    ax.set_xticks(tick_1)

    
# Saving figure
plt.savefig("DiffFlux.png", dpi = 200)
