from tkinter import *
import tkinter.filedialog as fd
import csv
import time
# import numpy
# import pandas


class Application(Frame):
    def __init__(self, master=None):
        """
        Constructor for the UI class.
        """
        self.root = master
        super().__init__(master)
        self.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.load_but = None  # Load Button
        self.analyze_but = None  # Analyze Button
        self.data = None  # Variable to store data from file.
        self.table_f = None  # Frame to hold the tabular data.
        self.status = None  # Label that shows the current status of the app.
        self.header_ch = None  # Checkbox to specify whether header exists or not.
        self.header = None  # Variable to access checkbox value.
        self.res_lab = None  # Label to show the results.
        self.create_widgets()

    def create_widgets(self):
        self.status = Label(self.root, bd=1, text='Pick a file to start.', relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)
        bot_frame = Frame(self)  # Frame to hold the load and analyze buttons.
        bot_frame.pack(side=BOTTOM, fill=X)
        self.analyze_but = Button(bot_frame, text='Analyze', state='disabled', command=self.analyze_data)  # add command to this button
        self.analyze_but.pack(side=RIGHT, padx=5)
        self.load_but = Button(bot_frame, text='Load file', command=self.load_file)
        self.load_but.pack(side=RIGHT, padx=5)

    def analyze_data(self):
        self.update_status('Analyzing.')
        Tk.update(self.root)
        # check if user data contains headers.
        if self.header.get():
            # use data excluding first row.
            pass
        else:
            # use all of the data.
            pass
        # here we can call the algorithm.
        final_result = self.test()
        self.update_status('Analysis complete.')
        self.del_table()
        self.show_results(final_result)

    def show_results(self, results):
        self.res_lab = Label(self, text=results)
        self.res_lab.pack(side=TOP)

    def test(self):
        time.sleep(2)
        return 'THE BITCOIN IS STABLE!!!'

    def update_status(self, status_):
        self.status.config(text=status_)

    def load_data(self, filename):
        self.data = list()
        # read data as list of lists or any other format.
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.data.append(row)
        self.update_status('Data loaded successfully.')

    def del_table(self):
        self.table_f.destroy()
        self.header = None
        self.header_ch.destroy()
        self.table_f.pack_forget()
        self.header_ch.pack_forget()

    def create_table(self, num_rows=10, data=None):
        """
        Create the table that shows snapshot of the CSV
        picked.
        :param num_rows:
        :return:
        """
        if self.res_lab:
            self.res_lab.destroy()
            self.res_lab.pack_forget()
        if data is None:
            data = self.data
        nrow = len(data)
        ncol = len(data[0])
        self.table_f = Frame(self, bg='black')
        self.table_f.pack(side=TOP)
        for row in range(min(num_rows, nrow)):
            for col in range(ncol):
                label = Label(self.table_f, text=data[row][col])
                label.grid(row=row, column=col, sticky='nsew', padx=1, pady=1)
        self.header = IntVar()
        self.header_ch = Checkbutton(self, text='Data contains header.', variable=self.header)
        self.header_ch.pack(side=TOP)
        self.update_status('Data displayed.')

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
            self.update_status('File selected.')

            # Load the data.
            self.load_data(filename)

            # Show data as table.
            self.create_table()

            # Enable analyze button.
            self.analyze_but.config(state='normal')
        else:
            pass


def main():
    """
    This will be called when the program starts.
    :return: NA
    """
    root = Tk()
    root.title('CS 5593 Project')
    root.geometry('500x500')

    # create the UI to display
    Application(master=root)

    # keep the UI running
    root.mainloop()


if __name__ == '__main__':
    main()
