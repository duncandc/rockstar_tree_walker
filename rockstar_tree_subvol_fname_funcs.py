"""
"""
from base10_int_to_baseN_int import base_10_signed_int_to_base_n_signed_int as b10_to_n


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

    s = str(b10_to_n(i, n))
    if len(s) == 1:
        return '0_0_'+s
    elif len(s) == 2:
        return '0_'+s[0]+'_'+s[1]
    elif len(s) == 3:
        return '_'.join(s)
    else:
        raise ValueError(error_msg)
