from nmrglue.process.proc_base import ps
from a_cout import *

import sys
import os
import nmrglue as ng
import numpy as np
import scipy.optimize

"""
This file uses the following functions (modified) from
the nmrglue project:

autops
_ps_acme_score
_ps_peak_minima_score

Copyright Notice and Statement for the nmrglue Project

Copyright (c) 2010-2015 Jonathan J. Helmus
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:


a. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.


b. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the
   distribution.


c. Neither the name of the author nor the names of contributors may 
   be used to endorse or promote products derived from this software 
   without specific prior written permission.


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

def phaseReference(residue, experiment):
    """
    Get a reference FID
    """
    os.chdir(experiment.dataDir + '/fid')
    referenceFid = residue.fidObjectsReference[0]

    """
    Fourier-transform the first dimension of the reference FID without knowing the phase yet
    """
    p0 = 0
    p1 = 0

    dic, nmrData = ng.pipe.read(referenceFid.filename)

    if referenceFid.solventFilter is True:
        dic, nmrData = ng.pipe_proc.sol(dic, nmrData, mode='low', fl=16,
                                        fs=1,
                                        head=0)

    dic, nmrData = ng.pipe_proc.sp(dic, nmrData,
                                   off=referenceFid.apodizationOffset,
                                   end=referenceFid.apodizationEnd,
                                   pow=referenceFid.apodizationPower,
                                   c=referenceFid.cValue)

    dic, nmrData = ng.pipe_proc.zf(dic, nmrData, zf=referenceFid.zeroFilling)
    dic, nmrData = ng.pipe_proc.ft(dic, nmrData, auto=True)

    dic, nmrData = ng.process.pipe_proc.ext(dic,
                                            nmrData,
                                            x1=0,
                                            xn=experiment.ROI)

    dic, nmrData = ng.pipe_proc.ps(dic, nmrData, float(p0), float(p1))

    """
    Obtain phases from ACME algorithm
    Write phased spectrum as phased.ftx file
    """
    nmrDataPhased, p0, p1 = autops(nmrData, 'acme')

    ng.pipe.write('phased.ftx', dic, nmrDataPhased, overwrite=True)

    nprint("P0", p0)
    nprint("P1", p1)

    residue.p0 = p0
    residue.p1 = p1

    os.chdir('../..')

    return residue

def autops(data, fn, p0=0.0, p1=0.0):
    """
    Automatic linear phase correction
    Parameters
    ----------
    data : ndarray
        Array of NMR data.
    fn : str or function
        Algorithm to use for phase scoring. Built in functions can be
        specified by one of the following strings: "acme", "peak_minima"
    p0 : float
        Initial zero order phase in degrees.
    p1 : float
        Initial first order phase in degrees.
    Returns
    -------
    ndata : ndarray
        Phased NMR data.
    """
    if not callable(fn):
        fn = {
            'peak_minima': _ps_peak_minima_score,
            'acme': _ps_acme_score,
        }[fn]

    opt = [p0, p1]
    #opt = scipy.optimize.fmin(fn, x0=opt, args=(data, ))
    opt = scipy.optimize.fmin_powell(fn, x0=opt, args=(data, ), disp=0)

    phasedspc = ps(data, p0=opt[0], p1=opt[1])
    #phasedspc = ps(data, p0=opt[0])

    return phasedspc, opt[0], opt[1]

def _ps_acme_score(ph, data):
    """
    Phase correction using ACME algorithm by Chen Li et al.
    Journal of Magnetic Resonance 158 (2002) 164-168
    Parameters
    ----------
    pd : tuple
        Current p0 and p1 values
    data : ndarray
        Array of NMR data.
    Returns
    -------
    score : float
        Value of the objective function (phase score)
    """
    stepsize = 1

    phc0, phc1 = ph

    s0 = ps(data, p0=phc0, p1=phc1)
    data = np.real(s0)

    """
    Calculation of first derivatives
    """

    ds1 = np.abs((data[1:] - data[:-1]) / (stepsize * 2))
    p1 = ds1 / np.sum(ds1)

    """
    Calculation of entropy
    """

    p1[p1 == 0] = 1

    h1 = -p1 * np.log(p1)
    h1s = np.sum(h1)

    """
    Calculation of penalty
    """

    pfun = 0.0
    as_ = data - np.abs(data)
    sumas = np.sum(as_)

    if sumas < 0:
        pfun = pfun + np.sum((as_ / 2) ** 2)

    p = 1000 * pfun

    return h1s + p

def _ps_peak_minima_score(ph, data):
    """
    Phase correction using simple minima-minimisation around highest peak
    This is a naive approach but is quick and often achieves reasonable
    results.  The optimisation is performed by finding the highest peak in the
    spectra (e.g. TMSP) and then attempting to reduce minima surrounding it.
    Parameters
    ----------
    pd : tuple
        Current p0 and p1 values
    data : ndarray
        Array of NMR data.
    Returns
    -------
    score : float
        Value of the objective function (phase score)
    """

    phc0, phc1 = ph

    s0 = ps(data, p0=phc0, p1=phc1)
    data = np.real(s0)

    i = np.argmax(data)
    mina = np.min(data[i - 100:i])
    minb = np.min(data[i:i + 100])

    return np.abs(mina - minb)
