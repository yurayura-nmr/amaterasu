import sys
import os

from a_cout import *

def writeScreeningOutput(experiment):
    print

    os.system('mkdir -p output')
    IntFile = open('./output/Int_r1rho_screening.txt', 'w')

    for currentResidue in experiment.residues:
        weakSL = currentResidue.fidObjectsReference[0].intensity
        strongSL = currentResidue.fidObjectsReference[1].intensity
        ratio = weakSL / strongSL

        """
        For output, round to 3 significant figures.
        """
        ratio = round(ratio, 3)

        nprint("Residue", str(currentResidue.index))
        nprint("Int. ratio", str(ratio))

        IntFile.write("Residue #" + str(currentResidue.index).ljust(10) +
                      "Ratio: " + str(ratio).ljust(20))

        if ratio < experiment.screeningThreshold:
            IntFile.write("R1rho dispersion !! ".ljust(20) + "\n")
        else:
            IntFile.write("\n")

    IntFile.close()
