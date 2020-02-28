#!/bin/bash

# usage
#   > ./run_regtest.sh {docker tag} {version name}

# for a c4.8xlarge
#   36 cpus
#   60 GB mem

# cpus/mem lower, meant to run two of these at the same time, set it and forget it

# WARNING
# incomplete = NO coverage of distortion correction, spike regression, and many other options etc.!
# this is meant entirely to get very quick numbers of the big basics
# this is NOT a full regression test meant for release validation

repo='/media/ebs/C-PAC'

sudo docker run \
    -v $repo/CPAC:/code/CPAC \
    -v $repo/dev/docker_data/run.py:/code/run.py \
    -v $repo/dev/docker_data:/cpac_resources \
    -v $repo/dev/docker_data/bids_utils.py:/code/bids_utils.py \
    -v $repo/dev/docker_data/default_pipeline.yml:/code/default_pipeline.yml \
    -v /home/ubuntu:/home/ubuntu \
    -v /media/ebs/CPAC_regtest_pack:/media/ebs/CPAC_regtest_pack \
    -v /media/ebs/runs/$2/default-pipeline:/output \
    $1 s3://fcp-indi/data/Projects/CORR/RawDataBIDS/HNU_1 /output participant \
    --save_working_dir \
    --n_cpus 6 \
    --mem_gb 12 \
    --pipeline_override "regOption: ['FSL']" \
    --pipeline_override "write_func_outputs: [1]" \
    --pipeline_override "write_debugging_outputs: [1]" \
    --pipeline_override "runSCA: [0]" \
    --participant_ndx 1
