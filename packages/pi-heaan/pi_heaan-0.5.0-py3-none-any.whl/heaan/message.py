
import copy
import numpy as np
import pickle
from typing import Union

Number = Union[int, float]

class Message:

    def __init__(self, data: list=[]):
        self._data = np.array([complex(slot) for slot in data])

    def __repr__(self):
        return repr(np.array([data.real for data in self._data]))
    
    def __len__(self):
        return len(self._data)

    def __getitem__(self, index: int):
        return self._data[index].real

    def __setitem__(self, index: int, value: Number):
        self._data[index] = complex(value)

    def load(self, path):
        with open(path, 'rb') as f:
            tmp = pickle.load(f)
        self.copy(tmp)
        pass

    def save(self, context, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)
        pass

    def copy(self, src):
        self._data = copy.deepcopy(src._data)
