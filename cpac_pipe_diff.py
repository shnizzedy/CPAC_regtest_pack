
import yaml
import math


def read_yaml_file(yaml_file):
    with open(yaml_file, 'r') as f:
        yaml_dct = yaml.load(f)
    return yaml_dct


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def dct_diff(dct1, dct2):
    diff = {}
    for key in dct1:

        if 'Directory' in key or 'maxCores' in key or 'numParticipants' in key \
                or 'maximumMemory' in key or 'pipelineName' in key:
            continue

        dct1_val = dct1.get(key)
        dct2_val = dct2.get(key)
        
        if isinstance(dct1_val, float) and isinstance(dct2_val, float):
            if isclose(dct1_val, dct2_val):
                continue
            else:
                diff[key] = (dct1_val, dct2_val)

        if dct1_val != dct2_val:
            diff[key] = (dct1_val, dct2_val)

    return diff
            

def main():

    import os
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("pipe1", type=str, \
                            help="path to a C-PAC pipeline configuration " \
                                 "YAML file")

    parser.add_argument("pipe2", type=str, \
                            help="path to a C-PAC pipeline configuration " \
                                 "YAML file")

    args = parser.parse_args()

    pipe_dct1 = read_yaml_file(args.pipe1)
    pipe_dct2 = read_yaml_file(args.pipe2)

    diff_dct = dct_diff(pipe_dct1, pipe_dct2)

    for key in diff_dct:
        print("{0}: {1}".format(key, diff_dct[key]))


if __name__ == "__main__":
    main()
