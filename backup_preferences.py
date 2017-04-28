""" Created by jieyi on 4/28/17. """
import io
import os
import sys
from shutil import copytree, rmtree

# Simulate the redirect stdin.
if len(sys.argv) > 1:
    filename = sys.argv[1]
    inp = ''.join(open(filename, "r").readlines())
    sys.stdin = io.StringIO(inp)


def decorate_check_destination(fun):
    def decorate_function(*args, **kwargs):
        destination_path = os.path.expanduser('~/Dropbox')
        # Checking if Dropbox is installed or not.
        if os.path.exists(destination_path):
            sync_folder = '/'.join([destination_path, 'Sync'])
            # Checking if sync folder exists or not.
            if not os.path.exists(sync_folder):
                # If not, create it.
                os.mkdir(sync_folder)

            return fun(*args, **kwargs)
        else:
            print('You didn\'t install Dropbox...')

    return decorate_function


def back_up_alfred3():
    alfred_src_path = os.path.expanduser('~/Library/Application Support/Alfred 3')
    alfred_preference_file_name = 'Alfred.alfredpreferences'
    alfred_dest_path = os.path.expanduser('~/Dropbox/Sync')

    # Checking if Alfred and Dropbox are installed or not.
    if alfred_src_path and alfred_dest_path:
        alfred_src_full_path = '/'.join([alfred_src_path, alfred_preference_file_name])
        alfred_dest_full_path = '/'.join([alfred_dest_path, alfred_preference_file_name])

        print('Backup Alfred preferences...')
        # If there exists a Alfred preference, then remove it.
        if os.path.exists(alfred_dest_full_path):
            rmtree(alfred_dest_full_path)
        # Sync the preference.
        copytree(alfred_src_full_path, alfred_dest_full_path)
    else:
        print('You didn\'t install Alfred or Dropbox.')

    print('Finished sync Alfred preference!!')


def back_up_bettertouchtool():
    pass


@decorate_check_destination
def back_up_zsh_bash():
    print('OK')
    pass


def back_up_():
    pass


def main():
    # back_up_alfred3()
    back_up_zsh_bash()


if __name__ == '__main__':
    main()
