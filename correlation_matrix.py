# coding=utf-8
import sys

if (sys.version_info < (3, 6)):
    raise EnvironmentError("This module requires Python 3.6 or newer.")

import argparse
import glob
import numpy as np
import os
import pandas as pd
import scipy.io as sio

from afnipy.lib_afni1D import Afni1D
from itertools import chain
from scipy.stats import pearsonr
from tabulate import tabulate

try:
    from configs.defaults import feature_headers, motion_list, regressor_list, \
                                 software
    from configs.subjects import fmriprep_sub, \
                                 generate_subject_list_for_directory
    from heatmaps import generate_heatmap, reshape_corrs
except ModuleNotFoundError:
    from .configs.defaults import feature_headers, motion_list, regressor_list,\
                                  software
    from .configs.subjects import fmriprep_sub, \
                                  generate_subject_list_for_directory
    from .heatmaps import generate_heatmap, reshape_corrs

sorted_keys = list(feature_headers.keys())
sorted_keys.sort(key=str.lower)
feat_def_table = tabulate(
    [
        [
            key,
            feature_headers[key].get('name'),
            feature_headers[key].get('link')
        ] for key in sorted_keys
    ],
    headers=["key", "feature name", "documentation link"]
)
del(sorted_keys)

def calc_corr(data1, data2):
    """
    Function to calculate Pearson's r between two np.ndarrays or lists

    Parameters
    ----------
    data1: np.ndarray or list

    data2: np.ndarray or list
    """
    if not any([
        data1 is None,
        data2 is None
    ]):
        if isinstance(data1, np.ndarray) and data1.shape == data2.shape:
            return(pearsonr(data1.flatten(), data2.flatten())[0])
        if len(data1) == len(data2):
            return(pearsonr(data1, data2)[0])
        if len(data1) == len(data2) + 1:
            return(pearsonr(data1[1:], data2)[0])
        if len(data2) == len(data1) + 1:
            return(pearsonr(data1, data2[1:])[0])
    return(float(np.nan))


