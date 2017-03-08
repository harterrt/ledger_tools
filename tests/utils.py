import pickle
import datetime

def load_data(path):
    with open(path, 'rb') as infile:
        return pickle.load(infile)
