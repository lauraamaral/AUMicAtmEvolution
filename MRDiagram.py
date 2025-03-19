import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd
import seaborn as sns
from matplotlib.patches import FancyArrowPatch
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle

################################# Importing the files ###################################

path_33Fe_68MgSiO3 = './SourceFiles/MassRadiiData/Mass-Radii-relation-325Fe_675MgSiO3.csv'
path_5H = './SourceFiles/MassRadiiData/Mass-Radii-relation-5H.csv'
path_2H = './SourceFiles/MassRadiiData/Mass-Radii-relation-2H.csv'
path_100Fe = './SourceFiles/MassRadiiData/Mass-Radii-relation-100Fe.csv'
path_100MgSiO3= './SourceFiles/MassRadiiData/Mass-Radii-relation-100MgSiO3.csv'
path_EarthH = './SourceFiles/MassRadiiData/Mass-Radii-relation-EarthH.csv'
path_PureH2O = './SourceFiles/MassRadiiData/Mass-Radii-relation-PureH2O.csv'
path_EarthH2O = './SourceFiles/MassRadiiData/Mass-Radii-relation-EarthH2O.csv'

Fe33_68MgSiO3 = pd.read_csv(path_33Fe_68MgSiO3).values
Earth5H = pd.read_csv(path_5H).values
Earth2H = pd.read_csv(path_2H).values
Fe100 = pd.read_csv(path_100Fe).values
MgSiO3100 = pd.read_csv(path_100MgSiO3).values
EarthH = pd.read_csv(path_EarthH).values
EarthH2O = pd.read_csv(path_EarthH2O).values

Fe33_68MgSiO3 = Fe33_68MgSiO3.T
Earth5H = Earth5H.T
Earth2H = Earth2H.T
Fe100 = Fe100.T
MgSiO3100 = MgSiO3100.T
EarthH = EarthH.T
EarthH2O = EarthH2O.T

radii = []
mass = []
age = []


folders = [
    "./SourceFiles/Flares_2.8Factor/star.b.forward",
    "./SourceFiles/Flares_2.8Factor/star.c.forward",
    "./SourceFiles/Flares_2.8Factor/star.d.forward",

    "./SourceFiles/Flares_2.8Factor/star.b_max.forward",
    "./SourceFiles/Flares_2.8Factor/star.c_max.forward",
    "./SourceFiles/Flares_2.8Factor/star.d_max.forward",
  
    "./SourceFiles/Flares_2.8Factor/star.b_min.forward",    
    "./SourceFiles/Flares_2.8Factor/star.c_min.forward",
    "./SourceFiles/Flares_2.8Factor/star.d_min.forward"]



for i in range(0, len(folders)):
    radii.append(np.genfromtxt(folders[i], usecols=(2), unpack=True))
    age.append(np.genfromtxt(folders[i], usecols=(4), unpack=True))
    mass.append(np.genfromtxt(folders[i], usecols=(7), unpack=True))

mass10 = []
radii10 = []

mass23 = []
radii23 = []

mass5 = []
radii5 = []

