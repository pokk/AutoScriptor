""" Created by jieyi on 4/30/17. """
import os
import shutil

from utils_zip import zip_files, unzip_files

temp_folder = '~/Documents'
root_remote_folder = '/Sync'


class DecoratorUploader:
    def __call__(self, func):
        def wrapper(*args):
            remote_account = args[0].remote_account
            app_name = args[1]
            # Assign the message callback function.
            msg_callback = args[2]

            src = func(*args)

            if not src or 0 == len(src):
                print()
                msg_callback(f'NOTICE!! You don\'t install the {app_name}\n\n')
                return

            # Zip variables.
            zip_file_name = '.'.join([app_name.split('.')[0], 'zip'])
            full_zip_file = os.path.expanduser(os.path.join(temp_folder, zip_file_name))

            # 1. Zip the app preferences.
            zip_files(src, full_zip_file)
            msg_callback('Finished packing preferences file to a zip package...\n')
            # 2. Upload.
            remote_account.upload_file(full_zip_file, os.path.join(root_remote_folder, zip_file_name))
            msg_callback(f'{zip_file_name} starts uploading...\n')
            # 3. Remove the temp file.
            os.remove(full_zip_file)
            msg_callback('Finished uploading your preferences and removing the temp zip package.\n')

        return wrapper


class DecoratorDownloader:
    def __call__(self, func):
        def wrapper(*args):
            remote_account = args[0].remote_account
            app_name = args[1]
            # Assign the message callback function.
            msg_callback = args[2]

            func(*args)

            # Zip variables.
            zip_file_name = '.'.join([app_name.split('.')[0], 'zip'])
            full_zip_file = os.path.expanduser(os.path.join(temp_folder, zip_file_name))

            # 1. Download.
            msg_callback(f'{zip_file_name} starts downloading...\n')
            remote_account.download_file(os.path.join(root_remote_folder, zip_file_name), full_zip_file)
            msg_callback(f'Finished downloading the {zip_file_name}...\n')
            # 2. Unzip the app preferences.
            unzip_files(full_zip_file, temp_folder)
            msg_callback(f'Finished unpacking {zip_file_name} preferences file in \'{temp_folder}\'...\n')
            # 3. Move the backup file to local path.
            self._move_file(os.path.join(temp_folder, 'Users'))
            # 4. Remove the temp file and unzip file.
            os.remove(full_zip_file)
            shutil.rmtree(os.path.expanduser(os.path.join(temp_folder, 'Users')))
            msg_callback('Finished removing the temp zip package.\n')

        return wrapper

    def _move_file(self, src):
        for dir_path, dir_names, file_names in os.walk(os.path.expanduser(src)):
            for filename in file_names:
                if '.DS_Store' not in filename:
                    os.rename(os.path.join(dir_path, filename), '/'.join([''] + dir_path.split('/')[4:] + [filename]))


def main():
    pass


if __name__ == '__main__':
    main()
