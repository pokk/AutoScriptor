""" Created by jieyi on 4/29/17. """
import io
import os
import sys
from copy import deepcopy
from shutil import rmtree, copytree, copyfile

# Simulate the redirect stdin.
if len(sys.argv) > 1:
    filename = sys.argv[1]
    inp = ''.join(open(filename, "r").readlines())
    sys.stdin = io.StringIO(inp)

warning_str = '*** Warning!!! You didn\'t have "%s"...'
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

                src, dst = func(args[0], args[1], sync_folder)

                # If there exists a src preference, then remove it.
                for s, d in zip(src, dst):
                    # Ignore the src which isn't exist.
                    if not os.path.exists(s):
                        print(warning_str % s.split('/')[-1])
                        continue
                    if os.path.exists(d):
                        self.remove_backup(d)

                    # Sync the preference.
                    self.copy_backup(s, d)

                    print(f'Finished sync {d.split("/")[-1]}')
            else:
                print(warning_str % 'Dropbox')

        return wrapper


class BackupApp:
    def __init__(self):
        self.__folder_path = '/'.join([os.getcwd(), 'application'])
        self.__settings = []
        self.__app_name = ''
        self.__src_file_path = []
        self.__dst_file_path = []

    def backup_process(self):
        self.__pre_process()

        # Parsing each of setting files' content.
        for stg in self.__settings:
            # Init the lists.
            self.__src_file_path = []
            self.__dst_file_path = []

            self.sync_preferences(stg)
            print('\n----------------------------------\n')

    @DecoratorCheckDestination()
    def sync_preferences(self, setting_file, dst_path):
        with open('/'.join([self.__folder_path, setting_file])) as f:
            content = [c.strip() for c in f.readlines()]

        self.__obtain_app_name(setting_file)
        print(start_syn_str % self.__app_name)
        self.__obtain_src_file_path(content)
        self.__obtain_dst_file_path(dst_path, content)

        return self.__src_file_path, self.__dst_file_path

    def __obtain_app_name(self, app_name):
        self.__app_name = app_name.split('.')[0]

    def __obtain_src_file_path(self, file_content):
        is_find_version = False
        shift_number = 0
        copy_content = deepcopy(file_content)

        # Obtain all the src path from each setting files.
        for index, c in enumerate(copy_content):
            # If '#' or '[preferences' in the word.
            if any(key_word in c for key_word in ['#', '[preferences']):
                is_find_version = 'slight' in c
                file_content.remove(c)
                shift_number += 1
            else:
                if is_find_version:
                    path_with_version = self.__find_version(c)
                    file_content[index - shift_number] = path_with_version

            # Translating to the real path.
            self.__src_file_path = [os.path.expanduser(path) for path in file_content if path is not None]

    def __obtain_dst_file_path(self, dst_path, file_content):
        for c in file_content:
            if c is not None:
                self.__dst_file_path.append('/'.join([dst_path, c.split('/')[-1]]))

    def __pre_process(self):
        # Obtaining all setting files.
        self.__settings = [name for name in os.listdir(self.__folder_path)
                           if os.path.isfile('/'.join([self.__folder_path, name]))]

    def __find_version(self, file_name):
        # Extracting folder name.
        folder = file_name.split('/')[-1]
        folder_path = file_name.split('/')[:-1]
        # Search app name with version.
        for folder_name in os.listdir(os.path.expanduser('/'.join(folder_path))):
            if folder in folder_name:
                folder_path.append(folder_name)
                return '/'.join(folder_path)

        print(warning_str % folder)
        return None


def main():
    # d = '/'.join([os.getcwd(), 'application'])
    # a = [name for name in os.listdir(d) if os.path.isfile('/'.join([d, name]))]
    # with open('/'.join([d, a[0]])) as f:
    #     content = f.readlines()
    # 
    # content = [x.strip() for x in content]
    b = BackupApp()
    b.backup_process()


if __name__ == '__main__':
    main()
