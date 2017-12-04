#!/usr/bin/env python3

import pandas as pandas
import pickle

from node import Node

serialized_file_name = 'trained_model.p'

def load_model():
    try:
        return pickle.load(open(serialized_file_name, "rb"))
    except:
        return None

model = load_model()

df = pandas.read_csv("coins.csv")
applied_df = pandas.concat([df, df.apply(model.predict, axis = 1)], axis=1)
applied_df.to_csv("coins_predicted.csv", encoding='utf-8', index=False)
