"""
This script produces a version of the Figure 1 from Amaral+2025, the
Stellar luminosity evolution of M dwarf stars between 0.2 and 0.6 Msun,
 using VPLANET's STELLAR and FLARE modules.

Laura N. R. do Amaral, Arizona State University 2024
Date:  July 2024
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

#for i in run:
#   run_vplanet(i)
    

results = ["./SourceFiles/NoFlares/star.star.forward",
    "./SourceFiles/Flares_2.8Factor/star.star.forward",
    "./SourceFiles/Flares_2.2Factor/star.star.forward"]


# Loading the data
time = []
LXUVTot = []
LXUVBody = []
Lum = []


for i in range(0,3):
    Lum.append(np.genfromtxt(results[i], usecols=(1), unpack=True))
    LXUVTot.append(np.genfromtxt(results[i], usecols=(2), unpack=True))
    LXUVBody.append(np.genfromtxt(results[i], usecols=(3), unpack=True))
    time.append(np.genfromtxt(results[i], usecols=(4), unpack=True))
    

    

# Plot
fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(16,31))


time = time[0]/1e6


cmap = [vpl.colors.red,
    vpl.colors.dark_blue,
    '#FFC1CB',
        '#257E60',
        'midnightblue'
]

# alpha value
a = 0.6
d = 0.99

# linewidth
b = 4.5
c = 2.5
rangeplot = 3
ls = ['-','--',':']
panel = ['a','b','c','d','e']
## Upper left: Bolometric Luminosity #

for i in range(0,3):
    #axes[0].plot(time, Lum[i], color='k', alpha=d, lw=b, ls=ls[i])
    axes[0].plot(time, LXUVTot[i], color=cmap[4], alpha=d, lw=b, ls=ls[i])
    
for i in range(1,3):
    L = 0
    L = LXUVTot[i]/LXUVBody[i]
    axes[1].plot(time, LXUVBody[i], color=cmap[4], alpha=d, lw=b, ls=ls[i])
    axes[2].plot(time, L, color=cmap[4], alpha=d, lw=b, ls='-')#ls=ls[i])# XUVBody[i]/LXUVTot[i]
    #axes[2].plot(time,time, color=cmap[4], alpha=d, lw=b, ls='-')
    #axes[2].scatter(x, y, s, c, marker = value3)
for i in range(0,rangeplot):
    axes[i].tick_params(axis='x', labelsize=40)
    axes[i].tick_params(axis='y', labelsize=40)
    axes[i].set_xscale("log")
    axes[i].axvline(x = 149, color = cmap[3], linestyle = '-', alpha = 1,lw = 2)
    axes[i].axvspan(20, 26, alpha=0.3, color= cmap[2])
    axes[i].axvline(x = 23, linestyle = '-', color= cmap[2], alpha = 1, lw = 2,label ='AU Mic Age')
    axes[i].axvspan(130, 200, alpha=0.3, color= cmap[3])
    axes[i].set_title(panel[i], x=0.95, y=1.0, fontsize = 55)

axes[1].set_yscale("log")
axes[0].text(18,2e-7, 'AU Mic Age', rotation=90, fontsize = 41, color = 'k') 
axes[0].text(117, 2e-7, 'Saturation Time', fontsize = 42,rotation = 90, color = 'k')
axes[0].set_yscale("log") 
axes[2].set_xlabel("Stellar Age (Myr)", fontsize = 39)
axes[0].set_ylabel(r"L$_{XUV,Total}$ (L$_{\odot}$)", fontsize = 46)
axes[1].set_ylabel(r"L$_{XUV,Flare}$ (L$_{\odot}$)", fontsize = 47)
axes[2].set_ylabel(r"L$_{XUV,Flare}$/L$_{XUV,Total}$", fontsize = 40)
axes[0].set_ylim(1e-7, 8e-4)
axes[1].set_ylim(1e-7, 8e-4)
#axes[2].set_ylim(0, 0.5)
# Legend
legend_elements = [Line2D([0], [0], color =  cmap[4], ls= '-',  lw = 8,  label=r'No Flares'),
                   Line2D([0], [0], color =  cmap[4], ls= '--', lw = 8, label=r'With Flares (factor 2.8)'),
                   Line2D([0], [0], color =  cmap[4], ls= ':',  lw = 8,label=r'With Flares (factor 2.2)')]

axes[0].legend(
    handles=legend_elements,
    loc="upper right",
    ncol=1,
    fontsize=37,
    frameon=False,
)

legend_elements2 = [Line2D([0], [0], color =  'k', ls= '-',  lw = c,  label=r'Bolometric Quiescent')]

'''axes[0].legend(
    handles=legend_elements2,
    loc="upper right",
    ncol=1,
    fontsize=14.5,
    frameon=False,
)'''

#tick_values = [10, 23, 149, 1000, 5000]


from matplotlib.ticker import LogLocator, FormatStrFormatter

# Format all axes
for ax in axes.flatten():
    # Format x axis
    ax.set_xlim(time[0], 5000)
    # Set rasterization
    ax.set_rasterization_zorder(0)
    #ax.set_xticks(ticks=a)
    #ax.locator_params(axis='x', nbins=5)
    # Use LogLocator to place ticks at the specified locations
    ax.tick_params(which='major', width=1.0)
    ax.tick_params(which='major', length=10)
    ax.tick_params(which='minor', width=0.75)
    ax.tick_params(which='minor', length=5.5)
    ax.xaxis.set_major_locator(LogLocator(base=10, subs=(1.0,), numticks=10))
    ax.xaxis.set_minor_locator(LogLocator(base=10, subs='auto', numticks=10))

    # Use FormatStrFormatter to format tick labels as plain numbers
    ax.xaxis.set_major_formatter(FormatStrFormatter('%g'))
    
    # Customize the ticks
    #ax.set_xticks(tick_values)



# Saving figure
plt.savefig("StellarEvolution.png", dpi = 200)
