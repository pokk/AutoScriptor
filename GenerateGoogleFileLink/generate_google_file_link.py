""" Created by jieyi on 4/27/17. """
import io
import sys
from tkinter import Frame, Tk, Label, Entry
from tkinter.constants import FALSE

# Simulate the redirect stdin.
if len(sys.argv) > 1:
    filename = sys.argv[1]
    inp = ''.join(open(filename, "r").readlines())
    sys.stdin = io.StringIO(inp)


class AppGui(Frame):
    def __init__(self, master=None):
        # Init the window frame.
        Frame.__init__(self, master)
        self.grid()

        # Keeping the tk object.
        self.master = master

        # Init the components.
        self.label_id = Label(self, text='Google File Share Link:')
        self.entry_id = Entry(self, width=50)
        self.label_title = Label(self, text='Example:')
        self.label_example = Label(self, text='https://drive.google.com/open?id=FILE_ID')

        # Setting the components.
        self.__create_component()

    def callback(self, event):
        if 'Return' == event.keysym:
            # Copy them to the clipboard.
            self.master.clipboard_clear()
            self.master.clipboard_append(self.entry_id.get().replace('open', 'uc'))
            # Clear the entry.
            self.entry_id.delete(0, 'end')

    def __create_component(self):
        self.label_id.grid(row=0, column=0)
        self.entry_id.grid(row=0, column=1)
        self.label_title.grid(row=1, column=0)
        self.label_example.grid(row=1, column=1)
        self.entry_id.focus()
        self.entry_id.bind('<Key>', self.callback)


def main():
    tk = Tk()
    tk.resizable(width=FALSE, height=FALSE)
    tk.title('Change Google sharing uri to img uri')
    app = AppGui(tk)

    app.mainloop()


if __name__ == '__main__':
    main()
