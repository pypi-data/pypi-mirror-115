import math
import heaan
from heaan import (
    HomEvaluator,
    PublicKeyPack,
    Ciphertext,
    Message
)
from heaan.math import approx


def sort(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt: Ciphertext,
    num_rows: int,
    ascend: bool,
    last_stage: bool
):
    n = max(num_rows, ctxt.get_number_of_slots())
    n_pow = 2 ** math.ceil(math.log2(n))
    start_idx = math.log2(n_pow) - 1 if last_stage else 0
    for idx in range(start_idx, math.ceil(math.log2(n_pow))):
        flip = not (idx == math.log2(n_pow) - 1)
        j = 2 ** idx
        while j >= 1:
            two_sort(eval, keypack, ctxt, j, 2**idx, flip, ascend)
            j //= 2
    pass

def two_sort(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt: Ciphertext,
    distance1: int,
    distance2: int,
    flip: bool,
    ascend: bool
):
    cost_per_iter = 5

    num_slots = ctxt.get_number_of_slots()
    mask = heaan.Message([0 for _ in range(num_slots)])
    for idx in range(num_slots):
        if (idx//distance1)%2 == 0: mask[idx] = 1
    
    approx.__check_level_and_bootstrap(eval, keypack, ctxt, ctxt, cost_per_iter)

    if flip: __flip_ctxt(eval, ctxt, distance2)

    ctxt_cmp = heaan.Ciphertext()
    __compare_for_sort(eval, keypack, ctxt, mask, distance1, ctxt_cmp)
    eval.bootstrap(ctxt_cmp, keypack, ctxt_cmp)

    ctxt_tmp1, ctxt_tmp2 = heaan.Ciphertext(), heaan.Ciphertext()
    eval.mult(ctxt, mask, ctxt_tmp1)
    eval.left_rotate(ctxt, distance1, keypack, ctxt)
    eval.mult(ctxt, mask, ctxt_tmp2)
    
    ctxt_sort1, ctxt_sort2 = heaan.Ciphertext(), heaan.Ciphertext()
    __two_sub_sort(eval, keypack, ctxt_tmp1, ctxt_tmp2, ctxt_cmp, ascend, ctxt_sort1, ctxt_sort2)
    __assemble_sort(eval, keypack, ctxt_sort1, ctxt_sort2, distance1, ctxt)

    if flip: __flip_ctxt(eval, ctxt, distance2)
    pass

def __flip_ctxt(eval: HomEvaluator,
    ctxt: Ciphertext,
    distance: int
):
    num_slots = ctxt.get_number_of_slots()
    mask1, mask2 = heaan.Message([0 for _ in range(num_slots)]), heaan.Message([0 for _ in range(num_slots)])
    for idx in range(num_slots):
        if (idx//(2*distance))%2 == 0: mask1[idx] = 1
        else: mask2[idx] = 1

    ctxt_tmp = heaan.Ciphertext()
    eval.mult(ctxt, mask1, ctxt_tmp)
    eval.mult(ctxt, -1, ctxt)
    eval.add(ctxt, 0.5, ctxt)
    eval.mult(ctxt, mask2, ctxt)
    eval.add(ctxt, ctxt_tmp, ctxt)
    pass

def __compare_for_sort(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt: Ciphertext,
    mask: Message,
    distance: int,
    ctxt_out: Ciphertext
):
    ctxt_rot = heaan.Ciphertext()
    eval.left_rotate(ctxt, distance, keypack, ctxt_rot)
    eval.mult(ctxt_rot, mask, ctxt_rot)
    approx.compare_shallow(eval, keypack, ctxt, ctxt_rot, ctxt_out, 6, 3)
    pass

def __two_sub_sort(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt_in1: Ciphertext,
    ctxt_in2: Ciphertext,
    ctxt_cmp: Ciphertext,
    ascend: bool,
    ctxt_out1: Ciphertext,
    ctxt_out2: Ciphertext
):
    if ascend:
        eval.sub(ctxt_in1, ctxt_in2, ctxt_out2)
        eval.mult(ctxt_cmp, ctxt_out2, keypack, ctxt_out2)
        eval.add(ctxt_out2, ctxt_in2, ctxt_out2)
        eval.add(ctxt_in1, ctxt_in2, ctxt_out1)
        eval.sub(ctxt_out1, ctxt_out2, ctxt_out1)
    else:
        eval.sub(ctxt_in1, ctxt_in2, ctxt_out1)
        eval.mult(ctxt_cmp, ctxt_out1, keypack, ctxt_out1)
        eval.add(ctxt_out1, ctxt_in2, ctxt_out1)
        eval.add(ctxt_in1, ctxt_in2, ctxt_out2)
        eval.sub(ctxt_out2, ctxt_out1, ctxt_out2)
    pass

def __assemble_sort(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt_in1: Ciphertext,
    ctxt_in2: Ciphertext,
    distance: int,
    ctxt_out: Ciphertext
):
    ctxt_out.copy(ctxt_in1)
    ctxt_tmp = heaan.Ciphertext()
    eval.right_rotate(ctxt_in2, distance, keypack, ctxt_tmp)
    eval.add(ctxt_out, ctxt_tmp, ctxt_out)
    pass
