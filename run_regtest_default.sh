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

docker_image=$1
run_name=$2
enter=$3

if [ $3 = "enter" ]
then
    sudo docker run -it \
        -v /home/ubuntu:/home/ubuntu \
        -v /media/ebs/CPAC_regtest_pack:/media/ebs/CPAC_regtest_pack \
        -v /media/ebs/runs/$run_name\_default-pipeline:/output \
        --entrypoint bash \
        $docker_image
else
    sudo docker run \
        -v /home/ubuntu:/home/ubuntu \
        -v /media/ebs/CPAC_regtest_pack:/media/ebs/CPAC_regtest_pack \
        -v /media/ebs/runs/$run_name\_default-pipeline:/output \
        $docker_image /home/ubuntu /output participant \
        --save_working_dir \
        --data_config_file /media/ebs/CPAC_regtest_pack/cpac_data_config_regtest.yml \
        --n_cpus 32 \
        --mem_gb 12 \
        --pipeline_override "num_ants_threads: 16" \
        --pipeline_override "numParticipantsAtOnce: 1"
fi
