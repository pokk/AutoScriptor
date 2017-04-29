""" Created by jieyi on 4/29/17. """
import io
import sys

from Backup.backup_template import BackupTemplate

# Simulate the redirect stdin.
if len(sys.argv) > 1:
    filename = sys.argv[1]
    inp = ''.join(open(filename, "r").readlines())
    sys.stdin = io.StringIO(inp)


class BackupAlfred(BackupTemplate):
    def _obtain_app_name(self):
        return 'Alfred'

    def _obtain_file_name(self):
        return 'Alfred.alfredpreferences'

    def _obtain_src_path(self):
        return '~/Library/Application Support/Alfred 3'


def main():
    alfred = BackupAlfred()
    alfred.backup_process()


if __name__ == '__main__':
    main()
