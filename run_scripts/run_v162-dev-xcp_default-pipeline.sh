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
    -v /home/ubuntu:/home/ubuntu \
    -v /media/ebs/CPAC_regtest_pack:/media/ebs/CPAC_regtest_pack \
    -v /media/ebs/v162/dev-v162-xcp/default-pipeline:/output \
    fcpindi/c-pac:dev-v1.6.2-xcp s3://fcp-indi/data/Projects/CORR/RawDataBIDS/HNU_1 /output participant \
    --save_working_dir \
    --n_cpus 2 \
    --mem_gb 15 \
    --data_config_file /media/ebs/CPAC_regtest_pack/data_config_HNU30_ses1.yml \
    --preconfig preproc \
    --pipeline_override "numParticipantsAtOnce: 5"
