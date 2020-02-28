#!/bin/bash

sudo docker run -ti --rm \
    -v /media/ebs/v162/lei-xcp/working/fcp-indi/data/Projects/CORR/RawDataBIDS/HNU_1:/data \
    -v /media/ebs/fmriprep_out:/output \
    poldracklab/fmriprep:latest \
    /data /output participant
