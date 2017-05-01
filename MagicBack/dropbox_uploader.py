""" Created by jieyi on 5/1/17. """
import os

import dropbox
from decorator_check_login import DecoratorCheckLogin
from dropbox.exceptions import ApiError

token_file = 'access.token'


class DropboxUploader:
    def __init__(self):
        self.SYNC_FOLDER_NAME = 'Sync'
        self.__connect = None
        self.__is_sync_folder = False

        self.__pre_process()

    def test(self):
        self.__pre_process()
        self.__is_sync_folder = self.search_file_or_folder()

        if self.__is_sync_folder:
            for entry in self.__connect.files_list_folder('/' + self.SYNC_FOLDER_NAME).entries:
                print(entry.name)
        pass

    @DecoratorCheckLogin()
    def search_file_or_folder(self, path, file_name=''):
        try:
            return self.__connect.files_search(path, file_name)
        except ApiError as e:
            print(e)

    # Create a folder.
    @DecoratorCheckLogin()
    def create_folder(self, path):
        try:
            return self.__connect.files_create_folder(path)
        except ApiError as e:
            print(e)

    # Upload file only.
    @DecoratorCheckLogin()
    def upload_file(self, src_path, dst_path):
        try:
            with open(os.path.expanduser(src_path), 'rb') as f:
                res = self.__connect.files_upload(f.read(), dst_path, mute=True)
            return res
        except ApiError as e:
            print(e)

    # Download file only.
    @DecoratorCheckLogin()
    def download_file(self, src_path, dst_path):
        try:
            return self.__connect.files_download_to_file(os.path.expanduser(dst_path), src_path)
        except ApiError as e:
            print(e)

    # Delete file and folder.
    @DecoratorCheckLogin()
    def delete_file(self, path):
        try:
            return self.__connect.files_delete(path)
        except ApiError as e:
            print(e)

    def __pre_process(self):
        with open(token_file) as f:
            content = [c.strip() for c in f.readlines()]

        token = content[1]  # token.
        self.__connect = dropbox.Dropbox(token)

        # Checking.
        try:
            self.__connect.users_get_current_account()
        except Exception as e:
            self.__connect = None
            print(e)

    @property
    def connection(self):
        return self.__connect


def main():
    d = DropboxUploader()
    # d.create_folder('/tt')
    # print(d.delete_file('/imgres.jpg'))
    print(d.upload_file('~/Downloads/aa', '/bb'))
    # print(d.download_file('/tt', '~/Downloads/11.jpg'))
    # print(d.search_file_or_folder('/Synccc', 'test'))


if __name__ == '__main__':
    main()
