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

import sys
import os
import argparse
import pprint

from jax import numpy as np
import uproot3 as uproot

from .tuples import write_array, read_array
from .resampling import store_to_cache
from .resampling import get_samples, get_variables

def main() : 

  parser = argparse.ArgumentParser(description = "Store selected PID calibration sample branches into local cache", 
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('--sample', type=str, default = None, 
                      help="Calibration sample name")
  parser.add_argument('--dataset', type=str, default = None, 
                      help="Calibration dataset in the form Polarity_Year, e.g. MagUp_2018")
  parser.add_argument('--variable', type=str, default = None, 
                      help="PID variable to resample")
  parser.add_argument('--maxfiles', type=int, default = 0, 
                      help="Maximum number of calibration files to read (0-unlimited)")
  parser.add_argument('--verbose', default = False, action = "store_const", const = True, 
                      help='Enable debug messages')
  parser.add_argument('--cachedir', type=str, default = None, 
                      help="Cache directory")

  args = parser.parse_args()

  if len(sys.argv)<2 : 
    parser.print_help()
    raise SystemExit

  config = get_samples()[args.sample][args.dataset]
  variable = get_variables()[args.variable]

  pp = pprint.PrettyPrinter(indent = 4)

  if (args.verbose) : 
    print(f"Calibration sample config: {pp.pformat(config)}")
    print(f"Variable definition: {pp.pformat(variable)}")

  calib_cache_dirname = f"{args.cachedir}/{args.sample}/{args.dataset}/{args.variable}/"
  os.system(f"mkdir -p {calib_cache_dirname}")

  store_to_cache(variable, config, max_files = args.maxfiles, 
                 verbose = args.verbose, cachedir = calib_cache_dirname)

if __name__ == "__main__" : 
  main()
