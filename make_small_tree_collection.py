"""
"""
import numpy as np
import os
from rockstar_tree_subvol_fname_funcs import tree_subvol_substring_from_int as fname_from_int

tree_basename = "tree_0_2_2.dat"
tree_dirname = "/Users/aphearin/work/sims/bolplanck/trees"
tree_fname = os.path.join(tree_dirname, tree_basename)


def char_generator(hlist_filename):
    with open(hlist_filename, 'r') as f:
        for i, raw_line in enumerate(f):
            if raw_line[0] == '#':
                yield i


def last_header_index(hlist_filename):
    """ Return the index of the final header line that begins with '#',
    starting from index-0. The subsequent line that has index equal to
    last_header_index + 1 is a special line storing only a single integer,
    num_total_trees. After that special line, the repeating pattern begins.
    """
    with open(hlist_filename, 'r') as f:
        for i, raw_line in enumerate(f):
            if raw_line[0] != '#':
                return i


def read_header(hlist_filename):
    """ Return the header as a list of strings, each beginning with '#'
    """
    with open(hlist_filename, 'r') as f:
        while True:
            header_line = next(f)
            if header_line[0] == '#':
                yield header_line.strip()
            else:
                break


# chararr = np.array(list(char_generator(tree_fname)))
idx_final_header_line = last_header_index(tree_fname)
header = list(read_header(tree_fname))


# with open(tree_fname, 'r') as f:
#     for i in range(idx_final_header_line):
#         raw_line = next(f)
#         print(i, raw_line)
#     print("\n now for the next line in the file:\n\n")
#     print(next(f))
#     print("\n now for the next line in the file:\n\n")
#     print(next(f))
#     print("\n now for the next line in the file:\n\n")
#     print(next(f))
#     print("\n\n")
