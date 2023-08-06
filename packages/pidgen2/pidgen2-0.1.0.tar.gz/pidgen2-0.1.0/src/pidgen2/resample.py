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
import argparse
import pprint

from jax import numpy as np
import numpy as onp
import uproot

from .tuples import write_array, read_array
from .resampling import read_calib_tuple, calib_transform, data_transform, get_or_create_template, resample_data
from .resampling import get_samples, get_variables

def main() : 

  parser = argparse.ArgumentParser(description = "PIDGen resampling script", 
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('--seed', type=int, default = 1, 
                      help="Initial random seed for resampling")
  parser.add_argument('--input', type=str, default = None, 
                      help="Input ROOT path (file:tree), wildcards allowed")
  parser.add_argument('--output', type=str, default = None, 
                      help="Output ROOT file")
  parser.add_argument('--outtree', type=str, default = "tree", 
                      help="Output TTree")
  parser.add_argument('--sample', type=str, default = None, 
                      help="Calibration sample name")
  parser.add_argument('--dataset', type=str, default = None, 
                      help="Calibration dataset in the form Polarity_Year, e.g. MagUp_2018")
  parser.add_argument('--variable', type=str, default = None, 
                      help="PID variable to resample")
  parser.add_argument('--branches', type=str, default = "pt:eta:ntr", 
                      help="Input branches for Pt,Eta,Ntracks variables in the form Pt:Eta:Ntrack")
  parser.add_argument('--pidgen', type=str, default = "pidgen", 
                      help="Resampled PID branch")
  parser.add_argument('--stat', type=str, default = "pidstat", 
                      help="PID calibration statistics branch")
  parser.add_argument('--maxfiles', type=int, default = 0, 
                      help="Maximum number of calibration files to read (0-unlimited)")
  parser.add_argument('--start', type=int, default = 0, 
                      help="Start event")
  parser.add_argument('--stop', type=int, default = -1, 
                      help="Stop event")
  parser.add_argument('--usecache', default = False, action = "store_const", const = True, 
                      help='Use calibration cache')
  parser.add_argument('--plot', default = False, action = "store_const", const = True, 
                      help='Produce control plots')
  parser.add_argument('--interactive', default = False, action = "store_const", const = True, 
                      help='Show control plots interactively')
  parser.add_argument('--kernels', type=str, default = None, 
                      help='Kernel widths (e.g. --kernels="2,3,3,4"), if None, use the default ones')
  parser.add_argument('--verbose', default = False, action = "store_const", const = True, 
                      help='Enable debug messages')
  parser.add_argument('--friend', default = False, action = "store_const", const = True, 
                      help='Create friend tree with only resampled PID and statistics branches')
  parser.add_argument('--storage', type=str, default = "/eos/lhcb/wg/PID/PIDGen2/templates/", 
                      help="Template storage directory")
  parser.add_argument('--cachedir', type=str, default = None, 
                      help="Local cache directory")

  args = parser.parse_args()

  if len(sys.argv)<2 : 
    parser.print_help()
    raise SystemExit

  kernels = args.kernels
  if kernels : kernels = eval(kernels)

  input_branches = args.branches.split(":")
  start_event = args.start
  stop_event = args.stop

  config = get_samples()[args.sample][args.dataset]
  variable = get_variables()[args.variable]

  pp = pprint.PrettyPrinter(indent = 4)

  if (args.verbose) : 
    print(f"Calibration sample config: {pp.pformat(config)}")
    print(f"Variable definition: {pp.pformat(variable)}")

  print(f"Checking if template exists in the storage")

  print(args.cachedir)

  # Create PID resampling template based on calibration sample
  template = get_or_create_template(args.sample, args.dataset, args.variable, 
                             variable, config, 
                             use_calib_cache = args.usecache, max_files = args.maxfiles, 
                             interactive_plots = args.interactive, 
                             control_plots = args.plot, verbose = args.verbose, 
                             prefix = args.storage, cachedir = args.cachedir)

  print(f"Template ready, starting resampling")

  input_df = uproot.concatenate(args.input, input_branches, library = "pd")
  input_data = input_df[input_branches].to_numpy()

  if stop_event > len(input_data) : stop_event = len(input_data)
  else : input_data = input_data[start_event:stop_event]
  if (args.verbose) : print (f"Shape of the array for resampling: {input_data.shape}")

  if not args.friend : 
    all_df = uproot.concatenate(args.input, library = "pd")
    all_branches = list(all_df.keys())
    all_data = all_df[all_branches].to_numpy()[start_event:stop_event]
    if (args.verbose) : 
      print (f"Shape of all input data array: {all_data.shape}")
      print (f"List of all input tree branches: {pp.pformat(all_branches)}")

  onp.random.seed(args.seed)

  data = data_transform(input_data, config)
  pid_arr, calib_stat = resample_data(data, config, variable, template, verbose = args.verbose)

  if (args.verbose) : 
    print(f"Data array after variable transformation: {data}")
    print(f"Resampled PID array: {pid_arr}")
    print(f"Resampling statistics array: {calib_stat}")

  if not args.friend : 
    write_array(args.output, np.concatenate([all_data, pid_arr, calib_stat], axis = 1), 
            branches = all_branches + [args.pidgen, args.stat], tree = args.outtree )
  else : 
    write_array(args.output, np.concatenate([pid_arr, calib_stat], axis = 1), 
            branches = [args.pidgen, args.stat], tree = args.outtree )

if __name__ == "__main__" : 
  main()
