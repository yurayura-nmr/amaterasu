def ppmCheck(fid, trialIntensity, trialPPM, residue):
    """
    If no peak was found, nothing to do here
    """
    if int(trialIntensity) == 0:
        return True
    else:
        """
        Check if picked peak is consistent with expected
        chemical shift.
        """

        deviationFromExpectedPPM = abs(float(trialPPM) - residue.wH)

    bl = deviationFromExpectedPPM < fid.tolerance

    return bl
