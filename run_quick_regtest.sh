#!/bin/bash

# usage
#   > ./run_quick_regtest.sh {docker tag} {version name} {parent directory of "CPAC_regtest_pack"}

# for a c4.8xlarge
#   36 cpus
#   60 GB mem

DEFAULT_CPAC_HOME="/home/ubuntu"
CPAC_HOME=${3:-$DEFAULT_CPAC_HOME}

sudo docker run -v $CPAC_HOME:/home/ubuntu -v $CPAC_HOME/CPAC_regtest_pack:/home/ubuntu/CPAC_regtest_pack -v /media/ebs/$2/ants-quick:/output -v /media/ebs/$2/ants-quick/work:/tmp $1 $CPAC_HOME /output participant  --data_config_file $DEFAULT_CPAC_HOME/CPAC_regtest_pack/data_config_regtest_quick.yml --pipeline_file $DEFAULT_CPAC_HOME/CPAC_regtest_pack/configs/$2/regtest_pipeline_ants.yml --n_cpus 7 --pipeline_override "numParticipantsAtOnce: 5" --save_working_dir
