import os
import zipfile


def decompress(zip_dir, fd_dir):
    if not os.path.exists(os.path.join(fd_dir)):
        os.makedirs(fd_dir)
    with zipfile.ZipFile(zip_dir) as f:
        for name in f.namelist():
            f.extract(name, fd_dir)


def get_file_dir(file_type, fd_dir):
    file_type = '.{}'.format(file_type.replace('.', ''))
    for i in os.walk(fd_dir):
        for f in i[2]:
            if os.path.splitext(f)[-1] == file_type:
                return os.path.abspath(i[0])


def compress_folder(zip_file, fd_dir):
    if not os.path.exists(os.path.dirname(zip_file)):
        os.makedirs(os.path.dirname(zip_file))
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as f:
        arr = os.listdir(fd_dir)
        for i in arr:
            if i.split('.')[-1] != 'zip':
                f.write(os.path.join(fd_dir, i))
