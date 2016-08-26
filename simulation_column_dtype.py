import numpy as np


def simulation_column_dtype(fname='bolplanck_columns.dat'):
    data_types = []
    with open(fname, 'r') as f:
        for raw_line in f:
            line = tuple(s for s in raw_line.strip().split('  '))
            data_types.append(line)

    return np.dtype(data_types)
