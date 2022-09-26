import sys
import scipy
from scipy import stats
import numpy as np
import pandas as pd

oned_one_file = str(sys.argv[1])
oned_two_file = str(sys.argv[2])

cols = None
try:
    cols = [str(sys.argv[3])]
except IndexError:
    cols = None

if "nuisance_regressors.1D" in oned_one_file:
    reg_one_df = pd.read_csv(oned_one_file, delimiter="\t", header=2)
    reg_two_df = pd.read_csv(oned_two_file, delimiter="\t", header=2)

    if not cols:
        cols = reg_one_df.columns

    corrs = ["{0}: {1}\n".format(x, scipy.stats.pearsonr(reg_one_df[x].values, reg_two_df[x].values)[0]) for x in cols]

elif "roi_stats.csv" in oned_one_file:
    reg_one_df = pd.read_csv(oned_one_file, header=1)
    reg_two_df = pd.read_csv(oned_two_file)

    if not cols:
        cols = reg_one_df.columns

    corrs = ["{0}: {1}\n".format(x, scipy.stats.pearsonr(reg_one_df[x].values, reg_two_df[x].values)[0]) for x in cols]

elif "spatial_map_timeseries.txt" in oned_one_file or ".par" in oned_one_file:
    reg_one_df = pd.read_csv(oned_one_file, delimiter="  ", header=None)
    reg_two_df = pd.read_csv(oned_two_file, delimiter="  ", header=None)

    if not cols:
        cols = reg_one_df.columns

    corrs = ["{0}: {1}\n".format(x, scipy.stats.pearsonr(reg_one_df[x].values, reg_two_df[x].values)[0]) for x in cols]

else:

    with open(oned_one_file, 'r') as f:
        lines = f.readlines()

    line_idx = 0
    delimiter = ','
    for line in lines:
        if '#' in line or "Mean_" in line:
            line_idx += 1
        else:
            if ',' in line:
                delimiter = ','
            elif '\t' in line:
                delimiter = '\t'
            else:
                delimiter = ' '
            break

    if '.par' in oned_one_file:
        delimiter = '  '

    header_line = line_idx-1
    if header_line < 0:
        header_line = None

    oned_one = pd.read_csv(oned_one_file, delimiter=delimiter, header=header_line).dropna(axis=1)
    oned_two = pd.read_csv(oned_two_file, delimiter=delimiter, header=header_line).dropna(axis=1)

    if cols:
        if '#' in cols:
            cols = [cols.replace('#','')]
    else:
        cols = [x.replace('#','') for x in oned_one.columns if isinstance(x, str)]

    if not cols:
        cols = range(0,oned_one.shape[1])

    corrs = np.asarray([f"{val}: {scipy.stats.pearsonr(oned_one.values.T[x], oned_two.values.T[x])[0]}" for x, val in enumerate(cols)])

for corr in corrs:
    print(corr)
