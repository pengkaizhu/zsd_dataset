import os
import xml.etree.ElementTree as ET
from os import getcwd

"""
generate the dataset and labels of VOC for ZS-YOLO.
"""


sets = [('2012', 'train'), ('2012', 'val'), ('2007', 'train'),
        ('2007', 'val'), ('2007', 'test')]

classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus",
           "car", "cat", "chair", "cow", "diningtable", "dog",
           "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]


def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    # (x, y) center of the bounding box
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    # (w, h) width and height
    w = box[1] - box[0]
    h = box[3] - box[2]
    # relative value
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def convert_annotation(year, image_id):
    with open('VOCdevkit/VOC{:s}/Annotations/{:s}.xml'.format(year, image_id)) as in_file:
        tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    with open('VOCdevkit/VOC{:s}/labels/{:s}.txt'.format(year, image_id), 'w') as out_file:
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
                 float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bb = convert((w, h), b)
            out_file.write(str(cls_id) + ' ' + ' '.join([str(a) for a in bb]) + '\n')


wd = getcwd()

if __name__ == '__main__':
    for year, image_set in sets:
        if not os.path.exists('VOCdevkit/VOC{:s}'.format(year)):
            continue
        if not os.path.exists('VOCdevkit/VOC{:s}/labels/'.format(year)):
            os.makedirs('VOCdevkit/VOC{:s}/labels/'.format(year))
        image_ids = open('VOCdevkit/VOC{:s}/ImageSets/Main/{:s}.txt'.format(year, image_set)).read().strip().split()
        with open('{:s}_{:s}.txt'.format(year, image_set), 'w') as list_file:
            for image_id in image_ids:
                list_file.write('{:s}/VOCdevkit/VOC{:s}/JPEGImages/{:s}.jpg\n'.format(wd, year, image_id))
                convert_annotation(year, image_id)
