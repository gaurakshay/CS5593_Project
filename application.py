#!/usr/bin/env python3

from tkinter import *
import tkinter.filedialog as fd
import csv
# import pandas

class Application(Frame):
    filename = None
    table_f = None

    def __init__(self, master=None):
        """
        Constructor for the UI class.
        """
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.load_but = Button(self, text='Load file', command=self.load_file)
        self.load_but.pack(side=TOP, padx=5, pady=5)
        self.anlyz_but = Button(self, text='Analyze', command = self.analyze_data)  # add command to this button
        self.anlyz_but.pack(side=TOP, padx=5, pady=5)

    def analyze_data(self):
        if not self.filename:
            return

        df = pandas.read_csv(self.filename)
        # Pass into implementation
        # predicted_df = implementation(df)

        predicted_list = predicted_df.values.tolist()
        self.create_table_from_list(predicted_list)


    def create_table_from_list(self, data):
        if self.table_f:
            self.table_f.destroy()

        nrow = len(data) if len(data) < 40 else 40
        ncol = len(data[0])
        self.table_f = Frame(self, bg='black')
        self.table_f.pack(side=BOTTOM)
        for row in range(nrow):
            for col in range(ncol):
                label = Label(self.table_f, text=data[row][col])
                label.grid(row=row, column=col, sticky='nsew', padx=1, pady=1)


    def create_table(self, filename):
        data = list()
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                data.append(row)
        self.create_table_from_list(data)


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
            self.filename = filename
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
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))

    # create the UI to display
    ui = Application(master=root)

    # keep the UI running
    root.mainloop()


if __name__ == '__main__':
    main()
