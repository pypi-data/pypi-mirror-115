
import copy
import numpy as np
import os
import pickle

class Ciphertext:

    def __init__(self, ctxt=None, number_of_primes: int=0, degree: int=0):
        if ctxt:
            self._level = ctxt._level
            self._number_of_slots = ctxt._number_of_slots
            self._number_of_primes = ctxt._number_of_primes
            self._degree = ctxt._degree
            self._data = copy.deepcopy(ctxt._data)
            self._in_device = ctxt._in_device
        else:
            self._level = 0
            self._number_of_slots = 0
            self._number_of_primes = number_of_primes
            self._degree = degree
            self._data = np.zeros(self._number_of_slots)
            self._in_device = False
    
    def __repr__(self):
        status = dict()
        status['level'] = self.get_level()
        status['num_slots'] = self.get_number_of_slots()
        return repr(status)

    def get_level(self):
        return self._level

    def get_min_level_for_bootstrap(self):
        return 4

    def get_number_of_slots(self):
        return self._number_of_slots

    def set_number_of_slots(self, number_of_slots):
        self._number_of_slots = number_of_slots

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
        self._level = src._level
        self._number_of_slots = src._number_of_slots
        self._number_of_primes = src._number_of_primes
        self._degree = src._degree
        self._data = copy.deepcopy(src._data)
        pass

    def to_device(self):
        self._in_device = True

    def to_host(self):
        self._in_device = False

    def in_device(self):
        return self._in_device

    def release(self):
        pass