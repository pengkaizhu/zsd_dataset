import numpy as np

"""
aP&Y attributes extraction.
"""


classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus",
           "car", "cat", "chair", "cow", "diningtable", "dog",
           "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]
num_class = len(classes)
num_attrs = 64
attrs = {}
for cls in classes:
    attrs[cls] = []

attr_files = ['apascal_train.txt', 'apascal_test.txt']
for attr_file in attr_files:
    with open('attribute_data/{:s}'.format(attr_file)) as file:
        for each_line in file:
            tmp = each_line.strip().split()
            attrs[tmp[1]].append(tmp[6:])

attr_array = np.zeros((num_class, num_attrs))
for i in range(len(classes)):
    attr_array[i] = np.array(attrs[classes[i]]).astype(np.float).mean(axis=0)

np.savetxt('attributes.txt', attr_array)
