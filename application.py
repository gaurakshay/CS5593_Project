#!/usr/bin/env python3

from tkinter import *
import tkinter.filedialog as fd
import csv
import pandas as pandas
# from ggplot import *
import pickle

#Local
from node import Node

serialized_file_name = 'trained_model.p'

# Check if a saved model exists
# load from file
def load_model():
    try:
        return pickle.load(open(serialized_file_name, "rb"))
    except:
        return None

class Application(Frame):
    filename = None
    table_f = None
    model = None

    def __init__(self, master=None):
        """
        Constructor for the UI class.
        """

        self.model = load_model()

        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.train_but = Button(self, text='Train model', command = self.train_model)
        self.train_but.pack(side=TOP, padx=5, pady=5)
        self.load_but = Button(self, text='Load CSV file and test up to 40 rows', command=self.load_file)
        self.load_but.pack(side=TOP, padx=5, pady=5)
        self.anlyz_but = Button(self, text='Analyze', command = self.analyze_data)  # add command to this button
        self.anlyz_but.pack(side=TOP, padx=5, pady=5)
        self.content_wrapper = Frame(self)
        self.content_wrapper.pack(expand=1, fill=BOTH)

    def train_model(self):
        filename = fd.askopenfilename()
        if not filename:
            return

        records = pandas.read_csv(filename)
        self.model = Node(records, 4, 10)
        try:
            pickle.dump(self.model, open(serialized_file_name, "wb"))
        except:
            pass


    # def create_visualization_from_df(df):
    #     ggplot(df, aes(x=('open', 'close', 'high'), fill='cut'))
    #     geom_density(alpha = .25) +\
    #     facet_wrap('clarity')

    def analyze_data(self):
        if not self.filename:
            return

        if not self.model:
            return

        df = pandas.read_csv(self.filename)
        applied_df = pandas.concat([df, df.apply(self.model.predict, axis = 1)], axis=1)
        print(applied_df.values.tolist())
        self.create_table_from_list([list(applied_df) + ["Chance of being viable"]] + applied_df.values.tolist())
        # Pass into implementation
        # predicted_df = implementation(df)

        # predicted_list = predicted_df.values.tolist()
        # self.create_table_from_list(predicted_list)
        # self.create_visualization_from_df(df)


    def create_table_from_list(self, data):
        if self.table_f:
            self.table_f.destroy()

        nrow = len(data) if len(data) < 40 else 40
        ncol = len(data[1])
        self.table_f = Frame(self.content_wrapper, bg='black')
        # self.table_f.pack()
        self.table_f.grid(row=0, column=0, sticky='nsew')
        for row in range(nrow):
            for col in range(ncol):
                label = Label(self.table_f, text=data[row][col]) if not (row == 0 and col == ncol - 1) else Label(self.table_f, text="Confidence in viability")
                label.grid(row=row, column=col, sticky='nsew', padx=1, pady=1, ipadx=1, ipady=1)
            # predicted_text = "Yes" if row > 0 else "Predicted to be viable?"
            # label = Label(self.table_f, text=predicted_text)
            # label.grid(row=row, column = ncol, sticky='nsew', padx=1, pady=1, ipadx=1, ipady=1)


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
