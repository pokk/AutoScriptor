""" Created by jieyi on 4/30/17. """
import os
from shutil import rmtree, copyfile, copytree

from __init__ import warning_str

from MagicBack.utils_zip import zip_files

temp_folder = '~/Documents'


class DecoratorCheckDestination:
    @staticmethod
    def remove_backup(path):
        if os.path.isdir(path):
            rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)

    @staticmethod
    def copy_backup(src, dst):
        if os.path.isdir(src):
            copytree(src, dst)
        elif os.path.isfile(src):
            copyfile(src, dst)

    def __call__(self, func):
        def wrapper(*args):
            destination_path = os.path.expanduser('~/Dropbox')
            # Assign the message callback function.
            msg_callback = args[2]
            # Checking if Dropbox is installed or not.
            if os.path.exists(destination_path):
                sync_folder = '/'.join([destination_path, 'Sync'])
                # Checking if sync folder exists or not.
                if not os.path.exists(sync_folder):
                    # If not, create it.
                    os.mkdir(sync_folder)

                src, dst = func(args[0], args[1], sync_folder, args[2])
                
                print(src)

                zip_files(src, os.path.join(temp_folder, '.'.join([args[1].split('.')[0], 'zip'])))
                # print(dst)

                # # If there exists a src preference, then remove it.
                # for s, d in zip(src, dst):
                #     # Ignore the src which isn't exist.
                #     if not os.path.exists(s):
                #         msg_callback(warning_str % s.split('/')[-1])
                #         continue
                #     if os.path.exists(d):
                #         self.remove_backup(d)
                #     # For that there are only file.
                #     target_folder = '/'.join(d.split('/')[:-1])
                #     if not os.path.exists(target_folder):
                #         # If not, create it.
                #         os.mkdir(target_folder)
                # 
                #     # Sync the preference.
                #     self.copy_backup(s, d)
                # 
                #     msg_callback(f'Finished sync {d.split("/")[-1]}\n')
            else:
                msg_callback(warning_str % 'Dropbox')

        return wrapper


def main():
    pass


if __name__ == '__main__':
    main()
