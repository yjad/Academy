#libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd


def plot_stacked_bar(bars1, bars2, names, file_name):

    print ("lengths: ", len(bars1), len(bars2), len(names))
    # y-axis in bold
    rc('font', weight='bold')

    # Values of each group
    # bars1 = [12, 28, 1, 8, 22]
    # bars2 = [28, 7, 16, 4, 10]
    # bars3 = [25, 3, 23, 25, 17]

    # Heights of bars1 + bars2
    bars = np.add(bars1, bars2).tolist()

    # The position of the bars on the x-axis
    #r = [0,1,2,3,4]
    #x = len(bars1)
    r = [i for i in range  (0,len(bars1))]
    # Names of group and bar width
    #names = ['A','B','C','D','E']
    if len(bars1) < 10:
        barWidth = 1
    else:
        barWidth = 1

    # Create brown bars
    plt.bar(r, bars1, color='#7f6d5f', edgecolor='white', width=barWidth, label= 'Academy Students')
    # Create green bars (middle), on top of the firs ones
    plt.bar(r, bars2, bottom=bars1, color='#557f2d', edgecolor='white', width=barWidth, label='External')
    # Create green bars (top)
    #plt.bar(r, bars3, bottom=bars, color='#2d7f5e', edgecolor='white', width=barWidth)

    # Create legend
    plt.legend()

    # Custom X axis
    plt.xticks(r, names, fontweight='normal', rotation=90)
    #plt.xticks(r, names, rotation=90)
    plt.xlabel("Zoom Meeting Date")

    plt.subplots_adjust(bottom=0.25, top=0.96)

    # Show graphic
    #plt.show()
    plt.savefig(file_name)