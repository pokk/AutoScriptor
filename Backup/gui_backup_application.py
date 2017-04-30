""" Created by jieyi on 4/30/17. """
import os
from tkinter import Tk, FALSE, Frame, W, Checkbutton, Button, BooleanVar

from backup_application import BackupRestoreApp


class AppGui(Frame):
    def __init__(self, master=None):
        self.__folder_path = '/'.join([os.getcwd(), 'application'])
        self.__check_var = []
        self.__check_button_list = []
        # Keeping the tk object.
        self.master = master

        # Init the window frame.
        Frame.__init__(self, master)
        self.grid()
        # Start the process!!
        self._process()

    def _process(self):
        # Init and set the components.
        self.__create_component()

    def __create_component(self):
        index = 0

        for index, f in enumerate([name for name in os.listdir(self.__folder_path)
                                   if os.path.isfile('/'.join([self.__folder_path, name]))]):
            self.__check_var.append(BooleanVar())
            self.__check_var[index].set(True)
            self.__check_button_list.append(Checkbutton(self, text=f, variable=self.__check_var[index],
                                                        onvalue=True, offvalue=False))
            self.__check_button_list[index].grid(row=index, column=0, sticky=W, columnspan=2)

        Button(self, text='Invert', command=self._invert_checkbutton).grid(row=index + 1, column=0)
        Button(self, text='Select All', command=self._select_all_checkbutton).grid(row=index + 1, column=1)
        Button(self, text='Deselect All', command=self._deselect_all_checkbutton).grid(row=index + 1, column=2)
        Button(self, text='Backup', command=self._backup_event).grid(row=index + 2, column=0)
        Button(self, text='Restore', command=self._restore_event).grid(row=index + 2, column=1)

    def _backup_event(self):
        self.__pre_backup_restore(True)

    def _restore_event(self):
        self.__pre_backup_restore(False)

    def _select_all_checkbutton(self):
        for cb in self.__check_button_list:
            cb.select()

    def _deselect_all_checkbutton(self):
        for cb in self.__check_button_list:
            cb.deselect()

    def _invert_checkbutton(self):
        for cb in self.__check_button_list:
            cb.toggle()

    def __pre_backup_restore(self, is_back=True):
        backup_process = BackupRestoreApp()
        ignore = [k.cget('text') for k, v in zip(self.__check_button_list, self.__check_var) if not v.get()]
        backup_process.ignore_setting = ignore
        # backup_process.backup_restore_process(is_back)


def main():
    tk = Tk()
    tk.resizable(width=FALSE, height=FALSE)
    tk.title('Backup & Restore application setting')
    app = AppGui(tk)

    app.mainloop()


if __name__ == '__main__':
    main()
