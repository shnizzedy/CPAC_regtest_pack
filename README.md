# CPAC_regtest_pack

```bash
$ python cpac_correlations_wf.py --help
usage: cpac_correlations_wf.py [-h] [--old_outputs_path OLD_OUTPUTS_PATH]
                               [--new_outputs_path NEW_OUTPUTS_PATH]
                               [--s3_creds S3_CREDS]
                               [--replacements REPLACEMENTS]
                               [--corr_map CORR_MAP]
                               [--working_dir WORKING_DIR]
                               num_cores run_name

positional arguments:
  num_cores             number of cores to use - will calculate correlations
                        in parallel if greater than 1
  run_name              name for the correlations run

optional arguments:
  -h, --help            show this help message and exit
  --old_outputs_path OLD_OUTPUTS_PATH
                        path to a CPAC outputs directory - the folder
                        containing the participant-ID labeled directories
  --new_outputs_path NEW_OUTPUTS_PATH
                        path to a CPAC outputs directory - the folder
                        containing the participant-ID labeled directories
  --s3_creds S3_CREDS   path to your AWS S3 credentials file
  --replacements REPLACEMENTS
                        text file containing strings you wish to have removed
                        from the filepaths if they occur - place one on each
                        line
  --corr_map CORR_MAP   YAML file with already-calculated correlations, which
                        can be provided if you only want to generate the box
                        plots again
  --working_dir WORKING_DIR
                        if you are correlating two working directories of a
                        single participant to check intermediates
```

```bash
$ python correlation_matrix.py --help
usage: correlation_matrix.py [-h] [--old_outputs_path OLD_OUTPUTS_PATH]
                             [--old_outputs_software {C-PAC,fmriprep}]
                             [--new_outputs_path NEW_OUTPUTS_PATH]
                             [--new_outputs_software {C-PAC,fmriprep}]
                             [--save] [--no-save]
                             [--subject_list SUBJECT_LIST] [--session SESSION]
                             [--feature_list FEATURE_LIST]
                             num_cores run_name

Create a correlation matrix between two C-PAC output directories.

positional arguments:
  num_cores             number of cores to use - will calculate correlations
                        in parallel if greater than 1
  run_name              name for the correlations run

optional arguments:
  -h, --help            show this help message and exit
  --old_outputs_path OLD_OUTPUTS_PATH
                        path to an outputs directory - the folder containing
                        the participant-ID labeled directories
  --old_outputs_software {C-PAC,fmriprep}
                        (default: fmriprep)
  --new_outputs_path NEW_OUTPUTS_PATH
                        path to an outputs directory - the folder containing
                        the participant-ID labeled directories
  --new_outputs_software {C-PAC,fmriprep}
                        (default: C-PAC)
  --save                save matrices & heatmap (default)
  --no-save             do not save matrices & heatmap
  --subject_list SUBJECT_LIST
                        (default: subjects in OLD_OUTPUTS_PATH sorted by
                        session, subject ID). TODO: handle path to file
  --session SESSION     limit to a single given session (integer)
  --feature_list FEATURE_LIST
                        TODO: handle path to file (default: ['GS', 'CSF',
                        'WM', 'tCompCor0', 'aCompCor0', 'aCompCor1',
                        'aCompCor2', 'aCompCor3', 'aCompCor4', 'FD'])

The following features currently have available definitions to calculate Pearson's r between C-PAC and fmriprep:

key       feature name              documentation link
--------  ------------------------  ----------------------------------------------------------------------------------
aCompCor  aCompCor                  https://fcp-indi.github.io/docs/user/nuisance.html#acompcor
CSF       mean cerebrospinal fluid  https://fcp-indi.github.io/docs/user/nuisance.html#mean-white-matter-csf
FD        framewise displacement    https://fcp-indi.github.io/docs/user/nuisance.html#regression-of-motion-parameters
GS        global signal regression  https://fcp-indi.github.io/docs/user/nuisance.html#global-signal-regression
tCompCor  tCompCor                  https://fcp-indi.github.io/docs/user/nuisance.html#tcompcor
WM        mean white matter         https://fcp-indi.github.io/docs/user/nuisance.html#mean-white-matter-csf
```