""" Created by jieyi on 5/1/17. """
import os

import dropbox
from decorator_check_login import DecoratorCheckLogin
from dropbox import files
from dropbox.exceptions import ApiError

token_file = 'access.token'


class DropboxHelper:
    def __init__(self, token=None):
        self.SYNC_FOLDER_NAME = 'Sync'
        self.__token = token
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
        CHUNK_SIZE = 10 * 1024 * 1024
        full_src_path = os.path.expanduser(src_path)
        file_size = os.path.getsize(full_src_path)

        if not os.path.isfile(full_src_path):
            return print('This is not a file...')

        try:
            res = None
            with open(full_src_path, 'rb') as f:
                print('Finished opening the zip file...')
                # If the file size is less than 20MB.
                if (file_size >> 20) < 20:
                    # TODO: 5/2/17 If the file exists, we should update it.
                    res = self.__connect.files_upload(f.read(), dst_path, mode=files.WriteMode.overwrite, mute=True)
                else:
                    # Starting the uploading session.
                    upload_session_start_result = self.__connect.files_upload_session_start(f.read(CHUNK_SIZE))
                    cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id,
                                                               offset=f.tell())
                    commit = dropbox.files.CommitInfo(path=dst_path)

                    print(f'Uploading... now finished {format((f.tell() / file_size) * 100, ".2f")}%...')
                    while f.tell() < file_size:
                        if (file_size - f.tell()) <= CHUNK_SIZE:
                            # The tail of the uploading session and finishing the cursor.
                            res = self.__connect.files_upload_session_finish(f.read(CHUNK_SIZE), cursor, commit)
                        else:
                            # According to the uploading session, continuing uploading the file.
                            self.__connect.files_upload_session_append(f.read(CHUNK_SIZE), cursor.session_id,
                                                                       cursor.offset)
                            print(f'Uploading... now finished {format((f.tell() / file_size) * 100, ".2f")}%...')
                            cursor.offset = f.tell()
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
        with open(os.path.expanduser(os.path.join(os.path.dirname(__file__), token_file))) as f:
            content = [c.strip() for c in f.readlines()]

        if not self.__token:
            self.__token = content[1]  # token.

        self.__connect = dropbox.Dropbox(self.__token)

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
    d = DropboxHelper()
    # d.create_folder('/tt')
    # print(d.delete_file('/imgres.jpg'))
    print(d.upload_file('~/Downloads/test.zip', '/test.zip'))
    # print('res =', d.upload_file('~/Downloads/test.jpg', '/test.jpg'))
    # print(d.download_file('/tt', '~/Downloads/11.jpg'))
    # print(d.search_file_or_folder('/Synccc', 'test'))


if __name__ == '__main__':
    main()
