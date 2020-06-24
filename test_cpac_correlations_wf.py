

def test_create_unique_file_dict():

    try:
        from cpac_correlations_wf import create_unique_file_dict
    except ModuleNotFoundError:
        from .cpac_correlations_wf import create_unique_file_dict

    filepaths = [
      "/path/sub001/centrality_outputs/_scan_rest_1/degree_centrality_weighted.nii.gz",
      "/path/sub001/centrality_outputs/_scan_rest_1/eigenvector_centrality_weighted.nii.gz",
      "/path/sub002/alff_to_standard_smooth/_scan_rest_1/file.nii.gz"
    ]

    output_folder = "/path"

    # output dictionary should have dictionaries as values, which have tuples 
    # as keys, where the tuple identifies the same file across different CPAC
    # versions (and thus potentially different filepaths)
    #   multiple dictionary levels to make it easy to pull up all of the
    #   entries for one particular derivative
    ref_output = {
      'alff_to_standard_smooth':
        {('alff_to_standard_smooth', 
          '/sub002/alff_to_standard_smooth/_scan_rest_1/', '1'):
            ['/path/sub002/alff_to_standard_smooth/_scan_rest_1/file.nii.gz']},
      'centrality_outputs: degree': 
        {('centrality_outputs: degree', 
          '/sub001/centrality_outputs/_scan_rest_1/', '1'): 
            ['/path/sub001/centrality_outputs/_scan_rest_1/degree_centrality_weighted.nii.gz']},
      'centrality_outputs: eigenvector': 
        {('centrality_outputs: eigenvector', 
          '/sub001/centrality_outputs/_scan_rest_1/', '1'):
            ['/path/sub001/centrality_outputs/_scan_rest_1/eigenvector_centrality_weighted.nii.gz']}
    }

    file_dict = create_unique_file_dict(filepaths, output_folder)

    assert ref_output == file_dict


def test_create_unique_file_dict_with_replacements():

    try:
        from cpac_correlations_wf import create_unique_file_dict
    except ModuleNotFoundError:
        from .cpac_correlations_wf import create_unique_file_dict

    filepaths = [
      "/path/sub001_site1/centrality_outputs/_scan_rest_1/degree_centrality_weighted.nii.gz",
      "/path/sub001_site1/centrality_outputs/_scan_rest_1/eigenvector_centrality_weighted.nii.gz",
      "/path/sub002_site1/alff_to_standard_smooth/_scan_rest_1/file.nii.gz"
    ]

    output_folder = "/path"

    # remove _site1 and replace with nothing
    replacements = ["_site1,"]

    # output dictionary should have dictionaries as values, which have tuples 
    # as keys, where the tuple identifies the same file across different CPAC
    # versions (and thus potentially different filepaths)
    #   multiple dictionary levels to make it easy to pull up all of the
    #   entries for one particular derivative
    ref_output = {
      'alff_to_standard_smooth':
        {('alff_to_standard_smooth', 
          '/sub002/alff_to_standard_smooth/_scan_rest_1/', '1'):
            ['/path/sub002/alff_to_standard_smooth/_scan_rest_1/file.nii.gz']},
      'centrality_outputs: degree': 
        {('centrality_outputs: degree', 
          '/sub001/centrality_outputs/_scan_rest_1/', '1'): 
            ['/path/sub001/centrality_outputs/_scan_rest_1/degree_centrality_weighted.nii.gz']},
      'centrality_outputs: eigenvector': 
        {('centrality_outputs: eigenvector', 
          '/sub001/centrality_outputs/_scan_rest_1/', '1'):
            ['/path/sub001/centrality_outputs/_scan_rest_1/eigenvector_centrality_weighted.nii.gz']}
    }

    file_dict = create_unique_file_dict(filepaths, output_folder, replacements)

    assert ref_output == file_dict


