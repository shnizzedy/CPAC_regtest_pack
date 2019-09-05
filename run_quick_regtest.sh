#!/bin/bash

# usage
#   > ./run_quick_regtest.sh {docker tag} {version name}

# for a c4.8xlarge
#   36 cpus
#   60 GB mem

sudo docker run -v /home/ubuntu:/home/ubuntu -v /home/ubuntu/CPAC_regtest_pack:/home/ubuntu/CPAC_regtest_pack -v /media/ebs/$2/ants-quick:/output -v /media/ebs/$2/ants-quick/work:/tmp $1 /home/ubuntu /output participant  --data_config_file /home/ubuntu/CPAC_regtest_pack/data_config_regtest_quick.yml --pipeline_file /home/ubuntu/CPAC_regtest_pack/configs/$2/regtest_pipeline_ants.yml --n_cpus 7 --pipeline_override "numParticipantsAtOnce: 5" --save_working_dir
