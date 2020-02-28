#!/bin/bash

# usage
#   > ./run_cpac_default.sh {docker tag} {S3 link} {run name} {num cpus} {mem GB}

# example
#     ./run_cpac_default.sh fcpindi/c-pac:nightly s3://fcp-indi/data/Projects/ABIDE/RawDataBIDS/NYU default-abide-nyu 25

sudo docker run -v /home/ubuntu:/home/ubuntu -v /media/ebs/CPAC_regtest_pack:/media/ebs/CPAC_regtest_pack -v /media/ebs/runs/$3:/output $1 $2 /output participant --n_cpus $4 --mem_gb $5 --save_working_dir --pipeline_override "ndmg_mode: [1]"
