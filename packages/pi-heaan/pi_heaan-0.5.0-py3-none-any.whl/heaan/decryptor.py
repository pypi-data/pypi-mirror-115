
import copy
import numpy as np
from heaan import Context, Message, Ciphertext, SecretKey

class Decryptor:

    def __init__(self, context: Context):
        self._context = context
        pass

    def decrypt(self, ciphertext: Ciphertext, secret_key: SecretKey, message: Message):
        message._data = copy.deepcopy(ciphertext._data)
        self._context._update_op_history('decrypt   ')
        pass
    