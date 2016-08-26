"""
"""
import os
import numpy as np


def store_structured_array(arr, parent_dirname, columns_to_save='all'):
    """
    """
    dt = arr.dtype
    if columns_to_save == 'all':
        columns_to_save = dt.names
    for colname in columns_to_save:
        msg = "Column name ``{0}`` does not appear in input array".format(colname)
        assert colname in dt.names, msg
        output_dirname = os.path.join(parent_dirname, colname)
        try:
            os.makedirs(output_dirname)
        except OSError:
            pass
        output_fname = os.path.join(output_dirname, column_filename(arr, colname))
        np.save(output_fname, arr[colname])


def column_filename(arr, colname):
    """
    """
    msg = "Column name ``{0}`` does not appear in input array".format(colname)
    assert colname in arr.dtype.names, msg

    type_string = str(arr[colname].dtype.type.__name__)
    return colname + '_data_' + type_string

