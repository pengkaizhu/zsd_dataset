import os

"""
Split the VOC/coco dataset into seen classes and unseen and
extract the corresponding images.

Please execute voc_label.py or get_coco_dataset.sh before executing this script.
"""


def load_class_names(names_file):
    class_names = []
    with open(names_file) as fp:
        for line in fp:
            line = line.rstrip()
            class_names.append(line)
    return class_names


def split_voc(data_dir, name_file, seen_name_file, save_dir_name):

    save_dir = os.path.join(data_dir, save_dir_name)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # for voc set setting
    all_sets = [(2007, 'trainval'), (2012, 'trainval'), (2007, 'test')]

    all_class = load_class_names(name_file)
    seen_class = load_class_names(seen_name_file)
    unseen_class = list(set(all_class) - set(seen_class))

    # split dataset
    all_train_list = []
    all_test_list = []
    seen_list = []
    unseen_train_list = []
    unseen_test_list = []
    img_year = {}

    for year, image_set in all_sets:
        with open('{:s}/VOCdevkit/VOC{:d}/ImageSets/Main/{:s}.txt'.format(
                data_dir, year, image_set)) as list_file:
            if image_set == 'test':
                for each_line in list_file:
                    all_test_list.append(each_line.strip())
                    img_year[each_line.strip()] = year
            else:
                for each_line in list_file:
                    all_train_list.append(each_line.strip())
                    img_year[each_line.strip()] = year
        for cls in unseen_class:
            with open('{:s}/VOCdevkit/VOC{:d}/ImageSets/Main/{:s}_{:s}.txt'.format(
                      data_dir, year, cls, image_set)) as unseen_list_file:
                for each_line in unseen_list_file:
                    image_cls = each_line.strip().split()
                    if image_cls[1] == '1':
                        if image_set == 'test':
                            unseen_test_list.append(image_cls[0])
                        else:
                            unseen_train_list.append(image_cls[0])
        for cls in seen_class:
            with open('{:s}/VOCdevkit/VOC{:d}/ImageSets/Main/{:s}_{:s}.txt'.format(
                    data_dir, year, cls, image_set)) as seen_list_file:
                for each_line in seen_list_file:
                    image_cls = each_line.strip().split()
                    if image_cls[1] == '1':
                        seen_list.append(image_cls[0])
    test_seen_img_list = list(set(all_test_list) - set(unseen_test_list))
    seen_img_list = list(set(all_train_list) - set(unseen_train_list))
    all_img_set = set(all_train_list).union(set(all_test_list))
    unseen_img_list = list(all_img_set - set(seen_list))
    mix_img_list = list(all_img_set - set(test_seen_img_list) - set(seen_img_list) -
                        set(unseen_img_list))
    seen_img_list.sort()
    test_seen_img_list.sort()
    unseen_img_list.sort()
    mix_img_list.sort()

    with open(os.path.join(save_dir, 'seen.txt'), 'w') as f:
        for image_id in seen_img_list:
            f.write('{:s}/VOCdevkit/VOC{:d}/JPEGImages/{:s}.jpg\n'.format(
                data_dir, img_year[image_id], image_id))
    with open(os.path.join(save_dir, 'test_seen.txt'), 'w') as f:
        for image_id in test_seen_img_list:
            f.write('{:s}/VOCdevkit/VOC{:d}/JPEGImages/{:s}.jpg\n'.format(
                data_dir, img_year[image_id], image_id))
    with open(os.path.join(save_dir, 'unseen.txt'), 'w') as f:
        for image_id in unseen_img_list:
            f.write('{:s}/VOCdevkit/VOC{:d}/JPEGImages/{:s}.jpg\n'.format(
                data_dir, img_year[image_id], image_id))
    with open(os.path.join(save_dir, 'mix.txt'), 'w') as f:
        for image_id in mix_img_list:
            f.write('{:s}/VOCdevkit/VOC{:d}/JPEGImages/{:s}.jpg\n'.format(
                data_dir, img_year[image_id], image_id))
    print('Dataset split done!')


def read_label_cls(label_file):
    classes = []
    with open(label_file) as f:
        for each_line in f:
            classes.append(int(each_line.strip().split(' ')[0]))
    return classes


def split_coco(data_dir, name_file, seen_name_file, save_dir_name):

    save_dir = os.path.join(data_dir, save_dir_name)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # for coco set setting
    file_lists = ['trainvalno5k.txt', '5k.txt'] # modify here if change file list

    # read class names
    all_class = load_class_names(name_file)
    seen_class = load_class_names(seen_name_file)

    # get seen and unseen class indices
    seen_idx = []
    unseen_idx = []
    for i in range(len(all_class)):
        if all_class[i] in seen_class:
            seen_idx.append(i)
        else:
            unseen_idx.append(i)
    seen_idx = set(seen_idx)
    unseen_idx = set(unseen_idx)

    # split dataset
    seen_img_list = []
    test_seen_img_list = []
    unseen_img_list = []
    mix_img_list = []
    for fi in file_lists:
        file = os.path.join(data_dir, fi)
        with open(file) as f:
            for each_img in f:
                each_label = each_img.strip().replace('images', 'labels').replace('.jpg', '.txt')
                try:
                    each_classes = set(read_label_cls(each_label))
                    if unseen_idx.intersection(each_classes) == set():
                        if fi == 'trainvalno5k.txt':
                            seen_img_list.append(each_img)
                        else:
                            test_seen_img_list.append(each_img)
                    elif seen_idx.intersection(each_classes) == set():
                        unseen_img_list.append(each_img)
                    else:
                        mix_img_list.append(each_img)
                except FileNotFoundError:
                    print('This label does not exists, skip it...')

    with open(os.path.join(data_dir, save_dir_name, 'seen.txt'), 'w') as f:
        for eachline in seen_img_list:
            f.write(eachline)
    with open(os.path.join(data_dir, save_dir_name, 'test_seen.txt'), 'w') as f:
        for eachline in test_seen_img_list:
            f.write(eachline)
    with open(os.path.join(data_dir, save_dir_name, 'unseen.txt'), 'w') as f:
        for eachline in unseen_img_list:
            f.write(eachline)
    with open(os.path.join(data_dir, save_dir_name, 'mix.txt'), 'w') as f:
        for eachline in mix_img_list:
            f.write(eachline)
    print('Dataset split done!')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True, help='dataset type: coco/voc')
    parser.add_argument('--data_dir', required=True, help='directory saving the dataset')
    parser.add_argument('--name_file', required=True,
                        help='file saving all classes names in the dataset')
    parser.add_argument('--seen_name_file', required=True,
                        help='file saving all seen classes for ZSD')
    parser.add_argument('--save_dir', required=True,
                        help='sub folder to save splitted dataset lists')
    a = parser.parse_args()

    if a.dataset == 'coco':
        split_coco(a.data_dir, a.name_file, a.seen_name_file, a.save_dir)
    elif a.dataset == 'voc':
        split_voc(a.data_dir, a.name_file, a.seen_name_file, a.save_dir)
    else:
        print('Wrong data set! Please choose coco/voc...Exiting...')
        exit(0)
