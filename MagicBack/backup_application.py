""" Created by jieyi on 4/29/17. """
import os
from copy import deepcopy

from __init__ import warning_str
from decorator_backup_process import DecoratorUploader, DecoratorDownloader


class BackupRestoreApp:
    def __init__(self):
        self.__folder_path = os.path.join(os.path.dirname(__file__), 'application')
        self.__settings = []
        self.__ignore_settings = []
        self.__app_name = ''
        self.__src_file_path = []
        self.__dst_file_path = []
        self.__is_find_version = False
        self.__is_backup = True
        self.__msg_callback = None
        self.__remote_account = None

    def backup_restore_process(self, msg_callback, is_backup=True):
        self.__pre_process()
        self.__is_backup = is_backup
        self.__msg_callback = msg_callback

        # Parsing each of setting files' content.
        for stg in list(set(self.__settings) - set(self.__ignore_settings)):
            msg_callback(f'Starting to backup the {stg}...\n')
            if self.__is_backup:
                # Init the lists.
                self.__src_file_path = []
                self.__dst_file_path = []

                # Start syncing the preferences.
                self._backup_preferences(stg, self.__msg_callback)
            else:
                self._restore_preferences(stg, self.__msg_callback)
                pass
            self.__msg_callback('\n\n----------------------------------\n\n')

        # Show the msg for finishing syncing.
        # messagebox.showinfo("Notification", "All application's preferences have finished syncing.")
        self.__msg_callback('!!!!!! All application\'s preferences have finished syncing. !!!!!\n')

    @DecoratorUploader()
    def _backup_preferences(self, setting_file, msg_callback):
        with open(os.path.join(self.__folder_path, setting_file)) as f:
            content = [c.strip() for c in f.readlines()]

        self.__obtain_app_name(setting_file)
        self.__obtain_src_file_path(content)

        return self.__src_file_path

    @DecoratorDownloader()
    def _restore_preferences(self, setting_file, msg_callback):
        return

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
            self.__src_file_path = [os.path.expanduser(path) for path in file_content
                                    if path is not None and os.path.exists(os.path.expanduser(path))]

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

        self.__msg_callback(warning_str % folder)
        return None

    @property
    def ignore_setting(self):
        return self.__ignore_settings

    @ignore_setting.setter
    def ignore_setting(self, value):
        self.__ignore_settings = value

    @property
    def remote_account(self):
        return self.__remote_account

    @remote_account.setter
    def remote_account(self, value):
        self.__remote_account = value


def main():
    b = BackupRestoreApp()
    b.backup_restore_process(None)


if __name__ == '__main__':
    main()
