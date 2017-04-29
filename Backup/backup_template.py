""" Created by jieyi on 4/29/17. """
import io
import os
import sys
from abc import ABCMeta, abstractmethod
from shutil import rmtree, copytree, copyfile

# Simulate the redirect stdin.
if len(sys.argv) > 1:
    filename = sys.argv[1]
    inp = ''.join(open(filename, "r").readlines())
    sys.stdin = io.StringIO(inp)

warning_str = '*** Warning!!! You didn\'t have %s...'
start_syn_str = 'Start sync %s!!!'


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
            # Checking if Dropbox is installed or not.
            if os.path.exists(destination_path):
                sync_folder = '/'.join([destination_path, 'Sync'])
                # Checking if sync folder exists or not.
                if not os.path.exists(sync_folder):
                    # If not, create it.
                    os.mkdir(sync_folder)

                src, dst = func(args[0], sync_folder)

                print(src, dst)

                # If there exists a src preference, then remove it.
                if os.path.exists(dst):
                    self.remove_backup(dst)

                # Sync the preference.
                self.copy_backup(src, dst)

                print(f'Finished sync {dst}')
            else:
                print(warning_str % 'Dropbox')

        return wrapper


class BackupTemplate(metaclass=ABCMeta):
    @DecoratorCheckDestination()
    def backup_process(self, dst_path):
        if not all([self._obtain_app_name(), self._obtain_file_name(), self._obtain_src_path()]):
            print('Please input variables completely...')
            return

        src_path = os.path.expanduser(self._obtain_src_path())
        src_full_path = '/'.join([src_path, self._obtain_file_name()])
        dst_full_path = '/'.join([dst_path, self._obtain_file_name()])

        # Checking if Alfred is installed or not.
        if os.path.exists(src_full_path):
            print(start_syn_str % self._obtain_app_name())

            return src_full_path, dst_full_path
        else:
            print(warning_str % self._obtain_app_name())

    @abstractmethod
    def _obtain_app_name(self):
        pass

    @abstractmethod
    def _obtain_file_name(self):
        pass

    @abstractmethod
    def _obtain_src_path(self):
        pass


def main():
    pass


if __name__ == '__main__':
    main()
