"""
"""


def mmp_row_generator(tree_fname, mmp_col_index, desc_id_col_index, halo_id_col_index,
        *colnums_to_yield):
    """ Given an input hlist ASCII file, yield the desired columns of all rows
    storing the main progenitors in the file.
    """

    with open(tree_fname, 'r') as f:

        # Skip the header, extracting num_trees
        while True:
            raw_header_line = next(f)
            if raw_header_line[0] != '#':
                break

        # Iterate over remaining ascii lines
        while True:
            try:
                raw_line = next(f)
                if raw_line[0] == '#':
                    current_tree_root_id = raw_line.strip().split()[1]
                else:
                    list_of_strings = raw_line.strip().split()
                    mmp = list_of_strings[mmp_col_index]
                    desc_id = list_of_strings[desc_id_col_index]
                    halo_id = list_of_strings[halo_id_col_index]
                    string_data = tuple(list_of_strings[idx] for idx in colnums_to_yield)
                    yield_current_line = ((mmp == '1') & (desc_id == current_tree_root_id) |
                        (current_tree_root_id == halo_id))
                    if yield_current_line:
                        yield string_data

            except StopIteration:
                break
