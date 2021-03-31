spinsys {
  nuclei 15N 1H
  channels 15N 1H

# 15N on resonance: offset 0 Hz
  shift 1 404 0 0 0 0 0
# 1H on resonance: offset 0 Hz
  shift 2 404 0 0 0 0 0

# can check off-resonance excitation by just moving
# the isotropic chemical shift away from 0ppm, say to
# 0.1 ppm or so


# no dipolar coupling in solution
  dipole 1 2 0 0 0 0

# J-coupling H-N is negative
  jcoupling 1 2 -93 0 0 0 0 0
}

par {

# sample orientational averaging
  crystal_file     alpha0beta0

# user variables
#     CP spin-lock power
  variable rfN     40
  variable rfH     40

# SW?
  variable tsw     10
  variable index   1

# spectral width
  sw               1e6/tsw

# length of FID
  np               4096

# spectrometer frequency
  proton_frequency 700e6

# start and detection operators
  start_operator   I2x
  detect_operator  I1p
  method           direct

# ???
  gamma_angles     1

# we will not spin the sample
  spin_rate        0

# verbosity
  verbose          1101
}

proc pulseq {} {
  global par

# CP
#  pulse 200 $par(rfH) x $par(rfN) x

# Ideal decouling
#  turnoff jcoupling_1_2

# Acquisition of FID
#  acq_block { delay [expr 1.0e6/$par(sw)] }

# original:
  acq_block { pulse $par(tsw) $par(rfN) x $par(rfH) x }
#  turnoff jcoupling_1_2
}


proc main {} {
  global par
  
  set f [fsimpson]
#  faddlb $f 15 0
  fsave $f trial.fid
  fsave $f trial.txt -xreim
#  fzerofill $f 8192
#  fft $f
#  fsave $f test.spe
}
