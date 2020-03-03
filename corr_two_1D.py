import sys
import scipy
from scipy import stats
import numpy as np
import pandas as pd

oned_one_file = str(sys.argv[1])
oned_two_file = str(sys.argv[2])

with open(oned_one_file, 'r') as f:
    lines = f.readlines()

line_idx = 0
delimiter = ','
for line in lines:
    if '#' in line:
        line_idx += 1
    else:
        if ',' in line:
            delimiter = ','
        elif '\t' in line:
            delimiter = '\t'
        break

oned_one = pd.read_csv(oned_one_file, delimiter=delimiter, header=line_idx-1).dropna(axis=1)
oned_two = pd.read_csv(oned_two_file, delimiter=delimiter, header=line_idx-1).dropna(axis=1)

corrs = np.asarray([scipy.stats.pearsonr(oned_one[x], oned_two[x])[0] for x in oned_one.columns]).mean()
print(corrs)

