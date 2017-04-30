import pickle


def load_data(path):
    with open(path, 'rb') as infile:
        return pickle.load(infile)
