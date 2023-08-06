# -*- coding: utf8 -*-

import os
import shutil
from os import path

import json
from loguru import logger

# 图片后缀名
SUFFIX_IMAGE = ['.jpg', '.png', '.jpeg', '.bmp']


def is_image_file(file_path):
    return filesuffix(file_path).lower() in SUFFIX_IMAGE


def filename(abspath: str) -> str:
    return path.splitext(path.basename(abspath))[0]


def filesuffix(abspath: str) -> str:
    return path.splitext(path.basename(abspath))[1]


def split(abspath: str):
    dir_path = file_name = suffix = ''
    if abspath:
        dir_path = path.dirname(abspath)
        base_name = path.basename(abspath)
        split_array = path.splitext(base_name)
        file_name = split_array[0]
        suffix = split_array[1]

    return dir_path, file_name, suffix


def dumps(data_json: dict):
    return json.dumps(data_json, sort_keys=True, indent=4, ensure_ascii=False)


def write_json(outfile, json_dict: dict):
    result = False

    if json_dict and len(json_dict):
        backup_file = outfile + '.backup'

        father_path = path.abspath(path.join(path.dirname(outfile), path.curdir))
        os.makedirs(father_path, exist_ok=True)

        try:
            if path.exists(outfile) and path.getsize(outfile):
                shutil.copy(outfile, backup_file)

            with open(outfile, 'w+') as out:
                json.dump(json_dict, out)

            result = path.exists(outfile) and path.getsize(outfile)
        except Exception as e:
            logger.exception(e)

            shutil.copy(backup_file, outfile)

    return result
