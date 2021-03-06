#!/usr/bin/python

import numpy as np
import scipy
from scipy import stats
import pandas as pd


def read_txt_file(txt_file):
    with open(txt_file,"r") as f:
        strings = f.read().splitlines()
    return strings


def read_csv_into_df(csv_file, header_row=None):
    if header_row:
        csvdf = pd.read_csv(csv_file, header=header_row, delimiter="\t", comment="#")
    else:
        csvdf = pd.read_csv(csv_file, delimiter="\t", comment="#")  
    return csvdf


def concordance(x, y, rho):
    """
    Calculates Lin's concordance correlation coefficient.

    Usage: concordence(x, y) where x, y are equal-length arrays
    Returns: concordance correlation coefficient

    Note: strict than pearson
    """

    import math
    import numpy as np

    map(float, x)
    map(float, y)
    xvar = np.var(x)
    yvar = np.var(y)
    #rho = scipy.stats.pearsonr(x, y)[0]
    #p = np.corrcoef(x,y)  # numpy version of pearson correlation coefficient
    ccc = 2. * rho * math.sqrt(xvar) * math.sqrt(yvar) / (xvar + yvar + (np.mean(x) - np.mean(y))**2)

    return ccc


def correlate(data_1, data_2):
    pearson = scipy.stats.pearsonr(data_1, data_2)[0]
    concor = concordance(data_1, data_2, pearson)
    return concor


def quick_corr_csv(csv_1, csv_2):
    csv_1_data = read_csv_into_df(csv_1)
    csv_2_data = read_csv_into_df(csv_2)

    concors = []

    for col, col2 in zip(csv_1_data, csv_2_data):
        try:
            concor = correlate(csv_1_data[col], csv_2_data[col2])
            concors.append(concor)
            print("{0}: {1}".format(col2, concor))
        except KeyError:
            print("different name now - {0}".format(col))
    else:
        print("Data not same shape")

    print("\nAverage concordance correlation of all columns:")
    print(np.asarray(concors).mean())


def main():
    import argparse

    parser = argparse.ArgumentParser()
                                 
    parser.add_argument("csv1", type=str)
    parser.add_argument("csv2", type=str)

    args = parser.parse_args()

    quick_corr_csv(args.csv1, args.csv2)


if __name__ == "__main__":
    main()
