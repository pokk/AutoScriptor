""" Created by jieyi on 5/1/17. """
import os
import zipfile


def zip_files(src_path, dst_path_with_filename='zipfile.zip'):
    with zipfile.ZipFile(os.path.expanduser(dst_path_with_filename), 'w', zipfile.ZIP_DEFLATED) as zf:
        for path in src_path:
            if os.path.isdir(path):
                for root, dirs, files in os.walk(os.path.expanduser(path)):
                    for file in files:
                        zf.write(os.path.join(root, file))
            elif os.path.isfile(path):
                zf.write(path)


def unzip_files(zipfile_path, dst_path):
    with zipfile.ZipFile(os.path.expanduser(zipfile_path), 'r') as zf:
        zf.extractall(os.path.expanduser(dst_path))


def main():
    zip_files(['/Users/jieyi/Library/Preferences/com.apple.Terminal.plist'], os.path.expanduser('~/Documents/test.zip'))
    unzip_files('~/Downloads/terminal.zip', '~/Downloads')


if __name__ == '__main__':
    main()
