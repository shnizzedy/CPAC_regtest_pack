import sys
import scipy
from scipy import stats
import numpy as np

oned_one = str(sys.argv[1])
oned_two = str(sys.argv[2])

def parse_oned_file(oned_file):
    with open(oned_file, 'r') as f:
        file_lines = f.readlines()
        file_lines = [float(x.rstrip('\n')) for x in file_lines]
    return file_lines

fileone_lines = parse_oned_file(oned_one)
filetwo_lines = parse_oned_file(oned_two)

print(scipy.stats.pearsonr(fileone_lines, filetwo_lines)[0])
