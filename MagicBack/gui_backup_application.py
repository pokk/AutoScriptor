""" Created by jieyi on 4/30/17. """
import os
import threading
import tkinter
from tkinter import BooleanVar, Button, Checkbutton, END, FALSE, Frame, Label, Text, Tk, W, messagebox

from backup_application import BackupRestoreApp
from decorator_backup_process import root_remote_folder
from dropbox_helper import DropboxHelper


class AppGui(Frame):
    def __init__(self, master=None):
        self.__folder_path = os.path.join(os.path.dirname(__file__), 'application')
        self.__check_var = []
        self.__check_button_list = []
        self.__msg_text = None
        self.__lock = threading.Lock()
        self.msg_line = 1

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
                                   if os.path.isfile(os.path.join(self.__folder_path, name))]):
            self.__check_var.append(BooleanVar())
            self.__check_var[index].set(True)
            self.__check_button_list.append(Checkbutton(self, text=f, variable=self.__check_var[index],
                                                        onvalue=True, offvalue=False, background='blue'))
            self.__check_button_list[index].grid(row=index, column=0, sticky=W, columnspan=2)

        self.__msg_text = Text(self)
        self.__msg_text.grid(row=1, column=2, rowspan=20)
        self.__msg_text.config(state=tkinter.DISABLED)
        self.__msg_text.tag_config('warning', background='yellow', foreground='blue')
        self.__msg_text.tag_config('finished', background='blue', foreground='white')
        self.__msg_text.tag_config('starting', background='green')
        self.__msg_text.tag_config('error', background='red', foreground='yellow')
        Label(self, text='Processing log').grid(row=0, column=2)
        Button(self, text='Invert', command=self._invert_checkbutton).grid(row=index + 1, column=0)
        Button(self, text='Select All', command=self._select_all_checkbutton).grid(row=index + 2, column=0)
        Button(self, text='Deselect All', command=self._deselect_all_checkbutton).grid(row=index + 2, column=1)
        Button(self, text='MagicBack', command=self._backup_event).grid(row=index + 3, column=0)
        Button(self, text='Restore', command=self._restore_event).grid(row=index + 3, column=1)

    def _backup_event(self):
        self.__active_thread_process(True)

    def _restore_event(self):
        self.__active_thread_process(False)

    def _select_all_checkbutton(self):
        for cb in self.__check_button_list:
            cb.select()

    def _deselect_all_checkbutton(self):
        for cb in self.__check_button_list:
            cb.deselect()

    def _invert_checkbutton(self):
        for cb in self.__check_button_list:
            cb.toggle()

    def __active_thread_process(self, is_back=True):
        if self.__lock.locked():
            messagebox.showinfo("Warning", "MagicBack is processing, you need to wait a moment.")
        else:
            threading.Thread(target=self.__pre_backup_restore, args=(is_back,)).start()

    def __pre_backup_restore(self, is_back=True):
        self.__lock.acquire()
        self.__msg_text.delete(1.0, END)
        backup_process = BackupRestoreApp()
        backup_process.remote_account = DropboxHelper(self.__add_msg)
        # Create a new sync folder on the remote.
        backup_process.remote_account.create_folder(root_remote_folder)
        ignore = [k.cget('text') for k, v in zip(self.__check_button_list, self.__check_var) if not v.get()]
        backup_process.ignore_setting = ignore
        backup_process.backup_restore_process(self.__add_msg, is_back)
        self.__lock.release()

    def __add_msg(self, msg):
        self.__msg_text.config(state=tkinter.NORMAL)
        # Insert the msg END of the text.
        self.__msg_text.insert(END, msg)
        # Scroll to the end.
        self.__msg_text.see(END)
        # Mark the yellow color when warning happened.
        if 'Warning' in msg:
            self.__add_text_color('warning', msg)
        elif 'to backup' in msg:
            self.__add_text_color('starting', msg)
        elif 'your preferences' in msg:
            self.__add_text_color('finished', msg)
        elif 'NOTICE' in msg:
            self.__add_text_color('error', msg)
        self.__msg_text.config(state=tkinter.DISABLED)

    def __add_text_color(self, tag, msg):
        current_line = float(self.__msg_text.index(END)) - 2
        self.__msg_text.tag_add(tag, str(current_line), f'{int(current_line)}.{len(msg)}')


def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def main():
    tk = Tk()
    tk.resizable(width=FALSE, height=FALSE)
    tk.title('MagicBack & Restore application setting')
    app = AppGui(tk)

    app.mainloop()


if __name__ == '__main__':
    main()
