""" Created by jieyi on 4/29/17. """
import os
from copy import deepcopy

from Backup import start_syn_str, warning_str
from Backup.decorator_back_process import DecoratorCheckDestination


class BackupRestoreApp:
    def __init__(self):
        self.__folder_path = '/'.join([os.getcwd(), 'application'])
        self.__settings = []
        self.__ignore_settings = []
        self.__app_name = ''
        self.__src_file_path = []
        self.__dst_file_path = []
        self.__is_find_version = False
        self.__is_backup = True

    def backup_restore_process(self, is_backup=True):
        self.__pre_process()
        self.__is_backup = is_backup

        # Parsing each of setting files' content.
        for stg in list(set(self.__settings) - set(self.__ignore_settings)):
            # Init the lists.
            self.__src_file_path = []
            self.__dst_file_path = []

            # Start syncing the preferences.
            self._sync_preferences(stg)
            print('\n----------------------------------\n')

    @DecoratorCheckDestination()
    def _sync_preferences(self, setting_file, dst_path):
        with open('/'.join([self.__folder_path, setting_file])) as f:
            content = [c.strip() for c in f.readlines()]

        self.__obtain_app_name(setting_file)
        print(start_syn_str % self.__app_name)
        self.__obtain_src_file_path(content)
        self.__obtain_dst_file_path(dst_path, content)

        return (self.__src_file_path, self.__dst_file_path) if self.__is_backup \
            else (self.__dst_file_path, self.__src_file_path)

    def __obtain_app_name(self, app_name):
        self.__app_name = app_name.split('.')[0]

    def __obtain_src_file_path(self, file_content):
        self.__is_find_version = False  # Checking the newest file for sync.
        shift_number = 0  # After deleting the number of the redundant comment line.
        copy_content = deepcopy(file_content)

        # Obtain all the src path from each setting files.
        for index, c in enumerate(copy_content):
            # If '#' or '[preferences' in the word.
            if any(key_word in c for key_word in ['#', '[preferences']):
                self.__is_find_version = 'slight' in c  # Mark the flag for searching the correct version.
                file_content.remove(c)
                shift_number += 1
            else:
                # If we need to add the version.
                if self.__is_find_version:
                    path_with_version = self.__find_version(c)
                    file_content[index - shift_number] = path_with_version

            # Translating to the real path.
            self.__src_file_path = [os.path.expanduser(path) for path in file_content if path is not None]

    def __obtain_dst_file_path(self, dst_path, file_content):
        for c in [fc for fc in file_content if fc is not None]:
            # If the file name are the same, we must separate them.
            new_file_name = '.'.join([c.split('/')[-1], c.split('/')[-2].split()[-1]]) if self.__is_find_version \
                else c.split('/')[-1]
            self.__dst_file_path.append('/'.join([dst_path, self.__app_name, new_file_name]))

    def __pre_process(self):
        # Obtaining all setting files.
        self.__settings = [name for name in os.listdir(self.__folder_path)
                           if os.path.isfile('/'.join([self.__folder_path, name]))]

    def __find_version(self, file_name):
        # Extracting folder name.
        folder = file_name.split('/')[-1]
        folder_path = '/'.join(file_name.split('/')[:-1])
        # Search app name with version from the folder direction.
        for folder_name in [f for f in os.listdir(os.path.expanduser(folder_path))
                            if os.path.isdir('/'.join([os.path.expanduser(folder_path), f]))]:
            if folder in folder_name:
                # Find it!!! Change the newest version file name.
                return '/'.join([folder_path, folder_name])

        print(warning_str % folder)
        return None

    @property
    def ignore_setting(self):
        return self.__ignore_settings

    @ignore_setting.setter
    def ignore_setting(self, value):
        self.__ignore_settings = value


def main():
    b = BackupRestoreApp()
    b.backup_restore_process()


if __name__ == '__main__':
    main()