# AU Mic b, c, d  
# list[0,1,2] = mean values
# list[3,4,5] = max values
# list[6,7,8] = min values
for i in range(len(age[0])):
################################# mean ##################################
        if age[0][i]== 1.0000000000e+07:
            mass10.append(((mass[0][i],(mass[0][i]-mass[6][i]),(mass[3][i]-mass[0][i])),
                          (mass[1][i],(mass[1][i]-mass[7][i]),(mass[4][i]-mass[1][i])),
                          (mass[2][i],(mass[2][i]-mass[8][i]),(mass[5][i]-mass[2][i]))))
            radii10.append(((radii[0][i],(radii[0][i]-radii[6][i]),(radii[3][i]-radii[0][i])),
                           (radii[1][i],(radii[1][i]-radii[7][i]),(radii[4][i]-radii[1][i])),
                           (radii[2][i],(radii[8][i]-radii[2][i]),(radii[2][i]-radii[5][i]))))
        if age[0][i]== 2.3000000000e+07: 
            mass23.append(((mass[0][i],(mass[0][i]-mass[6][i]),(mass[3][i]-mass[0][i])),
                          (mass[1][i],(mass[1][i]-mass[7][i]),(mass[4][i]-mass[1][i])),
                          (mass[2][i],(mass[2][i]-mass[8][i]),(mass[5][i]-mass[2][i]))))
            radii23.append(((radii[0][i],(radii[0][i]-radii[6][i]),(radii[3][i]-radii[0][i])),
                           (radii[1][i],(radii[1][i]-radii[7][i]),(radii[4][i]-radii[1][i])),
                           (radii[2][i],(radii[2][i]-radii[8][i]),(radii[5][i]-radii[2][i]))))
        if age[0][i]== 5.0000000000e+09:
            mass5.append(((mass[0][i],(mass[0][i]-mass[6][i]),(mass[3][i]-mass[0][i])),
                          (mass[1][i],(mass[1][i]-mass[7][i]),(mass[4][i]-mass[1][i])),
                          (mass[2][i],(mass[2][i]-mass[8][i]),(mass[5][i]-mass[2][i]))))
            radii5.append(((radii[0][i],(radii[0][i]-radii[6][i]),(radii[3][i]-radii[0][i])),
                           (radii[1][i],(radii[1][i]-radii[7][i]),(radii[4][i]-radii[1][i])),
                           (radii[2][i],(radii[2][i]-radii[8][i]),(radii[5][i]-radii[2][i]))))

mass10 = np.array(mass10[0]).T
radii10 = np.array(radii10[0]).T
mass23 = np.array(mass23[0]).T
radii23 = np.array(radii23[0]).T
mass5 = np.array(mass5[0]).T
radii5 = np.array(radii5[0]).T
################################ Plot ########################

size = 1500
alpha = 1
fontsize = 25
hfont = {'fontname':'Times'}

cmap = ['#E40303','#FF8C00','gold','#008026','#004CFF','#732982','#21B0FE']
cmapplanets= ['#FF9524',
              '#A50C37',
              '#078AED',
              'midnightblue']

plt.figure(figsize=(13, 20))

# EarthH[2] = 0.1H_300K
plt.plot(EarthH[0],EarthH[2], color = cmap[1])#,ls = '--')
plt.text(1.7,1.4,  r'0.1% H$_{2}$, 300K', fontsize=fontsize, fontweight='bold', color=cmap[1], ha='center', va='center',rotation = 6,**hfont)

# EarthH[3] = 1H_500K
plt.plot(EarthH[0],EarthH[3], color = cmap[3])#,ls = ':')
plt.text(1.8,2.24, r'1% H$_{2}$, 500K', fontsize=fontsize, fontweight='bold', color=cmap[3], ha='center', va='center',rotation = -15,**hfont)

# EarthH[4] = 0.1H_500K
plt.plot(EarthH[0],EarthH[4], color = cmap[2])#,ls = '--')
plt.text(1.7,1.7, r'0.1% H$_{2}$, 500K', fontsize=fontsize, fontweight='bold', color= cmap[2], ha='center', va='center',rotation = -1,**hfont)

# Earth5H[2] = 5H_500K
plt.plot(Earth5H[0],Earth5H[2], color =cmap[5])#,ls = '-.')
plt.text(6.6,3.8, r'5% H$_{2}$, 500K', fontsize=fontsize, fontweight='bold', color=cmap[5], ha='center', va='center',rotation = -22,**hfont)

# Fe33_68MgSiO3[1] = Fe33_68MgSiO3
plt.plot(Fe33_68MgSiO3[0],Fe33_68MgSiO3[1], color = cmap[0])
plt.text(10,1.75, r'Earth-like, 32.5$\%$Fe+67.5$\%$MgSiO$_{3}$', fontsize=fontsize+1, fontweight='bold', color= cmap[0], ha='center', va='center',rotation = 31,**hfont)

# Earth2H[2] = 2H_500K
plt.plot(Earth2H[0][1::],Earth2H[2][1::], color =cmap[4])
plt.text(1.85,2.84, r'2% H$_{2}$, 500K', fontsize=fontsize, fontweight='bold', color=cmap[4], ha='center', va='center',rotation = -36,**hfont)

############################ Adding AU Mic Planets error bars ####################################

