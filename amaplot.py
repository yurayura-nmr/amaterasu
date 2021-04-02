#! /usr/bin/env python

"""
Erik Walinda
Kyoto University
Graduate School of Medicine

Amaterasu
Plotting utility

Last change: 2018-2-22
"""

import nmrglue as ng
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm

from matplotlib import rcParams

"""
Run-specific parameters (to get from function call)
By default, one residue has <= 196 data
"""

datapath = "11"               # folder containing the fid and spectra
w_1H = 8.0577                 # where is the peak?
base_countour_level = 200000  # manual setting
startfid = 0  # 0 for 1(...).ft2
endfid = 178

columns = 14
rows = 14

"""
Plot parameters
"""
rcParams['axes.titlesize'] = 8
rcParams['xtick.labelsize'] = 0.5
rcParams['ytick.labelsize'] = 0.5
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Times New Roman']
rcParams['figure.figsize'] = 20, 20

def calculateCountours(base_countour_level):
    """
    Countour levels and colormap for countour plot
    """

    cmap = matplotlib.cm.seismic	
    cmapneg = cmap

    contour_start = base_countour_level
    contour_num = 20
    contour_factor = 1.2

    cl = contour_start * contour_factor ** np.arange(contour_num) 
    clneg = -cl[::-1]

    print "[ Amaplot ] Plotting positive contour levels:\n", cl
    print "[ Amaplot ] Plotting negative contour levels:\n", clneg

    return cl, clneg, cmap, cmapneg

def makePlot(datapath, startfid, endfid, cl, clneg, cmap, cmapneg):
    filecounter = startfid
    maxcounter = endfid

    fig, ax_array = plt.subplots(rows, columns)
    for i,ax_row in enumerate(ax_array):
        for j,axes in enumerate(ax_row):
            filecounter += 1
            if filecounter > maxcounter:
                axes.set_visible(False)   # avoid plotting empty panels
            else:
                axes.set_yticklabels([])
                axes.set_xticklabels([])

                """
                Read in data using nmrglue
                """
                # read in the data from a NMRPipe file
                filename = datapath + "/fid/" + str(filecounter) + ".fid_proc.ft2" # Amaterasu filename
                dic, data = ng.pipe.read(filename)

                # make ppm scales
                uc_1h = ng.pipe.make_uc(dic, data, dim=1)
                ppm_1h = uc_1h.ppm_scale()
                ppm_1h_0, ppm_1h_1 = uc_1h.ppm_limits()
                uc_15n = ng.pipe.make_uc(dic, data, dim=0)
                ppm_15n = uc_15n.ppm_scale()
                ppm_15n_0, ppm_15n_1 = uc_15n.ppm_limits()

                """
                Plot spectra using matplotlib
                Draw positve and negative countourlevels separately.
                Takes time, but prettier.
                """
                axes.set_title(str(filecounter), {'verticalalignment': 'baseline'})
                axes.contour(data, cl, cmap=cmap, extent=(ppm_1h_0, ppm_1h_1, ppm_15n_0, ppm_15n_1), linewidths=0.03)
                axes.contour(data, clneg, cmap=cmapneg, extent=(ppm_1h_0, ppm_1h_1, ppm_15n_0, ppm_15n_1), linewidths=0.03)
                axes.set_xlim(w_1H + 0.1, w_1H - 0.1) # zoom on __expected__ proton chemical shift

    #params = {'mathtext.default': 'regular' }          
    #plt.rcParams.update(params)

    fig.savefig("spectrum.pdf")

# Calculate contours
cl, clneg, cmap, cmapneg = calculateCountours(base_countour_level)

# Plot it!
makePlot(datapath, startfid, endfid, cl, clneg, cmap, cmapneg)
