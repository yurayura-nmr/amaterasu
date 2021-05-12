spinsys {
  channels 1H 15N 13C
  nuclei   1H 15N 13C

# on resonance nucleus
  shift 1 0 0 0 0 0 0
  shift 2 0 0 0 0 0 0
  shift 3 0 0 0 0 0 0

# couplings
  jcoupling 1 2 -93 0 0 0 0 0
  jcoupling 2 3  15 0 0 0 0 0
}

par {
  crystal_file     alpha0beta0

  start_operator   I1x
  detect_operator  -I3p
  
  variable index   1
  variable lb      10

  # CP to transfer magnetization H --> N --> C
  variable rfN     93
  variable rfH     93

  variable rfC     15
  variable rfN2    15

  variable tSL     10800
  variable tSL2    66700

  variable offset  0

  # Acquisition pars
  sw               4000
  variable tsw     1e6/sw
  np               512
  proton_frequency 700e6

  method           direct
  gamma_angles     1
  spin_rate        0
  verbose          1101
}

proc pulseq {} {
  global par

  turnoff jcoupling_1_2
  turnoff jcoupling_2_3

  # pulse <duration/usec> ?<rf(1)/Hz> <phase(1)/degrees>? ?<rf(2)> <phase(2)>? ...

  # CP  1H --> 15N --> 13C
  # As 1 single step
  #pulse $par(tSL) $par(rfH) x $par(rfN) x $par(rfC) x 


  # As two successive steps
  # CP  1H --> 15N
  #     DURATION   POWER     PH POWER      PH POWER     PH
  pulse $par(tSL)  $par(rfH) x  $par(rfN)  x  0         x
  # CP 15N --> 15N
  #     DURATION   POWER     PH POWER      PH POWER     PH
  pulse $par(tSL2) 0         x  $par(rfN2) x  $par(rfC) x 
   
  #turnon jcoupling_1_2
  #turnon jcoupling_2_3

  acq
  for {set i 1} {$i < $par(np)} {incr i} {
    delay $par(tsw)
    acq
  }
}

proc main {} {
  global par
  
  set f [fsimpson]
  faddlb $f $par(lb) 0
  fsave $f onres_offset_$par(offset)_pw_N$par(rfN)_C$par(rfC)_Hz.fid
  fzerofill $f 1024
  fft $f
  fsave $f onres_offset_$par(offset)_pw_N$par(rfN)_C$par(rfC)_Hz.spe
  #fsave $f onres_offset_$par(offset)_pw_N$par(rfN)_C$par(rfC)_Hz.txt -xreim
}
