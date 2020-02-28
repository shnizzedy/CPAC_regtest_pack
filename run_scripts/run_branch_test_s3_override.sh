#!/bin/bash

# inputs:
# - C-PAC branch name
# - pipe config
# - data config

# latest run (for reference):
#     ./run_branch_test_s3_override.sh feature/despike s3://fcp-indi/data/Projects/ADHD200/RawDataBIDS/NYU 'runDespike: True' despike

cpac_repo='/media/ebs/C-PAC'

cpac_branch=$1
s3_link=$2
override=$3
run_name=$4

localbuild="cpac/localbuild_"
tagname=$localbuild$run_name
echo "Tag name:"
echo $tagname

cd $cpac_repo
git pull
git checkout $cpac_branch
sudo docker build -t $tagname .
cd ..
mkdir "test_$run_name"
cd "test_$run_name"

docker run -v $data_config:/configs/data_config.yml -v $pipe_config:/configs/pipe_config.yml -v $PWD:/run_dir $tagname $s3_link /run_dir participant --participant_ndx 1 --pipeline_override '$override'
