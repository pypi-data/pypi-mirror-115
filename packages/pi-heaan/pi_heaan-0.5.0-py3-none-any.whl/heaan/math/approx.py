
import math
import heaan
from heaan import (
    HomEvaluator,
    PublicKeyPack,
    Ciphertext,
)

def sign(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt_in: Ciphertext,
    ctxt_out: Ciphertext,
    n1: int=7,
    n2: int=4
):
    coeffs = [315, -420, 378, -180, 35]
    coeffs_g = [5850/1024, -34974/1024, 97015/1024, -113492/1024, 46623/1024]
    degree = len(coeffs) - 1
    cost_per_iter = 6

    ctxt_tmp1, ctxt_tmp2 = heaan.Ciphertext(), heaan.Ciphertext()
    ctxt_pows = [heaan.Ciphertext() for _ in range(degree+1)]

    if ctxt_in is not ctxt_out:
        ctxt_out.copy(ctxt_in)
    
    conj_key = keypack.get_conj_key()

    for idx in range(n1):
        __check_level_and_bootstrap(eval, keypack, ctxt_out, ctxt_out, cost_per_iter)
            
        ctxt_pows[0] = ctxt_out
        eval.mult(ctxt_pows[0], ctxt_pows[0], keypack, ctxt_pows[1])

        for j in range(2, degree+1):
            if j%2 == 0:
                eval.mult(ctxt_pows[j//2], ctxt_pows[j//2], keypack, ctxt_pows[j])
            else:
                eval.mult(ctxt_pows[j//2], ctxt_pows[j//2+1], keypack, ctxt_pows[j])
        
        eval.mult(ctxt_pows[1], coeffs_g[1], ctxt_tmp1)
        for j in range(2, degree+1):
            eval.mult(ctxt_pows[j], coeffs_g[j], ctxt_tmp2)
            eval.add(ctxt_tmp1, ctxt_tmp2, ctxt_tmp1)
        eval.add(ctxt_tmp1, coeffs_g[0], ctxt_tmp1)
        eval.mult(ctxt_tmp1, ctxt_pows[0], keypack, ctxt_out)
        eval.kill_imag(ctxt_out, conj_key, ctxt_out)

    for _ in range(n2):
        __check_level_and_bootstrap(eval, keypack, ctxt_out, ctxt_out, cost_per_iter)
            
        ctxt_pows[0] = ctxt_out
        eval.mult(ctxt_pows[0], ctxt_pows[0], keypack, ctxt_pows[1])

        for j in range(2, degree+1):
            if j%2 == 0:
                eval.mult(ctxt_pows[j//2], ctxt_pows[j//2], keypack, ctxt_pows[j])
            else:
                eval.mult(ctxt_pows[j//2], ctxt_pows[j//2+1], keypack, ctxt_pows[j])
        
        eval.mult(ctxt_pows[1], coeffs[1], ctxt_tmp1)
        for j in range(2, degree+1):
            eval.mult(ctxt_pows[j], coeffs[j], ctxt_tmp2)
            eval.add(ctxt_tmp1, ctxt_tmp2, ctxt_tmp1)
        eval.add(ctxt_tmp1, coeffs[0], ctxt_tmp1)
        eval.mult(ctxt_tmp1, 1/128, ctxt_tmp1)
        eval.mult(ctxt_tmp1, ctxt_pows[0], keypack, ctxt_out)
        eval.kill_imag(ctxt_out, conj_key, ctxt_out)
    pass

def sign_shallow(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt: Ciphertext,
    n1: int,
    n2: int
):
    coeffs = [35/16, -35/16, 21/16, -5/16]
    coeffs_g = [4589/1024, -16577/1024, 25614/1024, -12860/1024]
    degree = len(coeffs) - 1
    cost_per_iter = 5

    ctxt_tmp = heaan.Ciphertext()
    ctxt_pows = [heaan.Ciphertext() for _ in range(2*degree+2)]

    for idx in range(n1):
        __check_level_and_bootstrap(eval, keypack, ctxt, ctxt, cost_per_iter)

        ctxt_pows[1] = ctxt

        for j in range(2, 2*degree):
            if j%2 == 0:
                eval.mult(ctxt_pows[j//2], ctxt_pows[j//2], keypack, ctxt_pows[j])
            else:
                eval.mult(ctxt_pows[j//2], ctxt_pows[j//2+1], keypack, ctxt_pows[j])
        
        l = 2*degree + 1
        eval.mult(ctxt_pows[l//2], ctxt_pows[l//2+1], keypack, ctxt_pows[l])
        eval.mult(ctxt_pows[1], coeffs_g[0], ctxt)

        for j in range(1, degree+1):
            eval.mult(ctxt_pows[2*j+1], coeffs_g[j], ctxt_tmp)
            eval.add(ctxt, ctxt_tmp, ctxt)
    
    for idx in range(n2):
        __check_level_and_bootstrap(eval, keypack, ctxt, ctxt, cost_per_iter)

        ctxt_pows[1] = ctxt

        for j in range(2, 2*degree):
            if j%2 == 0:
                eval.mult(ctxt_pows[j//2], ctxt_pows[j//2], keypack, ctxt_pows[j])
            else:
                eval.mult(ctxt_pows[j//2], ctxt_pows[j//2+1], keypack, ctxt_pows[j])
        
        l = 2*degree + 1
        eval.mult(ctxt_pows[l//2], ctxt_pows[l//2+1], keypack, ctxt_pows[l])
        eval.mult(ctxt_pows[1], coeffs[0], ctxt)

        for j in range(1, degree+1):
            eval.mult(ctxt_pows[2*j+1], coeffs[j], ctxt_tmp)
            eval.add(ctxt, ctxt_tmp, ctxt)
    pass

def inverse(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt_in: Ciphertext,
    ctxt_out: Ciphertext,
    n: int=18,
    m: int=20
):
    cost_per_iter = 1

    ctxt_in_neg, ctxt_tmp0, ctxt_tmp1 = heaan.Ciphertext(), heaan.Ciphertext(), heaan.Ciphertext()

    conj_key = keypack.get_conj_key()

    if ctxt_in is not ctxt_out:
        ctxt_out.copy(ctxt_in)
    
    eval.mult(ctxt_in, 1/pow(2, 44), ctxt_tmp0)

    eval.negate(ctxt_in, ctxt_in_neg)
    __check_level_and_bootstrap(eval, keypack, ctxt_in_neg, ctxt_in_neg, cost_per_iter)
    
    eval.mult(ctxt_in, 1/pow(2, 22), ctxt_out)
    eval.negate(ctxt_out, ctxt_out)
    eval.add(ctxt_out, 1, ctxt_out)

    for _ in range(m):
        __check_level_and_bootstrap(eval, keypack, ctxt_out, ctxt_out, cost_per_iter)        
        eval.mult(ctxt_out, ctxt_out, keypack, ctxt_out)
    
    eval.sub(ctxt_out, ctxt_tmp0, ctxt_out)
    eval.add(ctxt_out, pow(2, -21), ctxt_out)

    cost_per_iter = 3
    
    for _ in range(n):
        __check_level_and_bootstrap(eval, keypack, ctxt_out, ctxt_out, cost_per_iter)        
        eval.mult(ctxt_in_neg, ctxt_out, keypack, ctxt_tmp1)
        eval.add(ctxt_tmp1, 2, ctxt_tmp1)
        eval.mult(ctxt_tmp1, ctxt_out, keypack, ctxt_out)
        eval.kill_imag(ctxt_out, conj_key, ctxt_out)
    pass

def sqrt_inverse(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt_in: Ciphertext,
    ctxt_out: Ciphertext,
    y0: float=1.6,
    num_iter: int=20
):
    cost_per_iter = 5

    conj_key = keypack.get_conj_key()

    if ctxt_in.get_level() - cost_per_iter < ctxt_in.get_min_level_for_bootstrap():
        eval.bootstrap(ctxt_in, keypack, ctxt_in)

    ctxt_x, ctxt_y = heaan.Ciphertext(), heaan.Ciphertext()
    ctxt_tmp1, ctxt_tmp2 = heaan.Ciphertext(), heaan.Ciphertext()

    ctxt_x.copy(ctxt_in)

    for i in range(num_iter+1):

        if i==0:
            eval.mult(ctxt_x, y0*y0, ctxt_tmp1)
        else:
            if ctxt_y.get_level() - cost_per_iter < ctxt_y.get_min_level_for_bootstrap()+1:
                eval.mult(ctxt_y, 1/32, ctxt_y)
                eval.bootstrap(ctxt_y, keypack, ctxt_y)
                eval.mult(ctxt_y, 1<<5, ctxt_y)
            eval.mult(ctxt_y, ctxt_y, keypack, ctxt_tmp1)
            eval.mult(ctxt_x, ctxt_tmp1, keypack, ctxt_tmp1)

        eval.negate(ctxt_tmp1, ctxt_tmp1)
        eval.add(ctxt_tmp1, 3, ctxt_tmp1)
        eval.mult(ctxt_tmp1, 0.5, ctxt_tmp1)

        if i==0:
            eval.mult(ctxt_tmp1, y0, ctxt_y)
        else:
            eval.mult(ctxt_tmp1, ctxt_y, keypack, ctxt_y)
        eval.kill_imag(ctxt_y, conj_key, ctxt_y)
    
    ctxt_out.copy(ctxt_y)

    if ctxt_out.get_level() - 5 < ctxt_out.get_min_level_for_bootstrap():
        eval.bootstrap(ctxt_out, keypack, ctxt_out)
    pass


def sqrt_inverse_large(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt_in: Ciphertext,
    ctxt_out: Ciphertext,
    y0: float=2**(-9),
    num_iter: int=20
):
    cost_per_iter = 5

    conj_key = keypack.get_conj_key()
    
    if ctxt_in.get_level() - cost_per_iter < ctxt_in.get_min_level_for_bootstrap():
        eval.bootstrap(ctxt_in, keypack, ctxt_in)

    ctxt_x, ctxt_y = heaan.Ciphertext(), heaan.Ciphertext()
    ctxt_tmp1, ctxt_tmp2 = heaan.Ciphertext(), heaan.Ciphertext()

    ctxt_x.copy(ctxt_in)

    for i in range(num_iter+1):

        if i==0:
            eval.mult(ctxt_x, y0*y0, ctxt_tmp1)
        else:
            if ctxt_y.get_level() - cost_per_iter < ctxt_y.get_min_level_for_bootstrap()+1:
                eval.mult(ctxt_y, 1/32, ctxt_y)
                eval.bootstrap(ctxt_y, keypack, ctxt_y)
                eval.mult(ctxt_y, 1<<5, ctxt_y)
            eval.mult(ctxt_y, ctxt_y, keypack, ctxt_tmp1)
            eval.mult(ctxt_x, ctxt_tmp1, keypack, ctxt_tmp1)

        eval.negate(ctxt_tmp1, ctxt_tmp1)
        eval.add(ctxt_tmp1, 3, ctxt_tmp1)
        eval.mult(ctxt_tmp1, 0.5, ctxt_tmp1)

        if i==0:
            eval.mult(ctxt_tmp1, y0, ctxt_y)
        else:
            eval.mult(ctxt_tmp1, ctxt_y, keypack, ctxt_y)
        eval.kill_imag(ctxt_y, conj_key, ctxt_y)
    
    ctxt_out.copy(ctxt_y)

    if ctxt_out.get_level() - 5 < ctxt_out.get_min_level_for_bootstrap():
        eval.bootstrap(ctxt_out, keypack, ctxt_out)

    pass


def compare(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt1: Ciphertext,
    ctxt2: Ciphertext,
    ctxt_out: Ciphertext,
    n1: int=7,
    n2: int=4
):
    ctxt_tmp = heaan.Ciphertext()
    eval.sub(ctxt1, ctxt2, ctxt_tmp)
    sign(eval, keypack, ctxt_tmp, ctxt_out, n1, n2)
    eval.add(ctxt_out, 1, ctxt_out)
    eval.mult(ctxt_out, 0.5, ctxt_out)

    if ctxt_out.get_level() - 5 < ctxt_out.get_min_level_for_bootstrap():
        eval.bootstrap(ctxt_out, keypack, ctxt_out)
    pass

def minmax(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt1: Ciphertext,
    ctxt2: Ciphertext,
    ctxt_min: Ciphertext,
    ctxt_max: Ciphertext
):
    ctxt_tmp = heaan.Ciphertext()
    compare(eval, keypack, ctxt1, ctxt2, ctxt_tmp)

    if ctxt_tmp.get_level() - 2 < ctxt_tmp.get_min_level_for_bootstrap():
        eval.bootstrap(ctxt_tmp, keypack, ctxt_tmp)
    if ctxt1.get_level() - 1 < ctxt1.get_min_level_for_bootstrap():
        eval.bootstrap(ctxt1, keypack, ctxt1)
    if ctxt2.get_level() - 1 < ctxt2.get_min_level_for_bootstrap():
        eval.bootstrap(ctxt2, keypack, ctxt2)


    ctxt1_max = heaan.Ciphertext()
    ctxt1_min = heaan.Ciphertext()
    ctxt2_max = heaan.Ciphertext()
    ctxt2_min = heaan.Ciphertext()
    eval.mult(ctxt1, ctxt_tmp, keypack, ctxt1_max)
    eval.sub(ctxt1, ctxt1_max, ctxt1_min)
    eval.mult(ctxt2, ctxt_tmp, keypack, ctxt2_min)
    eval.sub(ctxt2, ctxt2_min, ctxt2_max)

    eval.add(ctxt1_max, ctxt2_max, ctxt_max)
    eval.add(ctxt1_min, ctxt2_min, ctxt_min)
    

def compare_shallow(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt1: Ciphertext,
    ctxt2: Ciphertext,
    ctxt_out: Ciphertext,
    n1: int,
    n2: int
):
    eval.sub(ctxt1, ctxt2, ctxt_out)
    sign_shallow(eval, keypack, ctxt_out, n1, n2)
    eval.add(ctxt_out, 1, ctxt_out)
    eval.mult(ctxt_out, 1/2, ctxt_out)
    pass

def sqrt(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt_in: Ciphertext,
    ctxt_out: Ciphertext,
    num_iter: int=20
):
    cost_per_iter = 2

    ctxt_tmp1, ctxt_tmp2 = heaan.Ciphertext(), heaan.Ciphertext()

    if ctxt_in is not ctxt_out:
        ctxt_out.copy(ctxt_in)

    eval.sub(ctxt_in, 1, ctxt_tmp1)

    for idx in range(num_iter):
        if ctxt_tmp1.get_level() - 3 < ctxt_tmp1.get_min_level_for_bootstrap():
            eval.bootstrap(ctxt_tmp1, keypack, ctxt_tmp1)
        if ctxt_out.get_level() - 3 < ctxt_out.get_min_level_for_bootstrap():
            eval.bootstrap(ctxt_out, keypack, ctxt_out)

        eval.mult(ctxt_tmp1, 0.5, ctxt_tmp2)
        eval.negate(ctxt_tmp2, ctxt_tmp2)
        eval.add(ctxt_tmp2, 1, ctxt_tmp2)
        eval.mult(ctxt_out, ctxt_tmp2, keypack, ctxt_out)

        eval.sub(ctxt_tmp1, 3, ctxt_tmp2)
        eval.mult(ctxt_tmp2, 0.25, ctxt_tmp2)
        eval.mult(ctxt_tmp1, ctxt_tmp1, keypack, ctxt_tmp1)
        eval.mult(ctxt_tmp1, ctxt_tmp2, keypack, ctxt_tmp1)

    if ctxt_out.get_level() - 5 < ctxt_out.get_min_level_for_bootstrap():
        eval.bootstrap(ctxt_out, keypack, ctxt_out)
    pass

def discrete_equal_zero(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt_in: Ciphertext,
    ctxt_out: Ciphertext
):
    scale_factor = 6
    cost_per_iter = 9

    sinc_coeffs = [1, 0, -1/6, 0, 1/120]
    cos_coeffs  = [1, 0, -1/2, 0, 1/24]
    degree = len(sinc_coeffs) - 1

    ctxt_x, ctxt_sinc, ctxt_cos, ctxt_tmp = heaan.Ciphertext(), heaan.Ciphertext(), heaan.Ciphertext(), heaan.Ciphertext()
    ctxt_pows = [heaan.Ciphertext() for _ in range(degree+1)]

    ctxt_x.copy(ctxt_in)
    __check_level_and_bootstrap(eval, keypack, ctxt_x, ctxt_x, cost_per_iter)

    eval.mult(ctxt_x, 201, ctxt_x)
    eval.mult(ctxt_x, 1/4096, ctxt_x)
    
    ctxt_pows[1].copy(ctxt_x)
    for idx in range(2, degree+1):
        if idx % 2 == 0:
            eval.mult(ctxt_pows[idx//2], ctxt_pows[idx//2], keypack, ctxt_pows[idx])
        else:
            eval.mult(ctxt_pows[idx//2], ctxt_pows[idx//2+1], keypack, ctxt_pows[idx])
    
    eval.mult(ctxt_pows[1], sinc_coeffs[1], ctxt_tmp)
    ctxt_sinc.copy(ctxt_tmp)
    for idx in range(2, degree+1):
        eval.mult(ctxt_pows[idx], sinc_coeffs[idx], ctxt_tmp)
        eval.add(ctxt_sinc, ctxt_tmp, ctxt_sinc)
    eval.add(ctxt_sinc, sinc_coeffs[0], ctxt_sinc)

    eval.mult(ctxt_pows[1], cos_coeffs[1], ctxt_tmp)
    ctxt_cos.copy(ctxt_tmp)
    for idx in range(2, degree+1):
        eval.mult(ctxt_pows[idx], cos_coeffs[idx], ctxt_tmp)
        eval.add(ctxt_cos, ctxt_tmp, ctxt_cos)
    eval.add(ctxt_cos, cos_coeffs[0], ctxt_cos)

    for idx in range(scale_factor):
        eval.mult(ctxt_sinc, ctxt_cos, keypack, ctxt_sinc)
        eval.mult(ctxt_cos, ctxt_cos, keypack, ctxt_cos)
        eval.mult(ctxt_cos, 2, ctxt_cos)
        eval.add(ctxt_cos, -1, ctxt_cos)

    eval.sub(ctxt_sinc, 0.5, ctxt_out)
    sign(eval, keypack, ctxt_out, ctxt_out, 2)
    eval.add(ctxt_out, 1, ctxt_out)
    eval.mult(ctxt_out, 0.5, ctxt_out)
    pass

def discrete_equal(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt1: Ciphertext,
    ctxt2: Ciphertext,
    ctxt_out: Ciphertext
):
    ctxt_tmp = heaan.Ciphertext()
    eval.sub(ctxt1, ctxt2, ctxt_tmp)
    discrete_equal_zero(eval, keypack, ctxt_tmp, ctxt_out)
    pass

def relu(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt_in: Ciphertext,
    ctxt_out: Ciphertext
):
    coeffs = [0.033, 0.5, 1.479, 0, -3.202, 0, 3.839, 0, -1.663]

    ctxt2, ctxt4, ctxt_tmp = heaan.Ciphertext(), heaan.Ciphertext(), heaan.Ciphertext()

    eval.mult(ctxt_in, coeffs[1], ctxt_out)
    eval.add(ctxt_out, coeffs[0], ctxt_out)

    eval.mult(ctxt_in, ctxt_in, keypack, ctxt2)
    eval.mult(ctxt2, coeffs[2], ctxt_tmp)
    eval.add(ctxt_out, ctxt_tmp, ctxt_out)

    eval.mult(ctxt2, ctxt2, keypack, ctxt4)
    eval.mult(ctxt4, coeffs[4], ctxt_tmp)
    eval.add(ctxt_out, ctxt_tmp, ctxt_out)

    eval.mult(ctxt2, ctxt4, keypack, ctxt_tmp)
    eval.mult(ctxt_tmp, coeffs[6], ctxt_tmp)
    eval.add(ctxt_out, ctxt_tmp, ctxt_out)

    eval.mult(ctxt4, ctxt4, keypack, ctxt_tmp)
    eval.mult(ctxt_tmp, coeffs[8], ctxt_tmp)
    eval.add(ctxt_out, ctxt_tmp, ctxt_out)
    pass

def sigmoid(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt_in: Ciphertext,
    ctxt_out: Ciphertext
):
    bound = 8
    cost_per_iter = 5

    coeffs = [0.5, -1.73496, 0, 4.19407, 0, -5.43402, 0, 2.50739]
    degree = len(coeffs) - 1

    conj_key = keypack.get_conj_key()
    
    ctxt_tmp = heaan.Ciphertext()
    ctxt_pows = [heaan.Ciphertext() for _ in range(degree+1)]

    ctxt_pows[1].copy(ctxt_in)
    __check_level_and_bootstrap(eval, keypack, ctxt_in, ctxt_pows[1], cost_per_iter)
    
    eval.mult(ctxt_pows[1], 2**(-math.log2(bound)), ctxt_pows[1])

    for idx in range(2, degree+1):
        if idx % 2 == 0:
            eval.mult(ctxt_pows[idx//2], ctxt_pows[idx//2], keypack, ctxt_pows[idx])
        else:
            eval.mult(ctxt_pows[idx//2], ctxt_pows[idx//2+1], keypack, ctxt_pows[idx])
    
    eval.mult(ctxt_pows[1], coeffs[1], ctxt_out)
    for idx in range(2, degree+1):
        if abs(coeffs[idx] < 1e-10): continue
        eval.mult(ctxt_pows[idx], coeffs[idx], ctxt_tmp)
        eval.add(ctxt_out, ctxt_tmp, ctxt_out)
    eval.add(ctxt_out, coeffs[0], ctxt_out)
    eval.negate(ctxt_out, ctxt_out)
    eval.add(ctxt_out, 1, ctxt_out)

    eval.kill_imag(ctxt_out, conj_key, ctxt_out)
    pass

def sigmoid_wide(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt_in: Ciphertext,
    depth: int,
    ctxt_out: Ciphertext
):
    bound = 14.5
    eps = 2.45**-depth
    div = 1.0 / 6.0025**depth
    cost_per_iter = 3

    ctxt_y = heaan.Ciphertext(ctxt_in)

    eval.mult(ctxt_y, 1.0/bound, ctxt_y)

    for _ in range(depth+1):
        if ctxt_y.get_level() - cost_per_iter < ctxt_y.get_min_level_for_bootstrap():
            eval.mult(ctxt_y, eps, ctxt_y)
            eval.bootstrap(ctxt_y, keypack, ctxt_y)
            eval.mult(ctxt_y, 1/eps, ctxt_y)
        
        ctxt_y = __auxilary_func_B(eval, keypack, ctxt_y, div)
        div *= 6.0025
    
    __minimax_sigmoid(eval, keypack, ctxt_y, ctxt_out, bound)
    pass


def __auxilary_func_B(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt_in: Ciphertext,
    div: float
):
    ctxt_out, ctxt2 = heaan.Ciphertext(), heaan.Ciphertext()
    
    coeff = -4 * div / 27
    eval.mult(ctxt_in, ctxt_in, keypack, ctxt2)
    eval.mult(ctxt_in, coeff, ctxt_out)
    eval.mult(ctxt2, ctxt_out, keypack, ctxt_out)
    eval.add(ctxt_in, ctxt_out, ctxt_out)

    return ctxt_out
    pass


def __minimax_sigmoid(eval: HomEvaluator,
    keypack: PublicKeyPack, 
    ctxt_in: Ciphertext, 
    ctxt_out: Ciphertext, 
    multiplier: float
):
    cost_per_iter = 5

    coeffs = [0.5, 0.1939, 0, -4.813e-3, 0, 5.992e-5, 0, -3.232e-7, 0, 6.195e-10]
    degree = len(coeffs) - 1
    norm = 16

    for idx in range(1, degree+1):
        coeffs[idx] *= multiplier**idx

    ctxt_x, ctxt_tmp = heaan.Ciphertext(), heaan.Ciphertext()
    ctxt2, ctxt3, ctxt4 = heaan.Ciphertext(), heaan.Ciphertext(), heaan.Ciphertext()
    ctxt5, ctxt7, ctxt9 = heaan.Ciphertext(), heaan.Ciphertext(), heaan.Ciphertext()

    ctxt_x.copy(ctxt_in)
    if ctxt_x.get_level() - cost_per_iter < ctxt_x.get_min_level_for_bootstrap():
        eval.mult(ctxt_x, 1/2**4, ctxt_x)
        eval.bootstrap(ctxt_x, keypack, ctxt_x)
        eval.mult(ctxt_x, norm, ctxt_x)
    
    eval.mult(ctxt_x, coeffs[1], ctxt_out)

    eval.mult(ctxt_x, ctxt_x, keypack, ctxt2)
    eval.mult(ctxt_x, coeffs[3], ctxt_tmp)
    eval.mult(ctxt2, ctxt_tmp, keypack, ctxt3)
    eval.add(ctxt_out, ctxt3, ctxt_out)

    eval.mult(ctxt2, coeffs[5]/coeffs[3], ctxt_tmp)
    eval.mult(ctxt3, ctxt_tmp, keypack, ctxt5)
    eval.add(ctxt_out, ctxt5, ctxt_out)

    eval.mult(ctxt2, ctxt2, keypack, ctxt4)
    eval.mult(ctxt_x, coeffs[7], ctxt_tmp)
    eval.mult(ctxt2, ctxt_tmp, keypack, ctxt_tmp)
    eval.mult(ctxt4, ctxt_tmp, keypack, ctxt7)
    eval.add(ctxt_out, ctxt7, ctxt_out)

    eval.mult(ctxt2, ctxt3, keypack, ctxt5)
    eval.mult(ctxt4, coeffs[9]/coeffs[3], ctxt_tmp)
    eval.mult(ctxt5, ctxt_tmp, keypack, ctxt9)
    eval.add(ctxt_out, ctxt9, ctxt_out)
    eval.add(ctxt_out, coeffs[0], ctxt_out)
    pass

def __check_level_and_bootstrap(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt_in: Ciphertext,
    ctxt_out: Ciphertext,
    cost_per_iter: int
):
    if ctxt_in.get_level() - cost_per_iter < ctxt_in.get_min_level_for_bootstrap():
        eval.bootstrap(ctxt_in, keypack, ctxt_out)
    pass
