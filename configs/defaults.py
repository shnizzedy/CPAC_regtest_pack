feature_headers = {
    'GS': {
        'name': 'global signal regression',
        'link': 'https://fcp-indi.github.io/docs/user/nuisance.html#'
                'global-signal-regression',
        'C-PAC': ['GlobalSignalMean0', 'GlobalSignal_mean'],
        'fmriprep': 'global_signal'
    },
    'CSF': {
        'name': 'mean cerebrospinal fluid',
        'link': 'https://fcp-indi.github.io/docs/user/nuisance.html#'
                'mean-white-matter-csf',
        'C-PAC': ['CerebrospinalFluidMean0', 'CerebrospinalFluid_mean'],
        'fmriprep': 'csf'
    },
    'WM': {
        'name': 'mean white matter',
        'link': 'https://fcp-indi.github.io/docs/user/nuisance.html#'
                'mean-white-matter-csf',
        'C-PAC': ['WhiteMatterMean0', 'WhiteMatter_mean'],
        'fmriprep': 'white_matter'
    },
    'aCompCor': {
        'name': 'aCompCor',
        'link': 'https://fcp-indi.github.io/docs/user/nuisance.html#acompcor',
        'C-PAC': ['aCompCorPC', 'aCompCor'],
        'fmriprep': 'aCompCor_comp_cor_0'
    },
    'tCompCor': {
        'name': 'tCompCor',
        'link': 'https://fcp-indi.github.io/docs/user/nuisance.html#tcompcor',
        'C-PAC': ['tCompCorPC', 'tCompCor'],
        'fmriprep': 'tCompCor_comp_cor_0'
    },
    'FD': {
        'name': 'framewise displacement',
        'link': 'https://fcp-indi.github.io/docs/user/nuisance.html#'
                'regression-of-motion-parameters'
    }
}
motion_list = ['FD']
regressor_list = [
    'GS',
    'CSF',
    'WM',
    'tCompCor0',
    'aCompCor0',
    'aCompCor1',
    'aCompCor2',
    'aCompCor3',
    'aCompCor4'
]
software = ["C-PAC", "fmriprep"]
