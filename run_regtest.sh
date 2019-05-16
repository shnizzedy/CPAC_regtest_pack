#!/bin/bash

# usage
#   > ./run_regtest.sh {docker tag} {version name}

# for a c4.8xlarge
#   36 cpus
#   60 GB mem

# sanity check on default pipeline, run just one participant from an S3 bucket
sudo docker run -v /home/ubuntu:/home/ubuntu -v /home/ubuntu/CPAC_regtest_pack:/home/ubuntu/CPAC_regtest_pack -v /media/ebs/$2/default:/output -v /media/ebs/$2/default/work:/tmp $1 s3://fcp-indi/data/Projects/ADHD200/RawDataBIDS/KKI /output participant --n_cpus 20 --participant_ndx 1 --save_working_dir

sudo docker run -v /home/ubuntu:/home/ubuntu -v /home/ubuntu/CPAC_regtest_pack:/home/ubuntu/CPAC_regtest_pack -v /media/ebs/$2/ants:/output -v /media/ebs/$2/ants/work:/tmp $1 /home/ubuntu /output participant  --data_config_file /home/ubuntu/CPAC_regtest_pack/data_config_regtest.yml --pipeline_file /home/ubuntu/CPAC_regtest_pack/regtest_pipeline_ants.yaml --n_cpus 2 --pipeline_override "numParticipantsAtOnce: 18" --save_working_dir

sudo docker run -v /home/ubuntu:/home/ubuntu -v /home/ubuntu/CPAC_regtest_pack:/home/ubuntu/CPAC_regtest_pack -v /media/ebs/$2/fnirt:/output -v /media/ebs/$2/fnirt/work:/tmp $1 /home/ubuntu /output participant  --data_config_file /home/ubuntu/CPAC_regtest_pack/data_config_regtest.yml --pipeline_file /home/ubuntu/CPAC_regtest_pack/regtest_pipeline_fnirt.yaml --n_cpus 2 --pipeline_override "numParticipantsAtOnce: 18" --save_working_dir

sudo docker run -v /home/ubuntu:/home/ubuntu -v /home/ubuntu/CPAC_regtest_pack:/home/ubuntu/CPAC_regtest_pack -v /media/ebs/$2/ants-spike:/output -v /media/ebs/$2/ants-spike/work:/tmp $1 /home/ubuntu /output participant  --data_config_file /home/ubuntu/CPAC_regtest_pack/data_config_regtest.yml --pipeline_file /home/ubuntu/CPAC_regtest_pack/regtest_pipeline_ants-spike.yaml --n_cpus 2 --pipeline_override "numParticipantsAtOnce: 18" --save_working_dir