def test_match_filepaths():

    try:
        from cpac_correlations_wf import match_filepaths
    except ModuleNotFoundError:
        from .cpac_correlations_wf import match_filepaths

    old_files_dict = {
      'alff_to_standard_smooth':
        {('alff_to_standard_smooth', 
          '/sub002/alff_to_standard_smooth/_scan_rest_1/', '1'):
            ['/old_run/sub002/alff_to_standard_smooth/_scan_rest_1/file.nii.gz']},
      'centrality_outputs: degree': 
        {('centrality_outputs: degree', 
          '/sub001/centrality_outputs/_scan_rest_1/', '1'): 
            ['/old_run/sub001/centrality_outputs/_scan_rest_1/degree_centrality_weighted.nii.gz']},
      'centrality_outputs: eigenvector': 
        {('centrality_outputs: eigenvector', 
          '/sub001/centrality_outputs/_scan_rest_1/', '1'):
            ['/old_run/sub001/centrality_outputs/_scan_rest_1/eigenvector_centrality_weighted.nii.gz']}
    }

    new_files_dict = {
      'alff_to_standard_smooth':
        {('alff_to_standard_smooth', 
          '/sub002/alff_to_standard_smooth/_scan_rest_1/', '1'):
            ['/new_run/sub002/alff_to_standard_smooth/_scan_rest_1/file.nii.gz']},
      'centrality_outputs: degree': 
        {('centrality_outputs: degree', 
          '/sub001/centrality_outputs/_scan_rest_1/', '1'): 
            ['/new_run/sub001/centrality_outputs/_scan_rest_1/degree_centrality_weighted.nii.gz']},
      'centrality_outputs: eigenvector': 
        {('centrality_outputs: eigenvector', 
          '/sub001/centrality_outputs/_scan_rest_1/', '1'):
            ['/new_run/sub001/centrality_outputs/_scan_rest_1/eigenvector_centrality_weighted.nii.gz']}
    }

    # the output should be similar to the inputs, except the two input
    # dictionaries have been merged
    ref_output_dict = {
      'alff_to_standard_smooth': 
        {('alff_to_standard_smooth',
          '/sub002/alff_to_standard_smooth/_scan_rest_1/', '1'): 
            ['/old_run/sub002/alff_to_standard_smooth/_scan_rest_1/file.nii.gz',
             '/new_run/sub002/alff_to_standard_smooth/_scan_rest_1/file.nii.gz']},
      'centrality_outputs: degree': 
        {('centrality_outputs: degree',
          '/sub001/centrality_outputs/_scan_rest_1/', '1'): 
            ['/old_run/sub001/centrality_outputs/_scan_rest_1/degree_centrality_weighted.nii.gz',
             '/new_run/sub001/centrality_outputs/_scan_rest_1/degree_centrality_weighted.nii.gz']},
      'centrality_outputs: eigenvector': 
        {('centrality_outputs: eigenvector',
          '/sub001/centrality_outputs/_scan_rest_1/', '1'): 
            ['/old_run/sub001/centrality_outputs/_scan_rest_1/eigenvector_centrality_weighted.nii.gz',
             '/new_run/sub001/centrality_outputs/_scan_rest_1/eigenvector_centrality_weighted.nii.gz']}
    }

    output_dict = match_filepaths(old_files_dict, new_files_dict)

    assert ref_output_dict == output_dict


def test_calculate_correlation_no_s3():

    pass


def test_aggregate_correlations():

    correlation_info_list = \
        [("anatomical_brain", 1.0, 1.0), ("anatomical_brain", 0.95, 0.89), \
         ("anatomical_brain", 0.67,0.50), ("alff_img", 0.98, 0.96), \
         ("alff_img", 0.82, 0.80)]

    ref_pearson_dict = \
        {"anatomical_brain": [1.0, 0.95, 0.67], "alff_img": [0.98, 0.82]}
    ref_concor_dict = \
        {"anatomical_brain": [1.0, 0.89, 0.50], "alff_img": [0.96, 0.80]}

    pearson_dict, concor_dict = aggregate_correlations(correlation_info_list)

    assert ref_pearson_dict == pearson_dict
    assert ref_concor_dict == concor_dict
