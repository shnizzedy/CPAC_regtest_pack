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
docker_image=$1
run_name=$2
enter=$3

if [ $enter = "enter" ]
then
    sudo docker run -it \
        -v $repo/CPAC:/code/CPAC \
        -v $repo/dev/docker_data/run.py:/code/run.py \
        -v $repo/dev/docker_data:/cpac_resources \
        -v $repo/dev/docker_data/bids_utils.py:/code/bids_utils.py \
        -v $repo/dev/docker_data/default_pipeline.yml:/code/default_pipeline.yml \
        -v /home/ubuntu:/home/ubuntu \
        -v /media/ebs/CPAC_regtest_pack:/media/ebs/CPAC_regtest_pack \
        -v /media/ebs/runs/$run_name\_benchmark-FNIRT:/output \
        --entrypoint bash \
        $docker_image
else
    sudo docker run \
        -v $repo/CPAC:/code/CPAC \
        -v $repo/dev/docker_data/run.py:/code/run.py \
        -v $repo/dev/docker_data:/cpac_resources \
        -v $repo/dev/docker_data/bids_utils.py:/code/bids_utils.py \
        -v $repo/dev/docker_data/default_pipeline.yml:/code/default_pipeline.yml \
        -v /home/ubuntu:/home/ubuntu \
        -v /media/ebs/CPAC_regtest_pack:/media/ebs/CPAC_regtest_pack \
        -v /media/ebs/runs/$run_name\_benchmark-FNIRT:/output \
        $docker_image /home/ubuntu /output participant \
        --save_working_dir \
        --data_config_file /media/ebs/CPAC_regtest_pack/cpac_data_config_regtest_oldsubs.yml \
        --preconfig benchmark-FNIRT \
        --n_cpus 6 \
        --mem_gb 12 \
        --pipeline_override "numParticipantsAtOnce: 5" \
        --pipeline_override "runICA: [0]" \
        --pipeline_override "skullstrip_option: [FSL]" \
        --pipeline_override "runRegisterFuncToTemplate: ['T1_template', 'Off']"
fi
