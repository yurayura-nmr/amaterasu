spinsys {
  channels 1H 15N
  nuclei 1H 15N

# on resonance nucleus
  shift 1 0 0 0 0 0 0
  shift 2 0 0 0 0 0 0

# couplings
  jcoupling 1 2 -93 0 0 0 0 0

}

par {
  crystal_file     alpha0beta0

  start_operator   I1x
  detect_operator  -I2p
  
  variable index   1
  variable lb      10

  # CP to transfer magnetization H--> N
  variable rfN     40
  variable rfH     40
  variable tSL     10800

  # Spin-lock while decoupling on 1H
  variable offset  0
  variable rfN2    100
  variable rfH2    3900  
  variable tSL2    40000

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
  pulse $par(tSL) $par(rfH) x $par(rfN) x 
  pulse $par(tSL2) $par(rfH2) x $par(rfN2) x 
   
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
  #fsave $f onres_offset_$par(offset)_pw_$par(rfN)Hz.fid
  fzerofill $f 1024
  fft $f
  fsave $f onres_offset_$par(offset)_pw_$par(rfN)Hz.spe
  fsave $f onres_offset_$par(offset)_pw_$par(rfN)Hz.txt -xreim
}
