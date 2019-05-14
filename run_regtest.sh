#!/bin/bash

# input argument: tag of the Docker container

# for a c4.8xlarge
#   36 cpus
#   60 GB mem

sudo docker run -v /home/ubuntu:/home/ubuntu -v /home/ubuntu/CPAC_regtest_pack:/home/ubuntu/CPAC_regtest_pack -v /media/ebs/ants:/output -v /media/ebs/ants/work:/tmp $1 /home/ubuntu /output participant  --data_config_file /home/ubuntu/CPAC_regtest_pack/data_config_regtest.yml --pipeline_file /home/ubuntu/CPAC_regtest_pack/regtest_pipeline_ants.yaml --n_cpus 2 --pipeline_override "numParticipantsAtOnce: 18" --save_working_dir

sudo docker run -v /home/ubuntu:/home/ubuntu -v /home/ubuntu/CPAC_regtest_pack:/home/ubuntu/CPAC_regtest_pack -v /media/ebs/fnirt:/output -v /media/ebs/fnirt/work:/tmp $1 /home/ubuntu /output participant  --data_config_file /home/ubuntu/CPAC_regtest_pack/data_config_regtest.yml --pipeline_file /home/ubuntu/CPAC_regtest_pack/regtest_pipeline_fnirt.yaml --n_cpus 2 --pipeline_override "numParticipantsAtOnce: 18" --save_working_dir

sudo docker run -v /home/ubuntu:/home/ubuntu -v /home/ubuntu/CPAC_regtest_pack:/home/ubuntu/CPAC_regtest_pack -v /media/ebs/ants-spike:/output -v /media/ebs/ants-spike/work:/tmp $1 /home/ubuntu /output participant  --data_config_file /home/ubuntu/CPAC_regtest_pack/data_config_regtest.yml --pipeline_file /home/ubuntu/CPAC_regtest_pack/regtest_pipeline_ants-spike.yaml --n_cpus 2 --pipeline_override "numParticipantsAtOnce: 18" --save_working_dir