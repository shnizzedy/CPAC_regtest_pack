#!/bin/bash

# usage
#   > ./run_cpac_container.sh {docker tag} {name} {data} {pipeline} {participant_ndx} {mode}
#                                                                                       /\ optional

# {mode} options:
#     (leave this blank to simply run C-PAC)
#     - enter         = enter the container instead of running C-PAC
#     - current       = use C-PAC install from code in current branch of C-PAC repo listed in "repo"
#     - enter-current = enter the container instead of running, with C-PAC install from code
#                       in current branch of C-PAC repo listed in "repo"
#     - pre-182       = don't use '--num_ants_threads'
#     - pre-182-current

docker_image=$1
run_name=$2
data=$3
pipe=$4
aux=$5
mode=$6

# Custom args for this run
#-------------------------
# Paths
repo="/media/ebs/C-PAC"

# Run settings
n_cpus=30
ants_cpus=15
mem_gb=45

# Automated args
#-------------------------
# Data
if [[ "${data}" == *".yml" || "${data}" == *".yaml" ]]
then
    data_config="${data}"
    bids_dir=/home/ubuntu # keep as /home/ubuntu when providing a data_config
else
    bids_dir="${data}"
fi

if [[ "${pipe}" == "default" ]]
then
    pipe_config=""
    preconfig=""
elif [[ "${pipe}" == *".yml" || "${pipe}" == *".yaml" ]]
then
    pipe_config="${pipe}"
    pipe_name=""
else
    # a preconfig name was given instead - this will be appended to {name}
    preconfig="${pipe}"
    pipe_name="_${pipe}"
fi

# Pipeline
run_name="${run_name}${pipe_name}"
#-------------------------

if [[ -z "$data_config" ]]
then
    data_map="-v /tmp:/tmp"
    data_config=""
else
    data_map="-v $data_config:/configs/data_config.yml"
    data_config="--data_config_file /configs/data_config.yml"
fi

if [[ -z "$bids_dir" ]]
then
    bids_map="-v /tmp:/tmp"
    bids_dir="/home/ubuntu"
else
    bids_map="-v $bids_dir:$bids_dir"
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

configs="${data_config} ${pipe_config}"

if [[ $mode != "pre-182" && $mode != "pre-182-current" ]]
then
    configs="${configs} --num_ants_threads ${ants_cpus}"
fi

if [[ -n $aux && $aux != "all" ]]
then
    configs="${configs} --participant_ndx ${aux}"
fi

if [[ $mode = "enter" ]]
then
    sudo docker run -it \
        -v /home/ubuntu:/home/ubuntu \
        -v /media/ebs:/media/ebs \
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
        -v /home/ubuntu:/home/ubuntu \
	-v /media/ebs:/media/ebs \
        -v /media/ebs/CPAC_regtest_pack:/media/ebs/CPAC_regtest_pack \
        -v /media/ebs/runs/$run_name:/output \
	$bids_map \
	$data_map \
	$pipe_map \
        --entrypoint bash \
        $docker_image
elif [[ $mode = "current" ]]
then
    sudo docker run \
        -v $repo/CPAC:/code/CPAC \
        -v $repo/dev/docker_data/run.py:/code/run.py \
        -v $repo/dev/docker_data:/cpac_resources \
        -v /home/ubuntu:/home/ubuntu \
	-v /media/ebs:/media/ebs \
        -v /media/ebs/CPAC_regtest_pack:/media/ebs/CPAC_regtest_pack \
        -v /media/ebs/runs/$run_name:/output \
	$bids_map \
        $data_map \
        $pipe_map \
	$docker_image $bids_dir /output participant \
        --save_working_dir \
        --skip_bids_validator \
        --n_cpus $n_cpus \
        --mem_gb $mem_gb \
	$configs
else
    sudo docker run \
        -v /home/ubuntu:/home/ubuntu \
	-v /media/ebs:/media/ebs \
        -v /media/ebs/CPAC_regtest_pack:/media/ebs/CPAC_regtest_pack \
        -v /media/ebs/runs/$run_name:/output \
	$bids_map \
        $data_map \
        $pipe_map \
        $docker_image $bids_dir /output participant \
        --save_working_dir \
        --skip_bids_validator \
        --n_cpus $n_cpus \
        --mem_gb $mem_gb \
	$configs
fi
