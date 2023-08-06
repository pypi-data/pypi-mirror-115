
import copy
import numpy as np
from typing import Union

from numpy.lib.arraysetops import isin
from heaan import (
    Ciphertext,
    Message,
    PublicKeyPack,
    RelinearlizationKey,
    RotationKey,
    Encryptor,
    ConjugationKey,
    Context,
)

class HomEvaluator:

    def __init__(self, context: Context):
        self._context = context
        pass

    def negate(self,
            ctxt: Ciphertext,
            ctxt_out: Ciphertext):

        self.mult(ctxt, -1, ctxt_out)
        pass

    def add(self,
            operand1: Ciphertext,
            operand2: Union[Ciphertext, Message, float],
            ctxt_out: Ciphertext):

        if not isinstance(operand1, Ciphertext):
            raise TypeError("Invalid type of operand1..")
        if not isinstance(operand2, (Ciphertext, Message, float, int)):
            raise TypeError("Invalid type of operand2..")
        if not isinstance(ctxt_out, Ciphertext):
            raise TypeError("Invalid type of ctxt_out..")

        if isinstance(operand2, (Ciphertext, Message)):
            if isinstance(operand2, Ciphertext):
                if operand1.get_level() < operand2.get_level():
                    target_level = operand1.get_level()
                    tmp_ctxt = Ciphertext()
                    self.level_down(operand2, target_level, tmp_ctxt)
                    self.add(operand1, tmp_ctxt, ctxt_out)
                    return
                elif operand1.get_level() > operand2.get_level():
                    target_level = operand2.get_level()
                    tmp_ctxt = Ciphertext()
                    self.level_down(operand1, target_level, tmp_ctxt)
                    self.add(tmp_ctxt, operand2, ctxt_out)
                    return
            self.check_parameter(operand1, operand2)
        
        if operand1 is not ctxt_out:
            ctxt_out._level = operand1.get_level()
            ctxt_out._number_of_slots = operand1.get_number_of_slots()

        with np.errstate(all='ignore'):
            if isinstance(operand2, (Ciphertext, Message)):
                ctxt_out._data = operand1._data + operand2._data
                self._context._update_op_history('add       ')
            else:
                ctxt_out._data = operand1._data + operand2
                self._context._update_op_history('add_const ')
        pass

    def sub(self,
            operand1: Ciphertext,
            operand2: Union[Ciphertext, Message, float],
            ctxt_out: Ciphertext):

        if not isinstance(operand1, Ciphertext):
            raise TypeError("Invalid type of operand1..")
        if not isinstance(operand2, (Ciphertext, Message, float, int)):
            raise TypeError("Invalid type of operand2..")
        if not isinstance(ctxt_out, Ciphertext):
            raise TypeError("Invalid type of ctxt_out..")

        if isinstance(operand2, Ciphertext) or isinstance(operand2, Message):
            if isinstance(operand2, Ciphertext):
                if operand1.get_level() < operand2.get_level():
                    target_level = operand1.get_level()
                    tmp_ctxt = Ciphertext()
                    self.level_down(operand2, target_level, tmp_ctxt)
                    self.sub(operand1, tmp_ctxt, ctxt_out)
                    return
                elif operand1.get_level() > operand2.get_level():
                    target_level = operand2.get_level()
                    tmp_ctxt = Ciphertext()
                    self.level_down(operand1, target_level, tmp_ctxt)
                    self.sub(tmp_ctxt, operand2, ctxt_out)
                    return
            self.check_parameter(operand1, operand2)
        
        if operand1 is not ctxt_out:
            ctxt_out._level = operand1.get_level()
            ctxt_out._number_of_slots = operand1.get_number_of_slots()

        with np.errstate(all='ignore'):
            if isinstance(operand2, (Ciphertext, Message)):
                ctxt_out._data = operand1._data - operand2._data
                self._context._update_op_history('sub       ')
            else:
                ctxt_out._data = operand1._data - operand2
                self._context._update_op_history('sub_const ')
        pass

    def mult(self,
            operand1: Ciphertext,
            operand2: Union[Ciphertext, Message, float],
            *args):

        if not isinstance(operand1, Ciphertext):
            raise TypeError("Invalid type of operand1..")
        if not isinstance(operand2, (Ciphertext, Message, float, int)):
            raise TypeError("Invalid type of operand2..")

        if isinstance(operand2, Ciphertext):
            if len(args) != 2:
                raise IndexError("Invalid number of inputs...")
            if not isinstance(args[0], PublicKeyPack) and not isinstance(args[0], RelinearlizationKey):
                raise TypeError("Invalid type of input...")
            if not isinstance(args[1], Ciphertext):
                raise TypeError("Invalid type of ctxt_out..")
            
            key = args[0]
            ctxt_out = args[1]

            if not isinstance(ctxt_out, Ciphertext):
                raise TypeError("Invalid type of ctxt_out..")

            if operand1.get_level() < operand2.get_level():
                target_level = operand1.get_level()
                tmp_ctxt = Ciphertext()
                self.level_down(operand2, target_level, tmp_ctxt)
                self.mult(operand1, tmp_ctxt, key, ctxt_out)
                return
            elif operand1.get_level() > operand2.get_level():
                target_level = operand2.get_level()
                tmp_ctxt = Ciphertext()
                self.level_down(operand1, target_level, tmp_ctxt)
                self.mult(tmp_ctxt, operand2, key, ctxt_out)
                return
            self.check_parameter(operand1, operand2)
        else:
            if len(args) != 1:
                raise IndexError("Invalid number of inputs...")
                
            ctxt_out = args[0]
            
            if not isinstance(ctxt_out, Ciphertext):
                raise TypeError("Invalid type of ctxt_out..")

            if isinstance(operand2, Message):
                self.check_parameter(operand1, operand2)
        
        if operand1 is not ctxt_out:
            ctxt_out._number_of_slots = operand1.get_number_of_slots()

        self.level_down(ctxt_out, operand1.get_level() - 1, ctxt_out)
        self.check_level(ctxt_out)

        with np.errstate(all='ignore'):
            if isinstance(operand2, Ciphertext):
                ctxt_out._data = operand1._data * operand2._data
                self._context._update_op_history('mult      ')
            elif isinstance(operand2, Message):
                ctxt_out._data = operand1._data * operand2._data
                self._context._update_op_history('mult_msg  ')
            else:
                ctxt_out._data = operand1._data * operand2
                self._context._update_op_history('mult_const')
        pass

    def left_rotate(self,
            ctxt: Ciphertext,
            rot_idx: int,
            key: Union[PublicKeyPack, RotationKey],
            ctxt_out: Ciphertext):

        if not isinstance(ctxt, Ciphertext):
            raise TypeError("Invalid type of ctxt_in..")
        if not isinstance(rot_idx, int):
            raise TypeError("Invalid type of rot_idx..")
        if not isinstance(key, PublicKeyPack) and not isinstance(key, RotationKey):
            raise TypeError("Invalid type of keypack..")
        if not isinstance(ctxt_out, Ciphertext):
            raise TypeError("Invalid type of ctxt_out..")
        if isinstance(key, RotationKey) and not key.get_evaluation_key_id()==rot_idx:
            raise TypeError("rot idx and rotation key id is not same")

        ctxt_out._level = ctxt.get_level()
        ctxt_out._number_of_slots = ctxt.get_number_of_slots()

        if rot_idx == 0:
            ctxt_out._data = ctxt._data.copy()
            return

        num_slots = self._context.get_degree() >> 1
        if rot_idx > num_slots:
            rot_idx = int(rot_idx % num_slots)
        
        big_2 = 1
        while rot_idx > big_2:
            big_2 = big_2 << 1
        intermediate = (big_2 >> 1) + (big_2 >> 2)
        gap = rot_idx - intermediate

        if gap > 0:
            ctxt_out._data = np.concatenate((ctxt._data[big_2:], ctxt._data[:big_2]))
            self._context._update_op_history('rotate    ')

            idx = 1
            gap = big_2 - rot_idx
            while gap >= idx:
                if gap & idx:
                    ctxt_out._data = np.concatenate((ctxt_out._data[num_slots-idx:], ctxt_out._data[:num_slots-idx]))
                    self._context._update_op_history('rotate    ')
                idx = idx << 1
        else:
            ctxt_out._data = ctxt._data.copy()
            idx = 1
            while rot_idx >= idx:
                if rot_idx & idx:
                    ctxt_out._data = np.concatenate((ctxt_out._data[idx:], ctxt_out._data[:idx]))
                    self._context._update_op_history('rotate    ')
                idx = idx << 1
        pass

    def right_rotate(self,
            ctxt: Ciphertext,
            rot_idx: int,
            key: Union[PublicKeyPack, RotationKey],
            ctxt_out: Ciphertext):

        if not isinstance(ctxt, Ciphertext):
            raise TypeError("Invalid type of ctxt_in..")
        if not isinstance(rot_idx, int):
            raise TypeError("Invalid type of rot_idx..")
        if not isinstance(key, PublicKeyPack) and not isinstance(key, RotationKey):
            raise TypeError("Invalid type of keypack..")
        if not isinstance(ctxt_out, Ciphertext):
            raise TypeError("Invalid type of ctxt_out..")

        idx = (self._context.get_degree() >> 1) - rot_idx
        self.left_rotate(ctxt, idx, key, ctxt_out)
        pass

    def bootstrap(self,
            ctxt: Ciphertext,
            public_keypack: PublicKeyPack,
            ctxt_out: Ciphertext):

        if not isinstance(ctxt, Ciphertext):
            raise TypeError("Invalid type of ctxt_in..")
        if not isinstance(public_keypack, PublicKeyPack):
            raise TypeError("Invalid type of keypack..")
        if not isinstance(ctxt_out, Ciphertext):
            raise TypeError("Invalid type of ctxt_out..")

        if not self._context._is_bootstrappable:
            raise ValueError("Should be make_bootstrappable...")

        self.check_level(ctxt)

        if ctxt is not ctxt_out:
            ctxt_out.copy(ctxt)
        ctxt_out._level = 13
        
        self._context._update_op_history('bootstrap ')
        self._context._max_level_down = 29
        pass

    def kill_imag(self,
            ctxt: Ciphertext,
            conj_key: ConjugationKey,
            ctxt_out: Ciphertext):
        
        if ctxt is not ctxt_out:
            ctxt_out.copy(ctxt)
        pass

    def level_down(self,
            ctxt: Ciphertext,
            target_level: int,
            ctxt_out: Ciphertext):

        ctxt_out._number_of_slots = ctxt.get_number_of_slots()
        ctxt_out._data = ctxt._data.copy()

        ctxt_out._level = target_level
        self.check_level(ctxt_out)

        if self._context._max_level_down < self._context.get_depth() - ctxt._level:
            self._context._max_level_down = self._context.get_depth() - ctxt._level
        pass

    def check_parameter(self, operand1: Ciphertext, operand2: Union[Ciphertext, Message]):
        
        if isinstance(operand2, Ciphertext):
            if operand1.get_number_of_slots() != operand2.get_number_of_slots():
                raise ValueError("operands should be computed with same number of slots...")

            if operand1.get_level() != operand2.get_level():
                raise ValueError("operands should be computed with same level...")

        if isinstance(operand2, Message):
            if operand1.get_number_of_slots() != len(operand2):
                raise ValueError("operands should be computed with same number of slots...")
        pass

    def check_level(self, ctxt: Ciphertext):

        if ctxt.get_level() < ctxt.get_min_level_for_bootstrap():
            raise ValueError("level of ciphertext is too small for computation...")
        pass