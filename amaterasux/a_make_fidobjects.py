from a_fid import *
from a_cout import *

import sys

def makeFidObjectsOffres(residue, experiment):
    """
    Generate FID objects for current residue spin-locked data (usually >19)
    This function (untested) is for the off-resonance experiment.
    """
    numberOffsets = len(experiment.fq3list) # is that all 178 or is it 176/4 + 2?
    numberFids = len(experiment.fidFilenames) # x 4?
    
    fidsPerResidue = numberOffsets
    
    nprint("[Amaterasu]",          "off-resonance experiment")
    nprint("Number of residues     ", experiment.TD4) # same for off-resonance
    nprint("Number of FIDs/residue ", fidsPerResidue)
    nprint("Number of offsets      ", numberOffsets)
    nprint("Total number of FIDs   ", numberFids)
    nprint("Current residue #      ", residue.index)
    # ...
    #test until here then continue
    sys.exit()


def makeFidObjects(residue, experiment):
    """
    Generate FID objects for current residue spin-locked data (usually >19)
    This function deals with on-resonance R1rho experiments.
    """
    numberPowers = len(experiment.valist)
    numberFids = len(experiment.fidFilenames)
    
    fidsPerResidue = numberPowers
    
    nprint("[Amaterasu]",          "on-resonance experiment")
    nprint("Number of residues     ", experiment.TD4)
    nprint("Number of FIDs/residue ", fidsPerResidue)
    nprint("Total number of FIDs   ", numberFids)
    nprint("Current residue #      ", residue.index)

    fidObjectsData = list()
    fidObjectsReference = list()

    """
    The first (n-2) experiments are spin-locked
    """
    start = residue.index * fidsPerResidue
    end = start + fidsPerResidue - 2

    for i in range(start, end):
        testFid = fid()
        testFid.index = i
        testFid.filename = experiment.fidFilenames[i]
        testFid.reference = False
        fidObjectsData.append(testFid)
        # print testFid.filename

    #nprint ("Spin-lock FIDs", fidObjectsData)

    """
    The next 2 experiments are reference experiments
    """
    start = residue.index * fidsPerResidue + (len(experiment.valist) - 2)
    end = start + 2

    for i in range(start, end):
        testFid = fid()
        testFid.index = i
        testFid.filename = experiment.fidFilenames[i]
        testFid.reference = True
        fidObjectsReference.append(testFid)

    #nprint ("Reference (or screening) FIDs", fidObjectsReference)

    """
    Store the information in the residue object
    """
    residue.fidObjectsData = fidObjectsData
    residue.fidObjectsReference = fidObjectsReference
