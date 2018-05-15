#!/bin/bash

##############################################
# This script will download the coco dataset, generate
# labels and split into seen, unseen and test datasets.
#
# Usage (in the project dir):
# bash get_coco_zsd_dataset.sh <zsd-data-dir>
# <zsd-data-dir>: the directory to save coco ZSD dataset
#
##############################################

if [ $# -eq 1 ]
then
    PROJECTSDIR=$PWD
    cd $1

    # Clone COCO API
    git clone https://github.com/pdollar/coco
    cd coco

    mkdir images
    cd images

    # Download Images
    wget -c http://images.cocodataset.org/zips/train2014.zip
    wget -c http://images.cocodataset.org/zips/val2014.zip

    # Unzip
    unzip -q train2014.zip
    unzip -q val2014.zip

    cd ..

    # Download COCO Metadata
    wget -c http://images.cocodataset.org/annotations/annotations_trainval2014.zip
    wget -c https://pjreddie.com/media/files/coco/5k.part
    wget -c https://pjreddie.com/media/files/coco/trainvalno5k.part
    wget -c https://pjreddie.com/media/files/coco/labels.tgz
    tar xzf labels.tgz
    unzip -q annotations_trainval2014.zip

    # Set Up Image Lists
    paste <(awk "{print \"$PWD\"}" <5k.part) 5k.part | tr -d '\t' > 5k.txt
    paste <(awk "{print \"$PWD\"}" <trainvalno5k.part) trainvalno5k.part | tr -d '\t' > trainvalno5k.txt

    cd $PROJECTSDIR
    python zsd_split.py --dataset coco --data_dir $1/coco --name_file coco.names \
    --seen_name_file seen_names/coco/20seen.names --save_dir 20seen
else

    echo "Wrong argument numbers"
    echo "Usage (in the project dir): bash get_coco_zsd_dataset.sh <zsd-data-dir>"
fi