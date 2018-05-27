# -*- coding: utf-8 -*-
import os
import numpy as np
import json
import sys

'''
Script for finding the coordinates after image augmentation and generate new annotations json file in VIA format.
It should be guaranteed that a folder(argv[1]) with images after data augmentation and a json file(argv[2]) of the 
original images exist in the current folder.
Written by P.C.Zhang.
'''


def coord_fliph(_x, _y, w=1920):
    x = [w - i - 1 for i in _x]
    y = [j for j in _y]
    return x, y


def coord_flipv(_x, _y, h=1080):
    x = [i for i in _x]
    y = [h - j - 1 for j in _y]
    return x, y


def coord_noise(_x, _y):
    x = _x
    y = _y
    return x, y


def coord_rot(_x, _y, angle, w=1920, h=1080):
    x0 = w / 2 - 0.5
    y0 = h / 2 - 0.5
    # print('angle:', angle)
    theta = int(angle) * np.pi / 180.0
    # print('theta:', theta)
    xy = list(zip(_x, _y))  # list(zip object) python3
    x = [int((i - x0) * np.cos(theta) - (j - y0) * np.sin(theta) + x0) for (i, j) in xy]
    y = [int((i - x0) * np.sin(theta) + (j - y0) * np.cos(theta) + y0) for (i, j) in xy]
    xy = list(zip(x, y))
    xy = [[i, j] for (i, j) in xy if i < w and j < h]
    x = [i for [i, j] in xy]
    y = [j for [i, j] in xy]

    return x, y


def coord_trans(_x, _y, dx, dy, w=1920, h=1080):
    x = [i + dx for i in _x]
    y = [j + dy for j in _y]
    xy = list(zip(x, y))
    xy = [[i, j] for (i, j) in xy if i < w and j < h]
    x = [i for [i, j] in xy]
    y = [j for [i, j] in xy]

    return x, y


def coord_zoom(_x, _y, r1, r2, r3, r4, w=1920, h=1080):
    w_r = r3 - r1
    h_r = r4 - r2
    a = w / w_r
    b = h / h_r

    _xy = list(zip(_x, _y))
    xy = [[i, j] for (i, j) in _xy if r1 < i < r3 and r2 < j < r4]
    x = [i for [i, j] in xy]
    y = [j for [i, j] in xy]

    x = [(i - r1) * a for i in _x]
    y = [(j - r2) * b for j in _y]
    x = list(map(int, x))
    y = list(map(int, y))

    return x, y


def coord_blur(_x, _y):
    x = _x
    y = _y
    return x, y


'''
def unchanged(_x, _y):
    x = _x
    y = _y
    return x, y
'''


def op_parse(op):
    if op.startswith('fliph'):
        op_name = 'fliph'
        op_args = None
        args_list = None

    elif op.startswith('flipv'):
        op_name = 'flipv'
        op_args = None
        args_list = None

    elif op.startswith('noise'):
        op_name = 'noise'
        op_args = op[5:]
        args_list = op_args

    elif op.startswith('rot'):
        op_name = 'rot'
        op_args = op[3:]
        args_list = [op_args]

    elif op.startswith('trans'):
        op_name = 'trans'
        op_args = op[5:]
        args_list = op_args.split('_')

    elif op.startswith('zoom'):
        op_name = 'zoom'
        op_args = op[4:]
        args_list = op_args.split('_')

    elif op.startswith('blur'):
        op_name = 'blur'
        op_args = op[4:]
        args_list = op_args
    else:
        op_name = None
        op_args = None
        args_list = None
    print(op_name)
    print(args_list)

    return op_name, args_list


def coordinate_transform(_x, _y, op_name, _args_list):
    if op_name == 'fliph':
        x, y = coord_fliph(_x, _y)
    elif op_name == 'flipv':
        x, y = coord_flipv(_x, _y)
    elif op_name == 'noise':
        x, y = coord_noise(_x, _y)
    elif op_name == 'rot':
        x, y = coord_rot(_x, _y, _args_list[0])
    elif op_name == 'trans':
        x, y = coord_trans(_x, _y, _args_list[0], _args_list[1])
    elif op_name == 'zoom':
        x, y = coord_zoom(_x, _y, int(_args_list[0]), int(_args_list[1]), int(_args_list[2]),
                          int(_args_list[3]))
    elif op_name == 'blur':
        x, y = coord_blur(_x, _y)
    return x, _y


def main(_images_folder_name, _json_name):
    with open(_json_name, 'r') as f:
        data = json.load(f)
        print(len(data))

    all_annotation = dict()

    for f in os.listdir(_images_folder_name):

        if f.endswith('.jpg'):
            # '43-2018_05_03_16_57_50.jpg'
            # '6-2018_05_03_15_42_44__zoom0_0_1920_1000__rot60.jpg'

            print(f)
            if '__' in f:  # If it's an augmented image.
                original_name = f.split('__')[0]+'.jpg'
                print(original_name)

                size = os.path.getsize('./' + _images_folder_name + '/' + f)
                filesize = str(size)
                print(filesize)
                filename = f.split('.jpg')[0]
                print(filename)
                op_split = filename.split('__')
                img_annotation_key = f + filesize

                for i in data:
                    if i.startswith(original_name):
                        if data[i]['filename'] == original_name:
                            regions = data[i]['regions']
                            img_annotation = {img_annotation_key: {'fileref': '', 'size': size, 'filename': f,
                                                                   'base64_img_data': '', 'file_attributes': {},
                                                                   'regions': {}
                                                                   }
                                              }
                            all_regions = {'regions': {}}
                            for i in regions:
                                print(i)
                                _x = regions[i]['shape_attributes']['all_points_x']
                                _y = regions[i]['shape_attributes']['all_points_y']
                                id = regions[i]['region_attributes']['id']

                                if len(op_split) == 2:
                                    op1 = op_split[1]
                                    op2 = op_split[2]
                                    op1_name, args_list1 = op_parse(op1)
                                    op2_name, args_list2 = op_parse(op2)
                                    x, y = coordinate_transform(_x, _y, op1_name, args_list1)
                                    x, y = coordinate_transform(x, y, op2_name, args_list2)

                                else:
                                    op = op_split[1]
                                    op_name, args_list = op_parse(op)
                                    x, y = coordinate_transform(_x, _y, op_name, args_list)

                                region = {i: {'shape_attributes': {'name': 'polygon', 'all_points_x': x,
                                                                   'all_points_y': y},
                                              'region_attributes': {'id': id}
                                              }
                                          }
                                all_regions['regions'].update(region)
                            img_annotation[img_annotation_key].update(all_regions)
                            print(img_annotation)

                all_annotation.update(img_annotation)
            else:  # If it's the original image.
                for i in data:
                    if i.startswith(f):
                        if data[i]['filename'] == f:
                            img_annotation = data[i].copy()
                all_annotation.update(img_annotation)

    print(all_annotation)

    new_json_name = images_folder_name + '.json'
    with open(new_json_name, 'w') as f:
        json.dump(all_annotation, f)


if __name__ == "__main__":

    images_folder_name = sys.argv[1]
    json_name = sys.argv[2]
    main(images_folder_name, json_name)












