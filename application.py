from tkinter import *
import tkinter.filedialog as fd
import csv
# import numpy

class Application(Frame):
    def __init__(self, master=None):
        """
        Constructor for the UI class.
        """
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.load_but = Button(self, text='Load file', command=self.load_file)
        self.load_but.pack(sid=TOP, padx=5, pady=5)
        self.anlyz_but = Button(self, text='Analyze')  # add command to this button
        self.anlyz_but.pack(side=TOP, padx=5, pady=5)

    def create_table(self, filename):
        data = list()
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                data.append(row)
        nrow = len(data)
        ncol = len(data[0])
        table_f = Frame(self, bg='black')
        table_f.pack(side=BOTTOM)
        for row in range(nrow):
            for col in range(ncol):
                label = Label(table_f, text=data[row][col])
                label.grid(row=row, column=col, sticky='nsew', padx=1, pady=1)

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
            self.create_table(filename)
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
    ui = Application(master=root)

    # keep the UI running
    root.mainloop()


if __name__ == '__main__':
    main()
