from tkinter import *
import tkinter.filedialog as fd
# import csv
# import numpy

class UI:
    def __init__(self, master):
        """
        Constructor for the UI class.
        """
        load_but = Button(master, text='Load file', command=self.load_file)
        load_but.pack()

    def load_file(self):
        """
        Load the file using file picker.
        :return:
        """
        filename = fd.askopenfilename()
        if filename:
            # do stuff with the file.
            # open it as csv or as numpy object.
            print('File picked is : {}'.format(filename))
        else:
            pass


def main():
    """
    This will be called when te program starts.
    :return:
    """
    root = Tk()
    root.title('CS 5593 Project')
    root.geometry('500x500')

    # create the UI to display
    ui = UI(root)

    # keep the UI running
    root.mainloop()


if __name__ == '__main__':
    main()
