#!/usr/bin/evn bash

##############################################
# This script will download the Pascal VOC dataset, generate
# labels and split into seen, unseen and test datasets.
#
# Usage (in the project dir):
# bash get_voc_zsd_dataset.sh <zsd-data-dir>
# <zsd-data-dir>: the directory to save VOC ZSD dataset
#
##############################################

if [ $# -eq 1 ]
then
    PROJECTSDIR=$PWD
    cp voc_label.py ext_att.py $1
    cd $1
    wget -c http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar
    wget -c http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar
    wget -c http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar
    tar xf VOCtrainval_11-May-2012.tar
    tar xf VOCtrainval_06-Nov-2007.tar
    tar xf VOCtest_06-Nov-2007.tar
    rm VOCtrainval_11-May-2012.tar
    rm VOCtrainval_06-Nov-2007.tar
    rm VOCtest_06-Nov-2007.tar
    python voc_label.py
    rm voc_label.py
    rm 2007* 2012*
    wget http://vision.cs.uiuc.edu/attributes/attribute_data.tar.gz
    tar xzf attribute_data.tar.gz
    rm attribute_data.tar.gz
    python ext_att.py
    rm ext_att.py
    cd $PROJECTDIR
    python zsd_split.py --dataset voc --data_dir $1 --name_file voc.names \
    --seen_name_file seen_names/voc/1010split.names --save_dir 1010split
else
    echo "Wrong argument numbers"
    echo "Usage (in the project dir): bash get_voc_zsd_dataset.sh <zsd-data-dir>"
fi