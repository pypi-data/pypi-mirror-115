##############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

"""
Definitions of LHCb PID calibration datasets (ROOT files produced by WG productions). 
The ROOT files can contain several trees corresponding to different calibration samples. 
These dictionaries are used further in the definitions of calibration samples (see samples/ subdir). 
"""

run2_dir = "root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/LHCb/"
run1_dir = "root://eoslhcb.cern.ch//eos/lhcb/wg/PID/PIDCalib_Run1_conversion/Reco14_DATA/"

legacy_run2_pidcalib_datasets = {
  'MagDown_2018'   : [f"{run2_dir}/Collision18/PIDCALIB.ROOT/00109278/0000/00109278_{i:08}_1.pidcalib.root" for i in range(1, 403) ], 
  'MagUp_2018'     : [f"{run2_dir}/Collision18/PIDCALIB.ROOT/00109276/0000/00109276_{i:08}_1.pidcalib.root" for i in range(1, 429) ], 
  'MagDown_2017'   : [f"{run2_dir}/Collision17/PIDCALIB.ROOT/00106052/0000/00106052_{i:08}_1.pidcalib.root" for i in range(1, 372) ], 
  'MagUp_2017'     : [f"{run2_dir}/Collision17/PIDCALIB.ROOT/00106050/0000/00106050_{i:08}_1.pidcalib.root" for i in range(1, 314) ],
  'MagDown_2016'   : [f"{run2_dir}/Collision16/PIDCALIB.ROOT/00111825/0000/00111825_{i:08}_1.pidcalib.root" for i in range(1,  259) ], 
  'MagUp_2016'     : [f"{run2_dir}/Collision16/PIDCALIB.ROOT/00111823/0000/00111823_{i:08}_1.pidcalib.root" for i in range(1,  239) ], 
  'MagDown_2015'   : [f"{run2_dir}/Collision15/PIDCALIB.ROOT/00064785/0000/00064785_{i:08}_1.pidcalib.root" for i in range(1,  79) ], 
  'MagUp_2015'     : [f"{run2_dir}/Collision15/PIDCALIB.ROOT/00064787/0000/00064787_{i:08}_1.pidcalib.root" for i in range(1,  45) ], 
}

converted_run1_pidcalib_datasets_dstar_k = {
  "MagUp_2011"   : [f"{run1_dir}/MagUp/DSt_K_MagUp_Strip21r1_{i}.root" for i in range(24) ], 
  "MagUp_2012"   : [f"{run1_dir}/MagUp/DSt_K_MagUp_Strip21_{i}.root" for i in range(72) ], 
  "MagDown_2011" : [f"{run1_dir}/MagDown/DSt_K_MagDown_Strip21r1_{i}.root" for i in range(35) ], 
  "MagDown_2012" : [f"{run1_dir}/MagDown/DSt_K_MagDown_Strip21_{i}.root" for i in range(71) ], 
}

converted_run1_pidcalib_datasets_dstar_pi = {
  "MagUp_2011"   : [f"{run1_dir}/MagUp/DSt_Pi_MagUp_Strip21r1_{i}.root" for i in range(24) ], 
  "MagUp_2012"   : [f"{run1_dir}/MagUp/DSt_Pi_MagUp_Strip21_{i}.root" for i in range(72) ], 
  "MagDown_2011" : [f"{run1_dir}/MagDown/DSt_Pi_MagDown_Strip21r1_{i}.root" for i in range(35) ], 
  "MagDown_2012" : [f"{run1_dir}/MagDown/DSt_Pi_MagDown_Strip21_{i}.root" for i in range(71) ], 
}
