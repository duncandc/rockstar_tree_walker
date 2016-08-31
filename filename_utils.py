""" Functions used for generating and interpreting typical filename patterns
used in rockstar hlist analysis.
"""
import string
import os
import fnmatch
import numpy as np


__all__ = ('base_10_signed_int_to_base_n_signed_int', 'tree_subvol_substring_from_int')


def base_10_signed_int_to_base_n_signed_int(i, n):
    digs = string.digits + string.letters

    if i < 0:
        sign = -1
    elif i == 0:
        return digs[0]
    else:
        sign = 1
    i *= sign

    digits = []
    while i:
        digits.append(digs[i % n])
        i /= n

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return int(''.join(digits))


def tree_subvol_substring_from_int(i, n):
    """ From any non-negative integer i, and n subdivisions per dimension,
    return the substring designating the corresponding subvolume.

    For an explicit example, the following (i, n) pairs yield the values below:

    (2, 5) --> '0_0_2'
    (5, 5) --> '0_1_0'
    (24, 5) --> '0_4_4'
    (25, 5) --> '1_0_0'
    """
    error_msg = ("The `tree_subvol_substring_from_int` function "
        "is only intended \nto work with 3d subvolumes "
        "with at most 10 subdivisions per dimension.\n"
        "You selected n = {0} subdivisions, for which there are "
        "at most {1} different subvolumes, \n"
        "exceeding your request for file number i = {2}.".format(n, n**3, i))

    s = str(base_10_signed_int_to_base_n_signed_int(i, n))
    if len(s) == 1:
        return '0_0_'+s
    elif len(s) == 2:
        return '0_'+s[0]+'_'+s[1]
    elif len(s) == 3:
        return '_'.join(s)
    else:
        raise ValueError(error_msg)


def _binary_fname_from_structured_arr_column(arr, colname):
    """ For column  ``colname`` of an input structured array ``arr``,
    use the dtype to create a string that will be used as the basename
    of the file storing a Numpy binary of the data for that column.
    """
    msg = "Column name ``{0}`` does not appear in input array".format(colname)
    assert colname in arr.dtype.names, msg

    type_string = str(arr[colname].dtype.type.__name__)
    return colname + '_data_' + type_string


def fname_generator(input_dirname, filepat):
    """ Yield all the files in ``input_dirname`` with basenames matching
    the specified file pattern.
    """
    for path, dirlist, filelist in os.walk(input_dirname):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)


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


def trunk_generator(trunks_dirname, ndivs, *haloprop_names):

    idx_trunks_gen = trunk_indices_generator(trunks_dirname, ndivs)
    haloprop_generators = list(trunk_array_generator(trunks_dirname, ndivs, name)
        for name in haloprop_names)

    for subvol_substr, trunks in _trunks_from_iterables(idx_trunks_gen, *haloprop_generators):
        yield subvol_substr, trunks
