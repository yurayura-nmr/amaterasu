import os
import sys

from a_cout import *


def writeIntFileHeader(residue, experiment):
    """
    Write intensity file for GLOVE
    Line 1: BF3              [MHz]
    Line 2: spinlock duration  [s]
    Line 3: spinlock power    [Hz]
    Line 4: spinlock offset   [Hz]
    """

    IntFile = open('./Int_r1rho' + '.txt', 'w')

    line1 = str(experiment.BF3)
    line2 = "0 0"  # Reference
    line3 = "0 0"  # Reference
    line4 = "0 0 "

    """
    Write non-reference spinlock powers to table

    Off-resonance R1rho dispersion is not implemented yet. 
    Thus, line 4 = 0 0 0 ...
    """

    for i in residue.fidObjectsData:
        i.spinlockHz = float(experiment.valist[i.index])
        if int(i.spinlockHz > 0):
            line2 = line2 + " " + str(experiment.spinLockLength)
            line3 = line3 + " " + str(i.spinlockHz)
            line4 = line4 + "0 "

    """
    Write header
    """

    IntFile.write(line1 + "\n")
    IntFile.write(line2 + "\n")
    IntFile.write(line3 + "\n")
    IntFile.write(line4 + "\n")


def writeIntFileLine(residue, experiment):
    """
    Write intensity list for current resonance
    """

    intensityLine = "1 " + str(residue.index) + " HN "

    """
    Write reference intensity
    """

    for i in residue.fidObjectsReference:
        intensityLine += str(i.intensity) + ' '

    """
    Write spin-lock dependent intensities
    """

    for i in residue.fidObjectsData:
        intensityLine += str(i.intensity) + ' '

    IntFile = open('./Int_r1rho.txt', 'a')
    IntFile.write(intensityLine + '\n')
    IntFile.close()


def glove(experiment, args):
    """
    Call glove to fit the created intensity file.
    To do: output filename needs adjustment.
    """

    temperature = str(round(experiment.TE))

    IntFile = 'Int_r1rho.txt'

    """
    Case: Matrix model

    r1rho2glove -t MATRIX_ON w1 -i Int_r1rho_.txt 280 > glove.in
    """

    if args.model == 'PALMER05':
        convertToGlove = 'r1rho2glove -t PALMER05 w1 -i ' + \
            IntFile + ' ' + temperature + \
                         ' > glove.in'
    elif args.model == 'CONST':
        convertToGlove = 'r1rho2glove -t CONST w1 -i ' + \
            IntFile + ' ' + temperature + \
                         ' > glove.in'
    elif args.model == 'MATRIX':
        convertToGlove = 'r1rho2glove -t MATRIX_ON w1 -i ' + \
            IntFile + ' ' + temperature + \
                         ' > glove.in'
    else:
        nprint("No fitting model assigned. Assuming MATRIX form.", "")
        convertToGlove = 'r1rho2glove -t MATRIX_ON w1 -i ' + \
            IntFile + ' ' + temperature + \
                         ' > glove.in'

    os.system(convertToGlove)
    os.system('glove -dvx && mplot -PDF')
    store(experiment, cnst=False)

    sys.exit()


def store(experiment, cnst):
    """
    Store glove in and out files and plot in output directory.
    Directory is created if necessary.
    """

    os.system('mkdir -p output')

    os.system('mv *.xmgr output/')
    os.system('mv plot.pdf output/plot_' + str(experiment.dataDir) + '.pdf')
    os.system('mv glove.in output/glove_' + str(experiment.dataDir) + '.in')
    os.system('mv glove.out output/glove_' + str(experiment.dataDir) + '.out')
    os.system('mv Int_r1rho.txt output/')
