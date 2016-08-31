# rockstar_tree_walker

This repository provides code for studying the evolutionary history of rockstar halos. There is a command-line script for converting publicly available ASCII hlist files into fast-loading Numpy binaries. Once the binaries are created, there are utilities for iterating over the binaries to calculate quantities that derive from each halo's history, such as Mpeak and Vmax-at-accretion. 


There are two primary user-facing utilities:

1. `create_binary_trunk_reduction_files`, a command-line script used to reduce ASCII data storing Rockstar hlist merger tree files into a collection of Numpy binaries. 
2. The `trunk_generator`, which iterates over the binary files and successively yields main progenitor histories of every (sub)halo in the simulation, one by one. 

For help on running the script:

$ python create_binary_trunk_reduction_files.py --help

After you creat the binaries you can use the `trunk_generator` to calculate quantities deriving from the main progenitor histories. For an explicit example usage of the `trunk_generator`, see the `tabulate_mpeak` function in the `example_calculations module`. This function calculates the peak historical mass for every (sub)halo in the simulation and saves the result as a Numpy binary. By matching the pattern illustrated by the `tabulate_mpeak` function, you can calculate any quantity derivable from the main progenitor history of a halo, and store result in a convenient fashion for cross-matching against some existing halo catalog. 


## Using the binary files

After running the `create_binary_trunk_reduction_files.py` script, all binaries can be loaded into memory as


``` 
arr = numpy.load(fname)
```

The binary files have a simple organization described below. 

* For each spatial subvolume, there is a dedicated subdirectory, e.g., `subvol_0_2_1`. 
* Within each subvolume, there are a collection of sub-directories, one for each halo property that has been reduced to a binary, e.g., `subvol_0_2_1/halo_id` and `subvol_0_2_1/mvir`.
* The file `subvol_0_2_1/mvir/mvir_data_float32.npy`  stores a Numpy binary containing the main progenitor histories of virial mass for every z=0 (sub)halo in subvolume 0_2_1. 
* The file `subvol_0_2_1/new_trunk_indices_data_int64.npy` contains the indices separating one trunk from another. To select the array of virial masses of the *i*th halo in the subvolume: 

Specify the files to work with:

```
idx_fname = "subvol_0_2_1/new_trunk_indices_data_int64.npy"
mvir_fname = "subvol_0_2_1/mvir/mvir_data_float32.npy"
scale_factor_fname = "subvol_0_2_1/scale_factor/scale_factor_data_float32.npy"
```

Load the data into memory:

```
idx_trunks = numpy.load(idx_fname)
mvir_array = numpy.load(mvir_fname)
a_array = numpy.load(scale_factor_fname)
```

Retrieve arrays for the virial mass history of the 20th halo, as well as the scale factor at which each mass is attained: 

```
i = 20
mvir_trunk20 = mvir_array[idx_trunks[i]:idx_trunks[i+1]]
a_trunk20 = a_array[idx_trunks[i]:idx_trunks[i+1]]
```

The above code would let you directly plot *Mvir(a)* for the 20th halo in subvolume `0_2_1`, with the first element of these arrays corresponding to the redshift-zero snapshot (a=1). 

## Cross-matching with a halo catalog

The most common use-case for these utilities is to create some value-added data to supplement the information contained in an existing halo catalog. To do this cross-matching, you may find it useful to use the `crossmatch` function located in `halotools` (https://github.com/astropy/halotools):

```
from halotools.utils import crossmatch
```

`crossmatch` is a highly efficient function for matching integer IDs; this function is implemented in a standalone module with Numpy as the only dependency. 

## Performance notes

The `trunk_generator` is intended to be convenient and completely general; this is at the cost of performance, as everything here is done in pure python. Performance improvements of at least an order of magnitude are possible if you write your own iteration in cython. In such a case, you may still find the following two filename generators useful: `trunk_array_fname_generator` and `trunk_indices_fname_generator`. 

## Comments and questions

Contact Andrew Hearin by email or **@aphearin** on GitHub. 