def main():
    parser = argparse.ArgumentParser(
        description="Create a correlation matrix between two C-PAC output "
                    "directories.",
        epilog="The following features currently have available definitions to "
               "calculate Pearson's \x1B[3mr\x1B[23m between C-PAC and "
               f"fmriprep:\n\n{feat_def_table}",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    path_help = ("path to an outputs directory - the "
                 "folder containing the participant-ID "
                 "labeled directories")

    parser.add_argument("--old_outputs_path", type=str,
                        help=path_help, default="fmriprep")

    parser.add_argument("--old_outputs_software", type=str,
                        choices=software, default="fmriprep",
                        help="(default: %(default)s)")

    parser.add_argument("--new_outputs_path", type=str,
                        help=path_help)

    parser.add_argument("--new_outputs_software", type=str,
                        choices=software, default="C-PAC",
                        help="(default: %(default)s)")

    parser.add_argument("--save", dest="save", action='store_true',
                        help="save matrices & heatmap (default)")

    parser.add_argument("--no-save", dest="save", action='store_false',
                        help="do not save matrices & heatmap")

    parser.set_defaults(save=True)

    parser.add_argument("--subject_list", type=str,
                        help="(default: subjects in OLD_OUTPUTS_PATH sorted by "
                             "session, subject ID). TODO: handle path to file")

    parser.add_argument("--session", type=int,
                        help="limit to a single given session (integer)")

    parser.add_argument("--feature_list", type=str,
                        default=regressor_list + motion_list,
                        help="TODO: handle path to file (default: %(default)s)")

    parser.add_argument("num_cores", type=int, \
                            help="number of cores to use - will calculate " \
                                 "correlations in parallel if greater than 1")

    parser.add_argument("run_name", type=str, \
                            help="name for the correlations run")

    args = parser.parse_args()

    subject_list = args.subject_list if (
        "subject_list" in args and args.subject_list is not None
    ) else generate_subject_list_for_directory(args.old_outputs_path)

    if "session" in args and args.session is not None:
        subject_list = [
            sub for sub in subject_list if sub.endswith(str(args.session))
        ]

    corrs = Correlation_Matrix(
        subject_list,
        args.feature_list,
        [{
            "software": args.new_outputs_software,
            "run_path": args.new_outputs_path if args.new_outputs_path.endswith(
                "/"
            ) else f"{args.new_outputs_path}/"
        }, {
            "software": args.old_outputs_software,
            "run_path": args.old_outputs_path if args.old_outputs_path.endswith(
                "/"
            ) else f"{args.old_outputs_path}/"
        }]
    )

    path_table = corrs.print_filepaths(plaintext=True)

    if args.save:
        output_dir = os.path.join(
            os.getcwd(), "correlations_{0}".format(args.run_name)
        )

        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except:
                err = ("\n\n[!] Could not create the output directory for the "
                       "correlations. Do you have write permissions?\n "
                       f"Attempted output directory: {output_dir}\n\n")
                raise Exception(err)

        path_table.to_csv(os.path.join(output_dir, "filepaths.csv"))
        sio.savemat(
            os.path.join(output_dir, "corrs.mat"), {'corrs':corrs.corrs}
        )

    generate_heatmap(
        reshape_corrs(corrs.corrs),
        args.feature_list,
        subject_list,
        save_path=os.path.join(
            output_dir, "heatmap.png"
        ) if args.save else args.save,
        title=f"{args.new_outputs_software} "
        f"{args.new_outputs_path.split('/')[-1]} vs "
        f"{args.old_outputs_software} {args.old_outputs_path.split('/')[-1]}"
    )


class Subject_Session_Feature:
    """
    A class for (subject × session) × feature data
    """
    def __init__(self, subject, feature, runs):
        """
        Parameters
        ----------
        subject: str
            (subject × session)

        feature: str

        runs: list of dicts
            [{"software": str, "run_path": str}]
        """
        if "_" in subject:
            self.subject, self.session = subject.split("_", 1)
        else:
            self.subject = subject
            self.session = None
        self.feature = feature
        self.paths = (
            self.get_path(
                self.subject,
                self.feature,
                runs[0]["run_path"],
                runs[0]["software"],
                self.session
            ),
            self.get_path(
                self.subject,
                self.feature,
                runs[1]["run_path"],
                runs[1]["software"],
                self.session
            )
        )
        self.data = (
            self.read_feature(
                self.paths[0],
                self.feature,
                runs[0]["software"]
            ),
            self.read_feature(
                self.paths[1],
                self.feature,
                runs[1]["software"]
            )
        )

    def get_path(self, subject, feature, run_path, software="C-PAC",
        session=None):
        """
        Method to find a path to specific outputs

        Parameters
        ----------
        subject: str or int

        feature: str

        run_path: str

        software: str

        session: str, int or None

        Returns
        -------
        path: str
        """
        subject = str(subject)
        session = f"*{str(session)}*" if session else ""
        paths = []
        if software.lower() in ["cpac", "c-pac"]:
            if feature in regressor_list:
                paths = glob.glob(
                    f'{run_path}working/'
                    f'resting_preproc_*{subject}{session}/'
                    'nuisance_*0_0/_*/*/build*/*1D'
                )
            elif feature in motion_list:
                # frame wise displacement power
                paths = glob.glob(
                    f'{run_path}output/*/*{subject}{session}'
                    '/frame_wise_displacement_power/*/*'
                )
        elif software.lower()=="fmriprep":
            fmriprep_subject = fmriprep_sub(subject)
            if feature in regressor_list:
                paths = [
                    f'{run_path}output/fmriprep/{fmriprep_subject}/func/'
                    f'{fmriprep_subject}_task-rest_run-1'
                    '_desc-confounds_regressors.tsv'
                ]
            elif feature in motion_list:
                paths = [
                    f'{run_path}working/fmriprep_wf/'
                    f'single_subject_{fmriprep_subject[4:]}_wf/'
                    'func_preproc_task_rest_run_1_wf/'
                    'bold_confounds_wf/fdisp/fd_power_2012.txt'
                ]
        return(paths[0] if len(paths) else None)

    def read_feature(self, file, feature, software="C-PAC"):
        """
        Method to read a feature from a given file

        Parameters
        ----------
        file: str
            path to file

        feature: str

        software: str

        Returns
        -------
        feature: np.ndarray or list or None
        """
        if file is None:
            return(None)
        software = "C-PAC" if software.lower() in [
            "c-pac",
            "cpac"
        ] else software.lower()

        feature_label = feature_headers.get(feature, {}).get(software, '') if (
            "CompCor" not in feature
        ) else f"{feature[:-1]}PC{feature[-1]}" if (
            software=="C-PAC"
        ) else f"{feature[0]}_comp_cor_0{feature[-1]}" if (
            software=="fmriprep"
        ) else ""

        if software=="C-PAC":
            data = Afni1D(file)
            header = data.header[-1] if len(data.header) else ""
            header_list = header.split('\t')
            return(
                data.mat[header_list.index(feature_label)] if (
                    feature_label in header_list
                ) else data.mat[0][1:]
            )

        elif software=="fmriprep":
            if file.endswith('.tsv'):
                data = pd.read_csv(file, sep='\t')
                if feature_label in data.columns:
                    return(data[feature_label])
            elif file.endswith('.txt'):
                with open(file) as f:
                    return([
                        float(x) for x in [x.strip() for x in f.readlines()][1:]
                    ])

        return(None)

class Correlation_Matrix:
    """
    A class for (subject × session) × feature correlation matrices
    """
    def __init__(self, subject_sessions, features, runs):
        """
        Parameters
        ----------
        subject_sessions: list of strings
            ["subject_session", ...]

        features: list of strings
            ["feature", ...]

        runs: list of dicts
            [{"software": str, "run_path": str}]
        """
        self.subjects = subject_sessions
        self.features = features
        self.runs = runs
        self.data = {
            subject: {
                feature: Subject_Session_Feature(
                    subject, feature, runs
                ) for feature in features
            } for subject in subject_sessions
        }
        self.corrs = np.zeros((len(subject_sessions), len(features)))
        self.run_pearsonsr()

    def print_filepaths(self, plaintext=False):
        """
        Function to print a table
        """
        columns = ["\n".join([
            self.runs[i]["software"], wrap(self.runs[i]["run_path"])
        ]) for i in range(2)]
        path_table = pd.DataFrame(
            [[
                "Not found" if not
                self.data[sub][feat].paths[i] else (
                    self.data[sub][feat].paths[i].replace(
                        self.runs[i]["run_path"], "", 1
                    ) if self.data[sub][feat].paths[i].startswith(
                        self.runs[i]["run_path"]
                    ) else self.data[sub][feat].paths[i]
                ) for i in range(2)
            ] for sub in self.data for feat in self.data[sub]],
            columns=columns,
            index=[
                f"{sub} {feat}" for sub in self.subjects for
                feat in self.features
            ]
        )
        if plaintext:
            plaintext_path_table = pd.DataFrame(
                [[
                    f"\u001b[3m\u001b[31mNot found\u001b[0m{' '*13}" if not
                    self.data[sub][feat].paths[i] else wrap(
                        self.data[sub][feat].paths[i].replace(
                            self.runs[i]["run_path"], "", 1
                        ) if self.data[sub][feat].paths[i].startswith(
                            self.runs[i]["run_path"]
                        ) else self.data[sub][feat].paths[i]
                    ) for i in range(2)
                ] for sub in self.data for feat in self.data[sub]],
                columns=columns,
                index=[
                    f"{sub} {feat}" for sub in self.subjects for
                    feat in self.features
                ]
            )
            print(tabulate(
                plaintext_path_table,
                headers=columns
            ))
        else:
            stored_options = (
                pd.options.display.max_rows,
                pd.options.display.max_colwidth
            )
            pd.options.display.max_rows = 999
            pd.options.display.max_colwidth = 1000
            try:
                from IPython.display import display
                display(path_table)
            except:
                print(path_table)
            (
                pd.options.display.max_rows,
                pd.options.display.max_colwidth
            ) = stored_options
            del stored_options
        return(path_table)

    def run_correlation(self, subject, feature, data1, data2):
        """
        A method to fill a cell in a correlation matrix with Pearson's r

        Parameters
        ----------
        subject: int
            subject index

        feature: int
            feature index

        data1: np.ndarray or list

        data2: np.ndarray or list
        """
        corr = calc_corr(data1, data2)
        print(
            f'Running subject: {subject} {feature} '
            f'correlation score: {str(corr)}'
        )
        self.corrs[subject][feature] = round(corr, 3)

    def run_pearsonsr(self):
        for i, subject in enumerate(self.data):
            for j, feature in enumerate(self.data[subject]):
                self.run_correlation(i, j, *self.data[subject][feature].data)


def wrap(string, at=25):
    return('\n'.join([
        string[i:i+at] for i in range(0, len(string), at)
    ]))

if __name__ == "__main__":
    main()