for i in range(3):
    plt.errorbar(mass10[0].tolist()[i], radii10[0].tolist()[i], radii10[1:3][0][i],  mass10[1:3][0][i], fmt='', capsize=7, color = 'gray', alpha = 0.9)
    plt.errorbar(mass23[0].tolist()[i], radii23[0].tolist()[i], radii23[1:3][0][i],  mass23[1:3][0][i], fmt='', capsize=7, color = 'gray', alpha = 0.9)
    plt.errorbar(mass5[0].tolist()[i], radii5[0].tolist()[i], radii5[1:3][0][i],  mass5[1:3][0][i], fmt='', capsize=7, color = 'gray', alpha = 0.9)
    plt.scatter(mass10[0].tolist()[i],radii10[0].tolist()[i], color = cmapplanets [i], marker = "^", s = 500, edgecolor='black',alpha = 0.5)
    plt.scatter(mass23[0].tolist()[i],radii23[0].tolist()[i], color = cmapplanets [i], marker = "*", s = size, edgecolor='black',alpha = alpha)
    plt.scatter(mass5[0].tolist()[i],radii5[0].tolist()[i], color = cmapplanets [i], marker = "D", s = 500, edgecolor='black',alpha = 0.5)

################################## Adding Solar System Planets ##################################

mass_earth = 5.97237e24
radius_earth = 6371.0

planets_list = [
    ['♀', 4.8675e24 / mass_earth, 6051.8 / radius_earth, 'Venus',0.815, 5500.8 / radius_earth],
    ['⊕', 1.0, 1.0,'Earth',1.1, 0.87],
    ['♅', 8.6810e25 / mass_earth, 25362.0 / radius_earth, 'Uranus',19.5,25362.0 / radius_earth],
    ['♆', 1.02413e26 / mass_earth, 24622.0 / radius_earth, 'Neptune',24, 24622.0 / radius_earth]
]

for i in range(len(planets_list)):
    plt.scatter(planets_list[i][1],planets_list[i][2], color = cmapplanets[3], marker = "o", s = 500,alpha =0.6)
    plt.text(planets_list[i][4],planets_list[i][5], planets_list[i][3], fontsize=22, fontweight='bold', color= cmapplanets[3], ha='center', va='center',**hfont)

############################################ Legend #############################################

legend_elements = [plt.Line2D([0], [0], marker='o',color='w',markersize=28, markerfacecolor= cmapplanets[3],markeredgecolor= cmapplanets[3],alpha = 0.6, label='Solar System Planets at 4.57 Gyrs'),
    plt.Line2D([1], [0], marker='s',color='w',markersize=26, markerfacecolor= cmapplanets[0],markeredgecolor='k',alpha = 0.6, label='AU Mic b'),
    plt.Line2D([1], [0], marker='s',color='w',markersize=26, markerfacecolor= cmapplanets[1],markeredgecolor='k',alpha = 0.6, label='AU Mic c'),
    plt.Line2D([1], [0], marker='s',color='w',markersize=26, markerfacecolor= cmapplanets[2],markeredgecolor='k',alpha = 0.6, label='AU Mic d'),
    plt.Line2D([0], [0], marker='^',color='w',markersize=28, markerfacecolor='k',markeredgecolor='k',alpha = 0.3, label='10 Myrs'),
    plt.Line2D([0], [0], marker='*',color='w',markersize=28, markerfacecolor='k',markeredgecolor='k',alpha = alpha,label='23 Myrs'),
    plt.Line2D([0], [0], marker='D',color='w',markersize=24, markerfacecolor='k',markeredgecolor='k',alpha = 0.3, label='5 Gyrs')
]

plt.legend(
    handles=legend_elements,
    loc='upper left',
    frameon=True,
    numpoints=1,
    prop={'family': 'serif','size': 20}
)


#################### Labels and ticks ######################

ticks = [1,1.5,2,3,4,5,10,15,35]
plt.xlim(0.5,35)
plt.ylim(0.5,5.7)
plt.xscale('symlog')
plt.xlabel(r'Planetary Mass (M$_{\oplus}$)',fontsize = 39, **hfont)
plt.ylabel(r'Planetary Radius (R$_{\oplus}$)',fontsize = 39, **hfont)
plt.xticks(ticks, labels= [1,1.5,2,3,4,5,10,15,35],fontsize = 33, **hfont)
plt.yticks(fontsize = 33, **hfont)


################### Saving Figure ##########################

plt.savefig('MRDiagram.png',dpi = 300)
