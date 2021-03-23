import os
import numpy as np

from a_cout import *
from a_getintensity import *
from a_consistency import *

def getIntAll(residue, args, experiment):
    """
    Obtain intensity of the expected resonance for all 
    spectra (spin-locked data)
    """
    print
    nprint('PROC', 'Spin-lock expt.')
    for i in residue.fidObjectsData:
        os.chdir(experiment.dataDir + '/fid')
        getIntensity(i, residue, args)
        os.chdir('../..')
    print

def getIntAllRef(residue, args, experiment):
    """
    Obtain intensity of the expected resonance for all 
    spectra (reference)
    """
    print
    nprint('PROC', 'Reference expt.')
    for i in residue.fidObjectsReference:
        os.chdir(experiment.dataDir + '/fid')
        getIntensity(i, residue, args)
        os.chdir('../..')
    print

def getIntensity(fid, residue, args):
    """
    Determine intensity for current fid/spectrum object.
    """
    nprint("Spectrum ", fid.specFilename)

    os.system("cp " + fid.specFilename + " ./test.ft")
    os.system("chmod +x pk.tcl && ./pk.tcl >& /dev/null")

    """
    Extract all peak intensities from nmrpipe peak picking report
    """
    intensities = np.empty((0, 1), float)
    peaksPickedPPM = np.empty((0, 1), float)

    peakTable = open('./test.tab', 'r')

    """
    Header length of test.tab depends on 1D or 2D experiment
    """
    headerLength = 18
    intColumnIdx = 17
    ppmColumnIdx = 5

    for i in range(0, headerLength):
        peakTable.readline()

    for line in peakTable:
        columns = line.split()
        intensities = np.vstack([intensities,
                                 float(columns[intColumnIdx])])
        peaksPickedPPM = np.vstack([peaksPickedPPM,
                                    float(columns[ppmColumnIdx])])

    peakTable.close()

    """
    If nmrWish did not find any peaks, set intensity to 0.
    """
    if len(intensities) == 0:
        nprint("[NOTE]", "No peak found in spectrum.")
        intensities = np.vstack([intensities, 0])

    """
    Select correct peak based on proton chemical shift.
    """
    selectedIntensity, selectedPPM = selectCorrectPeak(fid,
                                                       peaksPickedPPM,
                                                       intensities,
                                                       residue)

    """
    Store final intensity and ppm values.
    """
    fid.intensity = selectedIntensity
    fid.wH_observed = selectedPPM

    """
    Verbose output.
    """
    print
    nprint("Peak expected at [1H, ppm] ", residue.wH)
    nprint("Peak found    at [1H, ppm] ", fid.wH_observed)
    nprint("Peak intensity ", fid.intensity)

def selectCorrectPeak(fid, peaksPickedPPM, intensities, residue):
    """
    Loop over the peak table until the correct (expected) peak is found in list
    """
    correctPeakFound = False

    while correctPeakFound is False:
        """
        First guess: select peak of max. intensity
        """
        trialIntensity, trialPPM, trialIndex = selectMaxPeak(intensities,
                                                             peaksPickedPPM)

        """
        Check if this peak is consistent with the expected proton chemical shift.
        if consistent: quit the loop (found)
        if not consistent: delete current guess from array and try again.
        """
        checkPPM = ppmCheck(fid, trialIntensity, trialPPM, residue)

        if checkPPM is True:
            correctPeakFound = True
            selectedIntensity = trialIntensity
            selectedPPM = trialPPM
            break
        elif checkPPM is False:
            intensities = np.delete(intensities, trialIndex)
            peaksPickedPPM = np.delete(peaksPickedPPM, trialIndex)

    return selectedIntensity, selectedPPM

def selectMaxPeak(intensities, ppmPicked):
    """
    Check if intensity list is empty; if so, give up.
    If not empty: get max. intensity of list
    """
    if len(intensities) == 0:
        return 0, 0, 0
    else:
        maximumIntensity = np.amax(intensities)

    """
    Recall chemical shift and index of this peak in the intensity array
    (required to delete this intensity / ppm in case of
    an incorrect pick)
    """
    for i in range(len(intensities)):
        deviation = intensities[i] - maximumIntensity

        if int(deviation) == 0:
            """
            Check if no peak was picked at all by nmrPipe
            """
            if len(ppmPicked) > 0:
                maxIntPPM = ppmPicked[i]
                maxIntArrayIndex = i
            else:
                maxIntPPM = 0
                maxIntArrayIndex = 0

    """
    Return peak of maximum intensity (index, intensity and chemical shift)
    """
    return maximumIntensity, maxIntPPM, maxIntArrayIndex
