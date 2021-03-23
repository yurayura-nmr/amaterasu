import numpy as np


def dBtoHz(residue, valist_dB):
    """
    Convert spin-lock power values from decibel (dB) to Hz.

    Takes:      array      valist_dB: valist in Decibel
    Returns:    array      valist_Hz: valist in Hertz
    """

    valist_Hz = []

    Npulse_dB = float(residue.N15pulseDB)
    Npulse_length = float(residue.N15pulseLength)

    for i in valist_dB:
        dB = float(i[0])
        Hz = round(1 / ((np.power(10, ((float(dB) - float(Npulse_dB)
                                        ) / 20)) / 250000) * float(Npulse_length)))

        valist_Hz.append(Hz)

    return valist_Hz
