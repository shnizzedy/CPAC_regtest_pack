#!/bin/bash

# usage
#   > ./run_regtest.sh {docker tag} {version name}

# for a c4.8xlarge
#   36 cpus
#   60 GB mem

# cpus/mem lower, meant to run two of these at the same time, set it and forget it

repo='/media/ebs/C-PAC'

sudo docker run \
    -v /home/ubuntu:/home/ubuntu \
    -v /media/ebs/CPAC_regtest_pack:/media/ebs/CPAC_regtest_pack \
    -v /media/ebs/$2/ndmg:/output \
    $1 /home/ubuntu /output participant \
    --save_working_dir \
    --data_config_file /media/ebs/CPAC_regtest_pack/data_config_regtest_quick_incomplete.yml \
    --preconfig ndmg \
    --n_cpus 4 \
    --mem_gb 12 \
    --pipeline_override "numParticipantsAtOnce: 4"
