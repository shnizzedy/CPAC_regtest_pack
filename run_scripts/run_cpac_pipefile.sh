#!/bin/bash

# usage
#   > ./run_regtest.sh {docker tag} {run name} {data config path} {pipeline file path} {num cpus}

sudo docker run -v /home/ubuntu:/home/ubuntu -v /media/ebs/CPAC_regtest_pack:/media/ebs/CPAC_regtest_pack -v /media/ebs/$2:/output -v $3:/media/ebs/data_config.yml -v $4:/media/ebs/pipeline_file.yml $1 /home/ubuntu /output participant --data_config_file /media/ebs/data_config.yml --pipeline_file /media/ebs/pipeline_file.yml --n_cpus $5 --save_working_dir
