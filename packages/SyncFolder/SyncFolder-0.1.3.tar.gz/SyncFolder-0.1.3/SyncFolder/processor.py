import hashlib
import os
import shutil
import sys


import argparse

def main():
    parser=argparse.ArgumentParser(description='Python package for synchronizing folders.')

    parser.add_argument('from_folder_path',type=str,help='source folder path')
    parser.add_argument('to_folder_path',type=str,help='target folder path')

    args=parser.parse_args()

    sync(args.from_folder_path,args.to_folder_path)

def sync(from_folder_path, to_folder_path):
    _check_from_folder_path(from_folder_path)
    _check_to_folder_path(to_folder_path)

    if os.path.isdir(from_folder_path):
        sync_folder(from_folder_path, to_folder_path)
    elif os.path.isfile(from_folder_path):
        sync_file(from_folder_path, to_folder_path)
    else:
        raise Exception('{} IS NOT A FILE NOR A FOLDER!')


def _check_from_folder_path(from_folder_path):
    if not os.path.exists(from_folder_path):
        raise Exception('{} NOT EXISTS!'.format(from_folder_path))


def _check_to_folder_path(to_folder_path):
    if not os.path.exists(to_folder_path):
        print('{} not exists, mkdir? yes(y) or exit(n) ...')

        is_mkdir = input().strip()
        while len(is_mkdir) < 1:
            is_mkdir = input().strip()

        if is_mkdir == 'y' or is_mkdir == 'yes':
            os.mkdir(to_folder_path)
        else:
            sys.exit(0)


def sync_folder(from_folder_path, to_folder_path):
    base_from_path = from_folder_path
    base_to_path = to_folder_path

    for file_folder_name in os.listdir(base_from_path):
        from_file_folder_path = os.path.join(base_from_path, file_folder_name)
        to_file_folder_path = os.path.join(base_to_path, file_folder_name)

        if os.path.isdir(from_file_folder_path):
            
            if not os.path.exists(to_file_folder_path):
                os.mkdir(to_file_folder_path)

            sync_folder(from_file_folder_path, to_file_folder_path)
        elif os.path.isfile(from_file_folder_path):
            sync_file(from_file_folder_path, to_file_folder_path)
        else:
            raise Exception('{} IS NEITHER A FILE NOR A FOLDER!'.
                            format(from_file_folder_path))


def sync_file(from_file_path, to_file_path):
    if not os.path.exists(to_file_path):
        shutil.copyfile(from_file_path, to_file_path)
        return

    from_file_size, from_file_last_modified_time = _get_size_mtime(
        from_file_path)
    to_file_size, to_file_last_modified_time = _get_size_mtime(to_file_path)
    if (from_file_size != to_file_size
            or from_file_last_modified_time != to_file_last_modified_time):
        shutil.copyfile(from_file_path, to_file_path)
        return

    from_file_md5 = _get_md5_of(from_file_path)
    to_file_md5 = _get_md5_of(to_file_path)
    if from_file_md5 != to_file_md5:
        shutil.copyfile(from_file_path, to_file_path)


def _get_size_mtime(from_file_path):
    stat_info = os.stat(from_file_path)
    file_size, last_modified_time = stat_info.st_size, stat_info.st_mtime
    return file_size, last_modified_time


def _get_md5_of(from_file_path):
    md5 = hashlib.md5()
    with open(from_file_path, 'rb') as fr:
        while True:
            file_chunk = fr.read(4096)
            if not file_chunk:
                break
            md5.update(file_chunk)
    md5 = md5.hexdigest()
    return md5
