""" Created by jieyi on 5/1/17. """
import os
import zipfile


def zip_files(src_path, dst_path_with_filename='zipfile.zip'):
    with zipfile.ZipFile(dst_path_with_filename, 'w', zipfile.ZIP_DEFLATED) as zf:
        for path in src_path:
            for root, dirs, files in os.walk(os.path.expanduser(path)):
                for file in files:
                    zf.write(os.path.join(root, file))


def unzip_files(zipfile_path, dst_path):
    with zipfile.ZipFile(os.path.expanduser(zipfile_path), 'r') as zf:
        zf.extractall(os.path.expanduser(dst_path))


def main():
    zip_files(['~/Downloads/aa', '~/Downloads/bb', '~/Workspace/note'], os.path.expanduser('~/Downloads/cool.zip'))
    unzip_files('~/Downloads/cool.zip', '/')


if __name__ == '__main__':
    main()
