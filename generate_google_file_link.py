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
        Frame.__init__(self, master)
        self.grid()

        self.master = master

        self.label_id = Label(self, text='Google File ID:')
        self.entry_id = Entry(self, width=50)

        self.__create_component()

    def callback(self, event):
        if 'Return' == event.keysym:
            self.master.clipboard_clear()
            self.master.clipboard_append(self.entry_id.get().replace('open', 'uc'))
            self.entry_id.delete(0, 'end')

    def __create_component(self):
        self.label_id.grid(row=0, column=0)
        self.entry_id.grid(row=0, column=1)
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
