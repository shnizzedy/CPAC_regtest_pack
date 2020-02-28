#!/bin/bash

# inputs:
# - C-PAC branch name
# - pipe config
# - data config

cpac_repo='/media/ebs/C-PAC'

cpac_branch=$1
data_config=$2
override=$3

cd $cpac_repo
git pull
git checkout $cpac_branch
docker build -t 'localbuild_$cpac_branch' . --no-cache
cd ..
mkdir 'test_branch'
cd 'test_branch'

docker run -v $data_config:/configs/data_config.yml -v $pipe_config:/configs/pipe_config.yml -v $PWD:/run_dir 'localbuild_$cpac_branch' /run_dir participant --data_config_file /configs/data_config.yml --pipeline_file /configs/pipeline_config.yml
