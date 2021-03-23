import os
import nmrglue as ng

from a_cout import *

def ftAll(residue, args, experiment):
    """
    Fourier transform all spectra (spin-locked data)
    """
    for i in residue.fidObjectsData:
        os.chdir(experiment.dataDir + '/fid')
        FourierTransform(i, residue, args, experiment)
        os.chdir('../..')

def ftAllRef(residue, args, experiment):
    """
    Fourier transform all spectra (reference spectra; no spin-lock block)
    """
    for i in residue.fidObjectsReference:
        os.chdir(experiment.dataDir + '/fid')
        FourierTransform(i, residue, args, experiment)
        os.chdir('../..')

def FourierTransform(fid, residue, args, experiment):
    """
    Converts an input FID to a processed spectrum

    Read FID
    Process spectrum
    SOL
    SP
    ZF
    FT
    EXT
    DI
    Write output file "_proc.ft2"
    """
    p0 = residue.p0
    p1 = residue.p1

    nprint("FT", fid.filename)

    dic, nmrData = ng.pipe.read(fid.filename)

    spectrumFilename = fid.filename + '_proc.ft2'

    """
    Direct dimension (1H)
    """
    if fid.solventFilter is True:
        dic, nmrData = ng.pipe_proc.sol(
            dic, nmrData,
            mode='low',
            fl=16,
            fs=1,
            head=0)

    dic, nmrData = ng.pipe_proc.sp(dic, nmrData,
                                   off=fid.apodizationOffset,
                                   end=fid.apodizationEnd,
                                   pow=fid.apodizationPower,
                                   c=fid.cValue)

    dic, nmrData = ng.pipe_proc.zf(dic, nmrData, zf=fid.zeroFilling)
    dic, nmrData = ng.pipe_proc.ft(dic, nmrData, auto=True)

    dic, nmrData = ng.process.pipe_proc.ext(dic,
                                            nmrData,
                                            x1=0,
                                            xn=experiment.ROI)

    dic, nmrData = ng.pipe_proc.ps(dic, nmrData, float(p0), float(p1))
    dic, nmrData = ng.pipe_proc.di(dic, nmrData)

    """
    Indirect Dimension (15N)
    """
    dic, nmrData = ng.pipe_proc.tp(dic, nmrData)
    dic, nmrData = ng.pipe_proc.sp(dic, nmrData,
                                   off=0.5,
                                   end=1,
                                   pow=1,
                                   c=0.5)

    dic, nmrData = ng.pipe_proc.zf(dic, nmrData, zf=fid.zeroFilling)
    dic, nmrData = ng.pipe_proc.ft(dic, nmrData, auto=True)
    dic, nmrData = ng.pipe_proc.ps(dic, nmrData, -90, 0)
    dic, nmrData = ng.pipe_proc.di(dic, nmrData)
    dic, nmrData = ng.pipe_proc.tp(dic, nmrData)

    ng.pipe.write(spectrumFilename, dic, nmrData, overwrite=True)

    fid.specFilename = spectrumFilename
