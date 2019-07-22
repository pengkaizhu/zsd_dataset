# Zero Shot Detection Dataset
This repository contains the datasets used in [Zero Shot Detection](https://arxiv.org/pdf/1803.07113.pdf) by
[Pengkai Zhu](https://github.com/pengkaizhu), [Hanxiao Wang](https://github.com/STARrapier), [Tolga Bolukbasi](https://github.com/tolga-b) and Venkatesh Saligrama.
```
@article{Zhu_2019,
   title={Zero Shot Detection},
   DOI={10.1109/tcsvt.2019.2899569},
   journal={IEEE Transactions on Circuits and Systems for Video Technology},
   publisher={Institute of Electrical and Electronics Engineers (IEEE)},
   author={Zhu, Pengkai and Wang, Hanxiao and Saligrama, Venkatesh},
   year={2019}
}
```


## Seen/Unseen Split

The scripts can download [Pascal VOC](http://host.robots.ox.ac.uk/pascal/VOC/) or [MSCOCO](http://cocodataset.org/#home)
and split it into four parts as in the paper:
- **Train**: seen in train
- **Test-Seen**: seen in val/test
- **Test-Unseen**: unseen in train&val&test
- **Test-Mix**: both seen & unseen in val/test

The dataset is split based on assigned seen categories names. We provide
the splits we used in the paper in `seen_names` subfolder.

## Attributes

The attributes for Pascal VOC will be downloaded and extracted automatically
when running `get_voc_zsd_dataset.sh`. We also provide the attributes we use
in the paper in the `attributes` subfolder:
- `coco_w2v.txt`: w2v attributes for coco categories
- `coco_w2v_voc.txt`: projected w2v attributes for coco categories (mirroring VOC attributes similarity)
- `voc.txt`: labelled attributes (from [aP&Y](http://vision.cs.uiuc.edu/attributes/)) for VOC categories
- `voc_w2v.txt`: w2v attributes for VOC categories

## How to use
- Preliminary: `numpy`
#### Setup Pascal VOC:
```bash
bash get_voc_zsd_dataset.sh $zsd-data-dir  # $zsd-data-dir: directory for saving pascal ZSD dataset
```
The dataset will be downloaded to `$zsd-data-dir` and the split sets will be saved
in `1010split` subfolder by default. If you already downloaded the dataset or would like
to try some other splits, just run:
```bash
python zsd_split.py --dataset voc --data_dir $zsd-data-dir --name_file voc.names \
--seen_name_file seen_names/voc/${choose another split} \
--save_dir ${split save name} \
```

#### Setup MSCOCO
```bash
bash get_coco_zsd_dataset.sh $zsd-data-dir  # $zsd-data-dir: directory for saving coco ZSD dataset
```

