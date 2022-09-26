import yaml
import math


def read_yaml_file(yaml_file):
    '''Function to read a dict YAML file at a given path.

    Parameters
    ----------
    yaml_file: str
        path to YAML file

    Returns
    -------
    dict
        parsed YAML

    Example
    -------
    >>> read_yaml_file('/code/dev/docker_data/default_pipeline.yml')[
    ...     'pipeline_setup']['pipeline_name']
    'cpac-default-pipeline'
    '''
    with open(yaml_file, 'r') as f:
        yaml_dct = yaml.safe_load(f)
    return yaml_dct


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def dct_diff(dct1, dct2):
    '''Function to compare 2 nested dicts, dropping values unspecified
    in the second.

    Parameters
    ----------
    dct1: dict

    dct2: dict

    Returns
    -------
    diff: set
        a tuple of values from dct1, dct2 for each differing key

    Example
    -------
    >>> pipeline = read_yaml_file('/code/dev/docker_data/default_pipeline.yml')
    >>> dct_diff(pipeline, pipeline)
    {}
    >>> pipeline2 = read_yaml_file('/code/CPAC/resources/configs/'
    ...     'pipeline_config_fmriprep-options.yml')
    >>> dct_diff(pipeline, pipeline2)['pipeline_setup']['pipeline_name']
    ('cpac-default-pipeline', 'cpac_fmriprep-options')
    '''
    diff = {}
    for key in dct1:
        if isinstance(dct1[key], dict):
            diff[key] = dct_diff(dct1[key], dct2.get(key, {}))
        else:
            dct1_val = dct1.get(key)
            dct2_val = dct2.get(key) if isinstance(dct2, dict) else None

            # skip unspecified values
            if dct2_val is None:
                continue

            if isinstance(dct1_val, float) and isinstance(dct2_val, float):
                if isclose(dct1_val, dct2_val):
                    continue
                else:
                    diff[key] = (dct1_val, dct2_val)

            if dct1_val != dct2_val:
                diff[key] = (dct1_val, dct2_val)

    # only return non-empty diffs
    return {k: diff[k] for k in diff if diff[k]}


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
        print("{0}:\n{1}\n\n".format(key, diff_dct[key]))


if __name__ == "__main__":
    main()
