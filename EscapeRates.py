"""
This script produces the Figure 3 from Amaral+2025. The figure presents
the escape rates of the planets AU Mic b, c, and d, at 23 Myrs,
using VPLANET's ATMESC, STELLAR, and FLARE modules.

Laura N. R. do Amaral, Arizona State University (2024)
Date:  January 11th 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.legend_handler import HandlerLine2D


################# Defining functions #########################
#converting M_earth/Myr to g/s

Me = 5.972e27 # in grams
Myrs = 3.15576e13 # in seconds
ratio = Me/Myrs

def Me_Myrs2g_s(rate):
    return rate*ratio

################# Defining the directory where the data is #################

folders = [
    "./SourceFiles/Flares_2.8Factor/star.b.forward",
    "./SourceFiles/Flares_2.2Factor/star.b.forward",
    "./SourceFiles/NoFlares/star.b.forward",
    
    "./SourceFiles/Flares_2.8Factor/star.c.forward",
    "./SourceFiles/Flares_2.2Factor/star.c.forward",
    "./SourceFiles/NoFlares/star.c.forward",

    "./SourceFiles/Flares_2.8Factor/star.d.forward",
    "./SourceFiles/Flares_2.2Factor/star.d.forward",
    "./SourceFiles/NoFlares/star.d.forward",

    "./SourceFiles/Flares_2.8Factor/star.d_earth_equiv.forward",
    "./SourceFiles/Flares_2.2Factor/star.d_earth_equiv.forward",
    "./SourceFiles/NoFlares/star.d_earth_equiv.forward"
]

data = []

for i in range(0, len(folders)):
    data.append(((np.genfromtxt(folders[i], usecols=(4), unpack=True)),      
                      (np.genfromtxt(folders[i], usecols=(5), unpack=True))))

################################## Loading the data #########################

escaperate = []

for i in range(len(data[0][0])):
    for j in range(len(folders)):
        if data[0][0][i]== 2.3000000000e+07:
            escaperate.append((Me_Myrs2g_s(data[j][1][i])*(-1)))

Results = [ ('Carolan+2020', 3.2e10,0,0,0),
            ('Carolan+2020', 6.5e10,0,0,0),
            ('Hirano+2020', 2.841e10,0,0,0),
            ('Hirano+2020', 8.511e10,0,0,0),
            ('Feinstein+2022', 1.6e8,0,0,0),
            ('Feinstein+2022', 2.5e8,0,0,0),
            ('Feinstein+2022', 1e14,0,0,0),
            ('Spinelli+2023', 1.51356e11,0,0,0),
            ('Spinelli+2023', 1.94984e11,0,0,0),
            ('Rockcliffe+2023', 2.25e11,0,0,0),
            ('Rockcliffe+2023', 4.44e11,0,0,0),
            ('Mallorquín+2024', 1.42e12,7.59e10,0,0),
            (r'Single Flare | 10$^{34.45}$ ergs', 3.62e13, 9.36e12, 2.72e12, 7.91e11),# XUV energy
            (r'Single Flare | 10$^{28.45}$ ergs', 1.20e11, 3.10e10, 9.02e9, 4e8), # XUV energy
            #(r'Single Flare | 10$^{28}$ ergs', 1.16e11, 3.01e10, 8.76e9), # FUV energy
            #(r'Single Flare | 10$^{34}$ ergs', 2.16e13, 5.59e12, 1.63e12),# FUV energy
            ('With Flares (factor 2.8)',escaperate[0],escaperate[3],escaperate[6],escaperate[9]),
            ('With Flares (factor 2.2)',escaperate[1],escaperate[4],escaperate[7],escaperate[10]),
            ('No Flares',escaperate[2],escaperate[5],escaperate[8],escaperate[11])]


################################################### Plot ####################################################
 
hfont = {'fontname':'Times'}
size = 200
size2 = 25

symbol = ['*','o']

color = 'k'
a = 0.6
b = 0.6
c = 0.8

cmap = ['#FF9524',
        '#078AED',
        '#A50C37',
        'forestgreen',
        'k'
]

plt.figure(figsize=(9.5, 6))
plt.grid(True, color = 'peru', alpha = 0.2)

for i in range(len(Results)):
    if 0 <= i < 6 or 6 < i < 11:
        plt.scatter(Results[i][1],Results[i][0], color = cmap[0], marker = symbol[1], s = size, edgecolor=color,alpha = b)
    if i == 6:
        plt.scatter(Results[i][1],Results[i][0], color = cmap[0], marker = symbol[0], s = size, edgecolor=color,alpha = b)
    if i == 11:
        plt.scatter(Results[i][1],Results[i][0], color = cmap[0], marker = symbol[1], s = size, edgecolor=color,alpha = b)
        plt.scatter(Results[i][2],Results[i][0], color = cmap[2], marker = symbol[1], s = size, edgecolor=color,alpha = b)
    if i >= 14:
        plt.scatter(Results[i][1],Results[i][0], color = cmap[0], marker = symbol[1], s = size, edgecolor=color,alpha = b)
        plt.scatter(Results[i][2],Results[i][0], color = cmap[2], marker = symbol[1], s = size, edgecolor=color,alpha = b)
        plt.scatter(Results[i][3],Results[i][0], color = cmap[1], marker = symbol[1], s = size, edgecolor=color,alpha = b)
        plt.scatter(Results[i][4],Results[i][0], color = cmap[3], marker = symbol[1], s = size, edgecolor=color,alpha = b)
    if 12 <= i <= 13:
        plt.scatter(Results[i][1],Results[i][0], color = cmap[0], marker = symbol[0], s = size, edgecolor=color,alpha = b)
        plt.scatter(Results[i][2],Results[i][0], color = cmap[2], marker = symbol[0], s = size, edgecolor=color,alpha = b)
        plt.scatter(Results[i][3],Results[i][0], color = cmap[1] , marker = symbol[0], s = size, edgecolor=color,alpha = b)
        plt.scatter(Results[i][4],Results[i][0], color = cmap[3] , marker = symbol[0], s = size, edgecolor=color,alpha = b)

plt.xscale('log')
plt.xlabel(r'Escape Rate (g/s)', fontsize = 23, **hfont)
plt.xticks(fontsize=23, **hfont)
plt.yticks(fontsize=20, **hfont)
plt.tight_layout()

###################################################### Legend ############################################################

legend_elements = [
    plt.Line2D([0], [0], marker='s',color='w',markersize=13, markerfacecolor= cmap[0],markeredgecolor='slategray',alpha = b, label='AU Mic b'),
    plt.Line2D([0], [0], marker='s',color='w',markersize=13, markerfacecolor= cmap[2],markeredgecolor='slategray',alpha = b, label='AU Mic c'),
    plt.Line2D([0], [0], marker='s',color='w',markersize=13, markerfacecolor= cmap[1],markeredgecolor='slategray',alpha = b, label='AU Mic d'),
    plt.Line2D([0], [0], marker='s',color='w',markersize=13, markerfacecolor= cmap[3],markeredgecolor='slategray',alpha = b, label='AU Mic d at the HZ'),
    plt.Line2D([0], [0], marker='*',color='w',markersize=13, markerfacecolor= cmap[4],markeredgecolor='slategray',alpha = b, label=r'Single Flare')
]

plt.legend(
    handles=legend_elements,
    loc='upper right',
    fontsize=19.5,
    frameon=False,
    prop={'family': 'serif','size': 12}
)

####################################################### Saving Figure ############################################################

plt.savefig('EscapeRates.png',dpi = 300)
