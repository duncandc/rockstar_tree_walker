""" Iterators used to walk the binary trunk reductions
"""
import numpy as np
import os
from filename_utils import tree_subvol_substring_from_int, fname_generator


def trunk_generator(trunks_dirname, ndivs, *haloprop_names):

    idx_trunks_gen = trunk_indices_generator(trunks_dirname, ndivs)
    haloprop_generators = list(trunk_array_generator(trunks_dirname, ndivs, name)
        for name in haloprop_names)

    for subvol_substr, trunks in _trunks_from_iterables(idx_trunks_gen, *haloprop_generators):
        yield subvol_substr, trunks


def trunk_array_fname_generator(trunk_dirname, ndivs, propname):
    imax = ndivs**3
    for i in range(imax):
        subvol_substr = tree_subvol_substring_from_int(i, ndivs)
        subvol_dirname = os.path.join(trunk_dirname, 'subvol_'+subvol_substr, propname)
        filepat = propname + '_data*.npy'
        for fname in fname_generator(subvol_dirname, filepat):
            yield fname


def trunk_indices_fname_generator(trunk_dirname, ndivs):
    basename = "new_trunk_indices_data_int64.npy"
    imax = ndivs**3
    for i in range(imax):
        subvol_substr = tree_subvol_substring_from_int(i, ndivs)
        yield subvol_substr, os.path.join(trunk_dirname, 'subvol_'+subvol_substr, basename)


def trunk_array_generator(trunk_dirname, ndivs, propname):
    for fname in trunk_array_fname_generator(trunk_dirname, ndivs, propname):
        yield np.load(fname)


def trunk_indices_generator(trunk_dirname, ndivs):
    for subvol_substr, fname in trunk_indices_fname_generator(trunk_dirname, ndivs):
        yield subvol_substr, np.load(fname)


def _trunks_from_iterables(idx_iterable, *haloprop_iterables):
    for subvol_data in zip(idx_iterable, *haloprop_iterables):
        idx_data = subvol_data[0]
        haloprop_arrays = subvol_data[1:]
        subvol_substr = idx_data[0]
        idx_new_trunks = np.append(idx_data[1], len(haloprop_arrays[0]))
        for ifirst, ilast in zip(idx_new_trunks[:-1], idx_new_trunks[1:]):
            yield subvol_substr, tuple(haloprop_array[ifirst:ilast] for haloprop_array in haloprop_arrays)
