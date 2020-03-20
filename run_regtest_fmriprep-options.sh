#!/bin/bash

# usage
#   > ./run_regtest.sh {docker tag} {version name}

# for a c4.8xlarge
#   36 cpus
#   60 GB mem

# cpus/mem lower, meant to run two of these at the same time, set it and forget it


docker_image=$1
run_name=$2
enter=$3

if [ $3 = "enter" ]
then
    sudo docker run -it \
        -v /home/ubuntu:/home/ubuntu \
        -v /media/ebs/CPAC_regtest_pack:/media/ebs/CPAC_regtest_pack \
        -v /media/ebs/runs/$run_name\_fmriprep-opts:/output \
        --entrypoint bash \
        $docker_image
else
    sudo docker run \
        -v /home/ubuntu:/home/ubuntu \
        -v /media/ebs/CPAC_regtest_pack:/media/ebs/CPAC_regtest_pack \
        -v /media/ebs/runs/$run_name\_fmriprep-opts:/output \
        $docker_image /home/ubuntu /output participant \
        --save_working_dir \
        --data_config_file /media/ebs/CPAC_regtest_pack/cpac_data_config_regtest.yml \
        --preconfig fmriprep-options \
        --n_cpus 4 \
        --mem_gb 12 \
        --pipeline_override "numParticipantsAtOnce: 4"
fi
