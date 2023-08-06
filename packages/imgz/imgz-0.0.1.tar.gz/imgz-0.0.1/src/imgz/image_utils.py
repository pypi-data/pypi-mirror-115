# -*- coding: utf8 -*-

from os import path

# 图片后缀名
SUFFIX_IMAGE = ['.jpg', '.png', '.jpeg', '.bmp']


def split(abspath: str):
    dir_path = file_name = suffix = ''
    if abspath:
        dir_path = path.dirname(abspath)
        base_name = path.basename(abspath)
        split_array = path.splitext(base_name)
        file_name = split_array[0]
        suffix = split_array[1]

    return dir_path, file_name, suffix


def is_image_file(file_path):
    _, _, suffix = split(file_path)

    return suffix.lower() in SUFFIX_IMAGE
