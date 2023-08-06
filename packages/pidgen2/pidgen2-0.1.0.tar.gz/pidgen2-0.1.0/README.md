# PIDGen 

## Introduction

PIDGen is a tool to resample PID variables in the full MC bases on distributions from calibration samples. 

## Structure of the code

## Documentation

   * 11/02/21, RTA WP4-5 meeting, [PIDGen in Run3](https://indico.cern.ch/event/997930/#3-new-pidgencorr)
   * [Twiki for the old PIDGen/PIDCorr for Run1/2](https://twiki.cern.ch/twiki/bin/view/LHCb/MeerkatPIDResampling)
   * Details about Run2 PID calibration samples are here: [ChargedPID twiki](https://twiki.cern.ch/twiki/bin/viewauth/LHCbPhysics/ChargedPID)
   * [LHCb-INT-2017-007 internal note](https://gitlab.cern.ch/lhcb-docs/INT/LHCb-INT-2017-007/blob/master/drafts/LHCb-INT-2017-007_v0r0.pdf)

## Running PIDGen 

See `runme.sh` script as an example. It takes the Dstar2Dpi calibration sample and resamples the first 1M events from it (using `pidgen.py`). Then (with `pidgen_validation.py`) it produces the plot comparing the original and resampled PID distribution. 
