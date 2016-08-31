""" Example usages of the primary iterator. By matching the patterns shown here,
you can calculate any quantity from the main progenitor histories to create
value-added halo catalogs supplemented with your own tree-walking results.
"""
import numpy as np
from trunk_generators import trunk_generator
import os


def mpeak_generator(trunks_dirname, ndivs):
    """ This generator loops over the trunk_generator, and for each trunk
    the maximum historical value of mvir is calculated and yielded.

    Parameters
    ----------
    trunks_dirname : string
        Absolute path to the directory where the binary trunk data is stored.

    ndivs : int
        Number of subvolume divisions per dimension (e.g., ndivs=5 for bolplanck)

    Returns
    -------
    halo_id : long
        ID of the root of the trunk

    mpeak : float
        Peak historical mass of the main progenitor
    """
    gen = trunk_generator(trunks_dirname, ndivs, 'halo_id', 'mvir')
    for subvol_substr, trunks in gen:
        halo_id_array, mvir_array = trunks
        halo_id = halo_id_array[0]
        mpeak = np.max(mvir_array)
        yield halo_id, mpeak


def tabulate_mpeak(trunks_dirname, ndivs, foutname):
    """ This function loops over the mpeak_generator and saves the result
    to a Numpy binary.

    Parameters
    ----------
    trunks_dirname : string
        Absolute path to the directory where the binary trunk data is stored.

    ndivs : int
        Number of subvolume divisions per dimension (e.g., ndivs=5 for bolplanck)

    foutname : string
        Name of the output Numpy binary.
    """
    try:
        os.makedirs(os.path.dirname(os.path.abspath(foutname)))
    except OSError:
        pass

    dt = np.dtype([('halo_id', 'i8'), ('mpeak', 'f4')])
    result = np.array(list(mpeak_generator(trunks_dirname, ndivs)), dtype=dt)
    np.save(foutname, result)
