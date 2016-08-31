# rockstar_tree_walker

Python code for analyzing rockstar merger trees. 

There are two user-facing utilities in this repo:

1. `create_binary_trunk_reduction_files`, a command-line script used to reduce ASCII data storing Rockstar hlist merger tree files into a collection of Numpy binaries. 
2. The `trunk_generator`, which iterates over the binary files and successively yields main progenitor histories of every (sub)halo in the simulation, one by one. 

For help on running the script:

$ python create_binary_trunk_reduction_files.py --help

For an explicit example usage of the `trunk_generator`, see the `tabulate_mpeak` function in the `example_calculations module`. This function calculates the peak historical mass for every (sub)halo in the simulation and saves the result as a Numpy binary. 

## Using the binary files

All binaries can be loaded into memory as

``` arr = numpy.load(fname)
```

The binary files have a simple organization described below. 

* For each spatial subvolume, there is a dedicated subdirectory, e.g., `subvol_0_2_1`. 
* In each such subvolume directory, there are a collection of sub-directories, one for each halo property that has been reduced to a binary, e.g., `subvol_0_2_1/halo_id` and `subvol_0_2_1/mvir`.
* The file `subvol_0_2_1/mvir/mvir_data_float32.npy`  stores a Numpy binary containing the main progenitor histories of virial mass for every z=0 (sub)halo in 0_2_1. 
* The file `subvol_0_2_1/new_trunk_indices_data_int64.npy` contains the indices separating one trunk from another. To select the array of virial masses of the *i*th halo in the subvolume: 

```
idx_fname = "subvol_0_2_1/new_trunk_indices_data_int64.npy"
mvir_fname = "subvol_0_2_1/mvir/mvir_data_float32.npy"
scale_factor_fname = "subvol_0_2_1/scale_factor/scale_factor_data_float32.npy"

idx_new_trunks = numpy.load(idx_fname)
mvir_array = numpy.load(mvir_fname)
scale_factor_array = numpy.load(scale_factor_fname)

i = 20
mvir_trunk20 = mvir_array[idx_new_trunks[i]:idx_new_trunks[i+1]]
scale_factor_trunk20 = scale_factor_array[idx_new_trunks[i]:idx_new_trunks[i+1]]
```

The above code would let you plot Mvir(a) for the 20th halo in subvolume `0_2_1`, with the first element of these arrays corresponding to the redshift-zero snapshot. 

## Performance notes

The `trunk_generator` is intended to be convenient and completely general; this is at the cost of performance, as everything here is done in pure python. Performance improvements of at least an order of magnitude are possible if you write your own iteration in cython. In such a case, you may still find the following two filename generators useful: `trunk_array_fname_generator` and `trunk_indices_fname_generator`. 













