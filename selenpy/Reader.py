import pickle
import json

class Loader:

    def read_pkl(path=None, mode="rb"):
        
        if path:
            with open(path, mode) as f:
                data = pickle.load(f)
        else:
            with open("config/tasks.pkl", "rb") as f:
                data = pickle.load(f)

        if type(data) != list:
            raise TypeError("Input tasks must be a list object")

        return data

    def read_json(path):

        with open(path, "r") as f:
            data = json.load(f)

        return data
