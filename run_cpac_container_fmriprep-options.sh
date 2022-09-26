#!/bin/bash

# usage
#   > ./run_cpac_container.sh {docker tag} {run label} {mode}
#                                                        /\ optional

# {mode} options:
#     (leave this blank to simply run C-PAC)
#     - enter         = enter the container instead of running C-PAC
#     - current       = use C-PAC install from code in current branch of C-PAC repo listed in "repo"
#     - enter-current = enter the container instead of running, with C-PAC install from code
#                       in current branch of C-PAC repo listed in "repo"

docker_image=$1
name=$2
mode=$3

if [[ -z "$name" ]]
then
    name="test"
fi

# Custom args for this run
#-------------------------
# Paths
run_name="${name}_fmriprep-options"
repo="/media/ebs/C-PAC"

# Data
data_config="/media/ebs/CPAC_regtest_pack/data_config_regtest_quick_incomplete.yml"

bids_dir=/home/ubuntu # keep as /home/ubuntu when providing a data_config
#bids_dir="s3://fcp-indi/data/etc."

# Pipeline
pipe_config="/media/ebs/runs/configs/pipe_fmriprep-opts_antsmult.yml"
#preconfig="fmriprep-options" # preconfig will override pipe_config


# Run settings
cpu_max=16
n_cpus=16
ants_cpus=10
mem_gb=20
#-------------------------

if [[ -z "$data_config" ]]
then
    data_map="-v $bids_dir:$bids_dir"
    data_config=""
else
    data_map="-v $data_config:/configs/data_config.yml"
    data_config="--data_config_file /configs/data_config.yml"
fi

if [[ -z "$pipe_config" ]]
then
    pipe_map="-v /tmp:/tmp"
    pipe_config=""
else
    pipe_map="-v $pipe_config:/configs/pipe_config.yml"
    pipe_config="--pipeline_file /configs/pipe_config.yml"
fi

if [[ "$preconfig" ]]
then
    pipe_config="--preconfig $preconfig"
fi
    

if [[ $mode = "enter" ]]
then
    sudo docker run -it \
        -v /home/ubuntu:/home/ubuntu \
        -v /media/ebs/CPAC_regtest_pack:/media/ebs/CPAC_regtest_pack \
        -v /media/ebs/runs/$run_name:/output \
        --entrypoint bash \
        $docker_image
elif [[ $mode = "enter-current" ]]
then
    sudo docker run -it \
        -v $repo/CPAC:/code/CPAC \
        -v $repo/dev/docker_data/run.py:/code/run.py \
        -v $repo/dev/docker_data:/cpac_resources \
        -v $repo/dev/docker_data/bids_utils.py:/code/bids_utils.py \
        -v $repo/dev/docker_data/default_pipeline.yml:/code/default_pipeline.yml \
        -v /home/ubuntu:/home/ubuntu \
        -v /media/ebs/CPAC_regtest_pack:/media/ebs/CPAC_regtest_pack \
        -v /media/ebs/runs/$run_name:/output \
        --entrypoint bash \
        $docker_image
elif [[ $mode = "current" ]]
then
    sudo docker run \
        -v $repo/CPAC:/code/CPAC \
        -v $repo/dev/docker_data/run.py:/code/run.py \
        -v $repo/dev/docker_data:/cpac_resources \
        -v $repo/dev/docker_data/bids_utils.py:/code/bids_utils.py \
        -v $repo/dev/docker_data/default_pipeline.yml:/code/default_pipeline.yml \
        -v /home/ubuntu:/home/ubuntu \
        -v /media/ebs/CPAC_regtest_pack:/media/ebs/CPAC_regtest_pack \
        -v /media/ebs/runs/$run_name:/output \
        $data_map \
        $pipe_map \
        $docker_image $bids_dir /output participant \
        --save_working_dir \
        --skip_bids_validator \
        --n_cpus $cpu_max \
        --mem_gb $mem_gb \
        $data_config \
        $pipe_config
else
    sudo docker run \
        -v /home/ubuntu:/home/ubuntu \
        -v /media/ebs/CPAC_regtest_pack:/media/ebs/CPAC_regtest_pack \
        -v /media/ebs/runs/$run_name:/output \
        $data_map \
        $pipe_map \
        $docker_image $bids_dir /output participant \
        --save_working_dir \
        --skip_bids_validator \
        --n_cpus $cpu_max \
        --mem_gb $mem_gb \
        $data_config \
        $pipe_config 
fi
