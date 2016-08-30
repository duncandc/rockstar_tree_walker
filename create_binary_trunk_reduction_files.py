""" Executable script reading hlist ascii data and producing a collection
of Numpy binaries with standardized filenames and directory locations.
"""
import argparse
import os
from simulation_column_dtype import simulation_column_dtype, sub_dtype
from filename_utils import ascii_hlist_fname_generator
from ascii_subvolume_walker import mmp_row_generator
from time import time
import numpy as np
from save_structured_array import store_structured_array_columns


parser = argparse.ArgumentParser()

parser.add_argument("input_dirname",
    help="Disk location where the hlist ascii data is stored")

parser.add_argument("output_dirname",
    help="Disk location where the Numpy binaries will be stored")

parser.add_argument("colnames",
        help="Sequence of names of the columns for which you want to create binaries. "
        "Each string in the sequence must appear in the `tree_column_info_fname` file.",
        nargs='+')

parser.add_argument("-input_hlist_filepat",
    help="Filename pattern used to identify the hlist ascii data "
    "in the input_dirname. Default is `tree_*`",
    default="tree_*")

parser.add_argument("-tree_column_info_fname",
    help="Name of the user-created ascii file "
    "used to infer the dtype of the data stored in the hlist ascii file. "
    "Must at least have ``mmp``, ``desc_id`` and ``halo_id`` as column names."
    "See simulation_column_dtype for example formatting."
    "Default assumes tree hlist files are associated with "
    "simname = `bolplanck`, version_name = `version_0p4`",
    default="bolplanck_columns.dat")


args = parser.parse_args()
try:
    os.makedirs(args.output_dirname)
except OSError:
    pass

hlist_dt = simulation_column_dtype(args.tree_column_info_fname)

assert os.path.isdir(args.input_dirname), "input_dirname is not recognized on disk"

try:
    mmp_col_index = hlist_dt.names.index('mmp')
    desc_id_col_index = hlist_dt.names.index('desc_id')
    halo_id_col_index = hlist_dt.names.index('halo_id')
except ValueError:
    msg = ("The `tree_column_info_fname` file must at least have columns named \n"
            "``mmp``, ``desc_id`` and ``halo_id``.")
    raise ValueError(msg)

colnums_to_yield = [hlist_dt.names.index(name) for name in args.colnames]

output_dt = sub_dtype(hlist_dt, args.colnames)

print("\n")
start = time()
for tree_fname in ascii_hlist_fname_generator(args.input_dirname, args.input_hlist_filepat):
    print("...working on {0}".format(os.path.basename(tree_fname)))
    subvolume_data = np.array(list(mmp_row_generator(tree_fname,
        mmp_col_index, desc_id_col_index, halo_id_col_index, *colnums_to_yield)), dtype=output_dt)

    subvol_output_dirname = os.path.join(args.output_dirname, "subvol_"+tree_fname[-9:-4])
    store_structured_array_columns(subvolume_data, subvol_output_dirname)

end = time()
print("\nTotal runtime = {0:.2f} seconds\n".format(end-start))
# print(np.shape(data))
# print(data.dtype)
# print(data['halo_id'][0:4])



