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
Functions for PID resampling of calibration data. 
"""

import importlib
import os
import sys
from itertools import product
from copy import deepcopy
from hashlib import sha1
import json

from jax import numpy as np
import numpy as onp
import matplotlib
import matplotlib.pyplot as plt
import uproot
import uproot3
from scipy.ndimage import gaussian_filter

from .plotting import plot, plot_distr2d, plot_distr1d, set_lhcb_style, plot_hist2d
from .tuples import read_array_filtered, write_array, read_array
from . import density_estimation as de

def get_samples() :
  """
  Import all modules with calibration samples from the "samples" subdir
  and construct the dictionary of all calibration samples

  Returns: 
      Dictionary of all samples loaded from "samples/" subdirectory
  """
  from . import samples
  d = {}
  for i in samples.__all__ : 
    module = importlib.import_module("." + i, "pidgen2.samples")
    s = getattr(module, "sample")
    d[i] = s
  return d

def get_variables() : 
  """
  Import all modules with variables description from the "variables" subdir
  and construct the dictionary of all variables. 

  Returns: 
      Dictionary of all variables loaded from "variables/" subdirectory
  """
  from . import variables
  d = {}
  for i in variables.__all__ : 
    module = importlib.import_module("." + i, "pidgen2.variables")
    c = getattr(module, "variable")
    d[i] = c
  return d

def read_calib_tuple(sample, trees, branches, verbose = False, cachedir = None) : 
  """ 
  Read calibration sample from the list of files into numpy array. 

  Args: 
    sample: tuple in the form (formatstring, numfiles) describing the calibration sample.
    trees: list of ROOT trees to read from the calibration files 
    branches: list of branches to read. 
    cachedir: If not None, store the copy of each input tree into the local cache file 
              under cachedir (only the selected branches)

  Returns: 
    2D numpy array, result of concatenation of all calibration samples. 
    The 1st index of 2D array corresponds to event, 2nd index to the variable from the branches list. 
  """
  datasets = []
  if cachedir : 
    os.system(f"mkdir -p {cachedir}")
  for i,filename in enumerate(sample) : 

    sys.stdout.write(f"\rReading file ({i+1}/{len(sample)}) {filename}")
    sys.stdout.flush()

    if cachedir : 
      calib_cache_filename = cachedir + "/" + filename.split("/")[-1]
      file = uproot3.recreate(calib_cache_filename, compression=uproot3.ZLIB(4))

    for tree in trees : 
      try : 
        with uproot.open(filename + ":" + tree) as t :
          arr = t.arrays(branches, library = "pd")[branches].to_numpy()

          if cachedir : 
            outtree = tree.replace("/", "_") # Subdirs are not supported by uproot
            file[outtree] = uproot3.newtree( { b : "float64" for b in branches } )
            d = { b : arr[:,i] for i,b in enumerate(branches) }
            file[outtree].extend(d)

          #if verbose : print(f"Reading tree {tree}, {arr.shape[0]} events")
          datasets += [ arr ]

      except FileNotFoundError : 
        print(f"... file not found, skipping")
        break
    if cachedir : 
      file.close()

  print("")

  if len(datasets) == 0 : 
    print(f"No input calibration files found. Do you have a valid Kerberos ticket to access EOS?")
    print(f"Will not create PID template, exiting...\n\n")
    raise SystemExit

  return datasets

def read_calib_cache(cachedir, sample, trees, branches, verbose = False) : 
  """ 
  Read cached calibration sample from the list of files into numpy array. 

  Args: 
    cachedir: local cache directory
    sample: tuple in the form (formatstring, numfiles) describing the calibration sample.
    trees: list of ROOT trees to read from the calibration files 
    branches: list of branches to read. 

  Returns: 
    2D numpy array, result of concatenation of all calibration samples. 
    The 1st index of 2D array corresponds to event, 2nd index to the variable from the branches list. 
  """
  datasets = []

  for i,filename in enumerate(sample) : 

    calib_cache_filename = cachedir + "/" + filename.split("/")[-1]

    sys.stdout.write(f"\rReading cached file ({i+1}/{len(sample)}) {calib_cache_filename}")
    sys.stdout.flush()

    for tree in trees : 

      treename = tree.replace("/", "_") # Subdirs are not supported by uproot in cache files

      with uproot.open(calib_cache_filename + ":" + treename) as t :
        arr = t.arrays(branches, library = "pd")[branches].to_numpy()

        #if verbose : print(f"Reading tree {tree}, {arr.shape[0]} events")
        datasets += [ arr ]

  print("")

  if len(datasets) == 0 : 
    print(f"No input cache files found.")
    print(f"Will not create PID template, exiting...\n\n")
    raise SystemExit

  return datasets

def read_calib_tuple_2(sample, trees, branches, verbose = False, cachedir = None) : 
  """ 
  Read calibration sample from the list of files into numpy array. 

  Args: 
    sample: tuple in the form (formatstring, numfiles) describing the calibration sample.
    trees: list of ROOT trees to read from the calibration files 
    branches: list of branches to read. 
    cachedir: If not None, store the copy of each input tree into the local cache file 
              under cachedir (only the selected branches)

  Returns: 
    2D numpy array, result of concatenation of all calibration samples. 
    The 1st index of 2D array corresponds to event, 2nd index to the variable from the branches list. 
  """
  datasets = []
  if cachedir : 
    os.system(f"mkdir -p {cachedir}")
  filenames = sample

  locations = [ f"{f}:{t}" for f, t in product(filenames, trees) ]
 
  print(locations)

  return uproot.concatenate(locations, filter_name = branches, allow_missing = False, library = "pd")[branches].to_numpy()

def calib_transform(x, config, variable) :
  """
  Apply variable transformation to the calibration array. 

  Args: 
    x: 2D numpy array in the format returned by read_calib_tuple function. 
    config: calibration sample configuration dictionary. 
    variable: variable definition dictionary. 
  """

  transform_forward = eval("lambda x : (" + variable["transform_forward"] + ")")
  transform_sample = []
  for c in config["transform"] : 
    transform_sample += [ eval("lambda x : (" + c + ")") ]

  arr = [ 
    transform_forward(x[:,0]),    # PID variable
    transform_sample[0](x[:,1]),  # pT
    transform_sample[1](x[:,2]),  # eta
    transform_sample[2](x[:,3] + onp.random.uniform(size = x.shape[0]) - 0.5 ),   # Ntracks (add uniform random +-0.5)
    x[:,4]  # sWeight
  ]
  return np.stack(arr, axis = 1)

def data_transform(x, config) :
  """
  Apply variable transformation to the data array. 

  Args: 
    x: 2D numpy array in the format returned by read_array function. 
    config: calibration sample configuration dictionary. 
  """
  transform_sample = [ ]
  for c in config["transform"] : 
    transform_sample += [ eval("lambda x : (" + c + ")") ]
  arr = [ 
    transform_sample[0](x[:,0]),  # pT
    transform_sample[1](x[:,1]),  # eta
    transform_sample[2](x[:,2])   # Ntracks
  ]
  return np.stack(arr, axis = 1)

def store_to_cache(variable, config, max_files = 0, verbose = False, cachedir = None) : 
  """
  Store selected branches from PID calibration samples to local cache files. 

  Args: 
    variable: variable definition dictionary.
    config: calibration sample configuration dictionary.
    max_files: Maximum number of calibration files to load (0 for unlimited)

  """
  sample = config['sample']
  trees = config['trees']
  calib_branches = [variable["branch"]] + config["branches"]
  if not cachedir : 
    calib_cache_dirname = config["calib_cache_dirname"]
  else : 
    calib_cache_dirname = cachedir

  if max_files == 0 : 
    raw_data = read_calib_tuple(sample, trees, calib_branches, verbose = verbose, cachedir = calib_cache_dirname)
  else : 
    raw_data = read_calib_tuple(sample[:max_files], trees, calib_branches, verbose = verbose, cachedir = calib_cache_dirname)
  print(f"Read {len(raw_data)} calibration subsamples from remote storage.")

def get_or_create_template(sample_name, dataset_name, variable_name, 
                    variable, config, kernels = None, use_calib_cache = False, control_plots = False, 
                    interactive_plots = False, prefix = ".", max_files = 0, verbose = False, cachedir = None) : 
  """

  """

  hash_config = {
    "variable"  : deepcopy(variable), 
    "config"    : deepcopy(config), 
    "max_files" : max_files, 
  }

  keys_to_ignore = ["labels"]

  for k in keys_to_ignore : hash_config["config"].pop(k)

  config_hash = sha1(str(hash_config).encode('utf-8')).hexdigest()

  print(f"Template configuration hash : {config_hash}")

  template_storage = f"{prefix}/{sample_name}/{dataset_name}/{variable_name}/{config_hash}/"
  calib_cache_dirname = f"{cachedir}/{sample_name}/{dataset_name}/{variable_name}/"

  try: 

    f = open(template_storage + "/config.json")
    f.close()
    data = onp.load(template_storage + "/template.npz", allow_pickle = True)
    template = data["arr_0"], data["arr_1"], data["arr_2"]

    print(f"Read template from {template_storage}")

  except FileNotFoundError : 

    print(f"Template in {template_storage} not found, will create one. Be patient... ")

    os.system(f"mkdir -p {template_storage}")
    if not use_calib_cache : 
      os.system(f"mkdir -p {calib_cache_dirname}")

    template = create_template(variable, config, kernels = kernels, use_calib_cache = use_calib_cache, 
                    control_plots = control_plots, interactive_plots = interactive_plots, 
                    prefix = template_storage, max_files = max_files, verbose = verbose, cachedir = calib_cache_dirname)

    f = open(template_storage + "/config.json", "w")
    json.dump(hash_config, f, indent = 4)
    f.close()
    onp.savez(template_storage + "/template.npz", template[0], template[1], template[2] )

  return template

def create_template(variable, config, kernels = None, use_calib_cache = False, control_plots = False, 
                    interactive_plots = False, prefix = "", max_files = 0, verbose = False, cachedir = None) : 
  """
  Create PID calibration template from the calibration sample (smoothed PDF). 

  Args: 
    variable: variable definition dictionary.
    config: calibration sample configuration dictionary.
    kernels: optional list of kernel widths (if None, taken from config and variable definition dicts). 
    use_calib_cache: if True, take calibration sample from the local cache. 
    control_plots: if True, produce control plots (1D and 2D projections of calibration and smoothed distributions). 
    interactive_plots: if True, open control plots in interactive mode, if False, only store them to files. 
    prefix: prefix for control plots (e.g. --prefix="subdir/"). 
    max_files: Maximum number of calibration files to load (0 for unlimited)
    
  Returns: 
    template structure to be used for resampling. 
  """
  sample = config['sample']
  trees = config['trees']
  calib_branches = [variable["branch"]] + config["branches"]
  ranges = [ variable["data_range"]] + config["data_ranges"]
  calib_cache_branches = ["pid"] + config["calib_cache_branches"]
  normalise_bins = [variable["normalise_bins"]] + config["normalise_bins"]
  normalise_methods = [variable["normalise_method"]] + config["normalise_methods"]
  normalise_ranges = [variable["normalise_range"]] + config["normalise_ranges"]
  template_bins = [variable["template_bins"]] + config["template_bins"]
  if kernels : 
    template_sigma = kernels
  else : 
    template_sigma = [variable["template_sigma"]] + config["template_sigma"]
  max_weights = config["max_weights"]

  onp.random.seed(1)  # To make variable transformation of the calibration sample (calib_transform) deterministic

  if use_calib_cache : 
    if max_files == 0 : 
      data = read_calib_cache(cachedir, sample, trees, calib_branches, verbose = verbose)
    else : 
      data = read_calib_cache(cachedir, sample[:max_files], trees, calib_branches, verbose = verbose)
    print(f"Read {len(data)} calibration subsamples from local cache.")
  else :
    if max_files == 0 : 
      data = read_calib_tuple(sample, trees, calib_branches, verbose = verbose, cachedir = cachedir)
    else : 
      data = read_calib_tuple(sample[:max_files], trees, calib_branches, verbose = verbose, cachedir = cachedir)

    #print(data)
    print(f"Read {len(data)} calibration subsamples from remote storage.")

  if (verbose) : print(f"Original data array: {data[0]}")

  if (verbose) : print(f"Starting to transform data array")
  for i, d in enumerate(data) : 
    d1 = calib_transform(d, config, variable)
    data[i] = d1
  if (verbose) : print(f"Transformed data array: {data[0]}")

  print(f"Starting to filter data, ranges = {ranges}")
  for i, d in enumerate(data) : 
    d1 = de.filter_data(d, ranges + [ (-1000., 1000.) ] )
    data[i] = d1
  if (verbose) : print(f"Filtered data: {data[0]}")

  weights1 = [ d[:,-1] for d in data ]

  weights = []
  if max_weights : 
    histograms = de.create_histograms_vector(data, ranges = ranges, bins = normalise_bins, weights = weights1)[1:]
    for d,w in zip(data, weights1) : 
      weights2 = de.reweight(d[:,:-1], histograms, max_weights = max_weights, weights = w)
      weights += [ w*weights2 ]
  else : 
    weights = weights1

  print(f"Creating normaliser structure")
  normaliser = de.create_normaliser_vector(data, ranges = ranges, bins = normalise_bins, weights = weights1)

  print(f"Starting to normalise data array")
  norm_data = []
  for d in data : 
    norm_data += [ de.normalise(d[:,:-1], normaliser, normalise_methods) ]
  if (verbose) : print(f"Normalised data array: {norm_data[0]}")

  #unnorm_data = de.unnormalise(norm_data, normaliser, normalise_methods)

  counts = None
  edges = None
  for i,(nd,w) in enumerate(zip(norm_data, weights)) : 
    sys.stdout.write(f"\rFilling histogram for subsample {i+1}/{len(norm_data)}")
    sys.stdout.flush()
    c, e = onp.histogramdd(nd, bins = template_bins, range = normalise_ranges, weights = w)
    if counts is None : 
      counts = c
      edges = e
    else : 
      counts += c

  print("")
  print(f"Applying Gaussian filter")
  smooth_counts = gaussian_filter(counts, template_sigma)

  if control_plots : 

    labels = config["labels"]
    names = config["names"]

    log = True

    print(f"Producing control plots")
    set_lhcb_style(size = 12, usetex = False)
    #fig, axes = plt.subplots(nrows = 7, ncols = 6, figsize = (12, 9) )

    for i in range(len(ranges)) : 
    
      if verbose : print(f"Plots for 1D projection {names[i]}")
     
      with plot(f"{names[i]}_transformed", prefix) as (fig, ax) : 
        plot_distr1d(data, i, bins = 50, range = ranges[i], ax = ax, label = "Transformed " + labels[i], weights = weights1, title = "Transformed distribution")

#    for i in range(len(ranges)) : 
      with plot(f"{names[i]}_weighted", prefix) as (fig, ax) : 
        plot_distr1d(data, i, bins = 50, range = ranges[i], ax = ax, label = "Weighted " + labels[i], weights = weights, title = "Weighted distribution")

#    for i in range(len(ranges)) : 
      with plot(f"{names[i]}_normalised", prefix) as (fig, ax) : 
        plot_distr1d(norm_data, i, bins = 50, range = normalise_ranges[i], ax = ax, label = "Normalised " + labels[i], weights = weights, title = "Normalised distribution")

#    for i,j in [ (0,1), (0,2), (1,2), (0,3), (1,3), (2,3) ] : 

#    bins = template_bins

    smooth_proj = {
      (0, 1) : [np.sum(smooth_counts, (2,3)), edges[0], edges[1]],
      (0, 2) : [np.sum(smooth_counts, (1,3)), edges[0], edges[2]],
      (1, 2) : [np.sum(smooth_counts, (0,3)), edges[1], edges[2]],
      (0, 3) : [np.sum(smooth_counts, (1,2)), edges[0], edges[3]],
      (1, 3) : [np.sum(smooth_counts, (0,2)), edges[1], edges[3]],
      (2, 3) : [np.sum(smooth_counts, (0,1)), edges[2], edges[3]],
    }

    n1,n2,n3,n4 = [int(n/2) for n in template_bins]  # Make slices through the central region of the distribution

    data_slices = {
      (0, 1) : [counts[:,:,n3,n4], edges[0], edges[1]], 
      (0, 2) : [counts[:,n2,:,n4], edges[0], edges[2]], 
      (1, 2) : [counts[n1,:,:,n4], edges[1], edges[2]], 
      (0, 3) : [counts[:,n2,n3,:], edges[0], edges[3]], 
      (1, 3) : [counts[n1,:,n3,:], edges[1], edges[3]], 
      (2, 3) : [counts[n1,n2,:,:], edges[2], edges[3]], 
    }

    smooth_slices = {
      (0, 1) : [smooth_counts[:,:,n3,n4], edges[0], edges[1]], 
      (0, 2) : [smooth_counts[:,n2,:,n4], edges[0], edges[2]], 
      (1, 2) : [smooth_counts[n1,:,:,n4], edges[1], edges[2]], 
      (0, 3) : [smooth_counts[:,n2,n3,:], edges[0], edges[3]], 
      (1, 3) : [smooth_counts[n1,:,n3,:], edges[1], edges[3]], 
      (2, 3) : [smooth_counts[n1,n2,:,:], edges[2], edges[3]], 
    }

    for i,j in smooth_proj.keys() : 

      if verbose : print(f"Plots for 2D projection ({names[i]}, {names[j]})")

      with plot(f"{names[i]}_{names[j]}_data_proj", prefix) as (fig, ax) : 
        plot_distr2d(norm_data, i, j, bins = 2*[50], ranges = (normalise_ranges[i], normalise_ranges[j]), 
             fig = fig, ax = ax, labels = ("Normalised " + labels[i], "Normalised " + labels[j]), weights = weights, cmap = "jet", log = log, 
             title = "Data projection")

      with plot(f"{names[i]}_{names[j]}_smooth_proj", prefix) as (fig, ax) : 
        plot_hist2d(smooth_proj[(i,j)], fig = fig, ax = ax, labels = ("Normalised " + labels[i], "Normalised " + labels[j]), log = log, cmap = "jet", 
                  title = "Smoothed projection")

      with plot(f"{names[i]}_{names[j]}_data_slice", prefix) as (fig, ax) : 
        plot_hist2d(data_slices[(i,j)], fig = fig, ax = ax, labels = ("Normalised " + labels[i], "Normalised " + labels[j]), log = log, cmap = "jet", 
                  title = "Data slice")

      with plot(f"{names[i]}_{names[j]}_smooth_slice", prefix) as (fig, ax) : 
        plot_hist2d(smooth_slices[(i,j)], fig = fig, ax = ax, labels = ("Normalised " + labels[i], "Normalised " + labels[j]), log = log, cmap = "jet", 
                  title = "Smoothed slice")

    #plt.tight_layout(pad=1., w_pad=1., h_pad=0.5)
    if interactive_plots : plt.show()

  return smooth_counts, edges, normaliser

def resample_data(data, config, variable, template, chunk_size = 50000, verbose = False) : 
  """
  Perform resampling of data sample using the template created by create_template function.

  Args: 
    data: numpy 2D array with input data 
    config: calibration sample configuration dictionary.
    variable: variable definition dictionary.
    template: PID template structure.
    chunk_size: Size of data chunk for vectorised processing.

  Returns: 
    Tuple of (pid_arr, pid_stat), where
      pid_arr: numpy 1D array of resampled PID data. 
      pid_stat: numpy 1D array of effective template statistics per each event.
  """

  counts, edges, normaliser = template

  normalise_methods = [variable["normalise_method"]] + config["normalise_methods"]
  normalise_ranges = [variable["normalise_range"]] + config["normalise_ranges"]
  resample_bins = variable["resample_bins"]
  transform_backward = eval("lambda x : (" + variable["transform_backward"] + ")")

  norm_data = de.normalise(data, normaliser[1:], normalise_methods[1:])

  if (verbose) : 
    print(f"Normalised data: {norm_data}")

  start_index = 0
  chunk = 0
  resampled_pid_arrs = []
  pid_calib_stats = []
  stop = False
  chunks = (len(norm_data)-1)//chunk_size+1

  while not stop : 
    print(f"Resampling chunk {chunk+1}/{chunks}, index={start_index}/{len(norm_data)}")
    end_index = start_index + chunk_size
    if end_index >= len(norm_data) :
      end_index = len(norm_data)
      stop = True

    rnd = onp.random.uniform(size = (end_index-start_index, ))
    norm_pid, stats = de.resample(counts, edges, norm_data[start_index:end_index,], 
                          rnd = rnd, range = normalise_ranges[0], 
                          bins = resample_bins)
    unnorm_pid = de.unnormalise(norm_pid, normaliser[0:1], normalise_methods)
    resampled_pid = transform_backward(unnorm_pid)

    resampled_pid_arrs += [ resampled_pid ]
    pid_calib_stats += [ stats ]

    start_index += chunk_size
    chunk += 1

  resampled_pid_arr = np.concatenate(resampled_pid_arrs, axis = 0)
  pid_calib_stat = np.concatenate(pid_calib_stats, axis = 0)
  return resampled_pid_arr, pid_calib_stat

  #output_data = np.concatenate([data[start_index:end_index,:], norm_data[start_index:end_index,:], unnorm_data[:nev,:], 
  #                              norm_pid, unnorm_pid, resampled_pid], axis = 1)
  #write_array("output.root", output_data, branches = 
  #            ["pid", "pt", "eta", "ntr", "sw", 
  #             "normpid", "normpt", "normeta", "normntr", 
  #             "unnormpid", "unnormpt", "unnormeta", "unnormntr", 
  #             "normpidgen", "pidgen", "respidgen"])
