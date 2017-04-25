def pr(x, m=None, step=4):
    """ Helper function for displaying bit strings nicely.
    """
    s = ''
    if m:
        s += '{}:\n'.format(m)
    for i, elem in enumerate(x):
        s += str(elem)
        if i%step == step-1:
            s += ' '
    print(s)

def perm(x, p):
    """ Applies the permutation p on list x.
    """
    return [x[elem] for elem in p]

__pc1 = [56, 48, 40, 32, 24, 16, 8,
		  0, 57, 49, 41, 33, 25, 17,
		  9, 1, 58, 50, 42, 34, 26,
		 18, 10, 2, 59, 51, 43, 35,
		 62, 54, 46, 38, 30, 22, 14,
		  6, 61, 53, 45, 37, 29, 21,
		 13, 5, 60, 52, 44, 36, 28,
		 20, 12, 4, 27, 19, 11, 3]

__left_rotations = [
    1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
]

__pc2 = [
    13, 16, 10, 23,  0,  4,
        2, 27, 14,  5, 20,  9,
    22, 18, 11,  3, 25,  7,
    15,  6, 26, 19, 12,  1,
    40, 51, 30, 36, 46, 54,
    29, 39, 50, 44, 32, 47,
    43, 48, 38, 55, 33, 52,
    45, 41, 49, 35, 28, 31
]

__ip = [57, 49, 41, 33, 25, 17, 9,  1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7,
    56, 48, 40, 32, 24, 16, 8,  0,
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6
]

__expansion_table = [
    31,  0,  1,  2,  3,  4,
        3,  4,  5,  6,  7,  8,
        7,  8,  9, 10, 11, 12,
    11, 12, 13, 14, 15, 16,
    15, 16, 17, 18, 19, 20,
    19, 20, 21, 22, 23, 24,
    23, 24, 25, 26, 27, 28,
    27, 28, 29, 30, 31,  0
]

S = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

__p = [
    15, 6, 19, 20, 28, 11,
    27, 16, 0, 14, 22, 25,
    4, 17, 30, 9, 1, 7,
    23,13, 31, 26, 2, 8,
    18, 12, 29, 5, 21, 10,
    3, 24
]

__ip_inverse = [
    39,  7, 47, 15, 55, 23, 63, 31,
    38,  6, 46, 14, 54, 22, 62, 30,
    37,  5, 45, 13, 53, 21, 61, 29,
    36,  4, 44, 12, 52, 20, 60, 28,
    35,  3, 43, 11, 51, 19, 59, 27,
    34,  2, 42, 10, 50, 18, 58, 26,
    33,  1, 41,  9, 49, 17, 57, 25,
    32,  0, 40,  8, 48, 16, 56, 24
]

def left_shift(x, step):
    """ Performs a left shift the specified number of steps on
    the provided list x.
    """
    return x[step:] + x[:step]

def get_key_schedule(k):
    """ Gets the key schedule for the provided key k. Returns a list
    of 16 elements, each of length 48.
    """
    key_schedule = []
    Kp = perm(K, __pc1)
    C = Kp[:len(Kp)//2]
    D = Kp[len(Kp)//2:]
    for i,shift in enumerate(__left_rotations):
        C_next = left_shift(C, shift)
        D_next = left_shift(D, shift)
        key_schedule.append(perm(C_next + D_next, __pc2))
        C = C_next
        D = D_next

    return key_schedule

def elementwise_xor(a, b):
    """ Performs xor on each element in the lists a and b.
    Lists must be of equal length. Returns an equivalent length
    list.
    """
    assert len(a) == len (b)
    return [a[i] ^ b[i] for i in range(len(a))]

def f(R, sub_key):
    """ The round function as specified by DES.
    """
    expanded = perm(R, __expansion_table)
    res = elementwise_xor(sub_key, expanded)
    Bs = [''.join([str(x) for x in res[i:i+6]]) for i in range(0, len(res), 6)]
    Ss = []
    for i,B in enumerate(Bs):
        row, col = int(B[0] + B[-1], 2), int(B[1:-1], 2)
        Ss.append(format(S[i][row][col], '04b'))
    Ss = ''.join(Ss)
    return perm([int(s) for s in Ss], __p)

def DES_encrypt(msg, key):
    """ The main encryption method. Encrypts the provided message
    with the given key according to DES. Outputs a cipertext of length 64.
    """
    key_schedule = get_key_schedule(key)
    x = perm(msg, __ip)
    L = x[:len(x)//2]
    R = x[len(x)//2:]
    for i in range(16):
        L_next = R
        R = elementwise_xor(L, f(R, key_schedule[i]))
        L = L_next
    return perm(R + L, __ip_inverse)

def DES_decrypt(ciphertext, key):
    """ The decryption algorithm. Decrypts the provided ciphertext
    with the given key according to DES. Outputs a plaintext of length 64.
    """
    key_schedule = get_key_schedule(key)
    x = perm(ciphertext, __ip)
    R = x[:len(x)//2]
    L = x[len(x)//2:]
    for i in reversed(range(16)):
        R_next = L
        L = elementwise_xor(R, f(R_next, key_schedule[i]))
        R = R_next
    return perm(L + R, __ip_inverse)
M = [0,0,0,0,0,0,0,1,0,0,1,0,
     0,0,1,1,0,1,0,0,0,1,0,1,
     0,1,1,0,0,1,1,1,1,0,0,0,
     1,0,0,1,1,0,1,0,1,0,1,1,
     1,1,0,0,1,1,0,1,1,1,1,0,
     1,1,1,1]

K = [0,0,0,1,0,0,1,1,
     0,0,1,1,0,1,0,0,
     0,1,0,1,0,1,1,1,
     0,1,1,1,1,0,0,1,
     1,0,0,1,1,0,1,1,
     1,0,1,1,1,1,0,0,
     1,1,0,1,1,1,1,1,
     1,1,1,1,0,0,0,1]
correct_ciphertext = [1,0,0,0,0,1,0,1,
                      1,1,1,0,1,0,0,0,
                      0,0,0,1,0,0,1,1,
                      0,1,0,1,0,1,0,0,
                      0,0,0,0,1,1,1,1,
                      0,0,0,0,1,0,1,0,
                      1,0,1,1,0,1,0,0,
                      0,0,0,0,0,1,0,1]
ciphertext = DES_encrypt(M, K)
assert ciphertext == correct_ciphertext
deciphered = DES_decrypt(ciphertext, K)
assert deciphered == M
pr(M, '\noriginal plaintext')
pr(ciphertext, '\nciphertext')
pr(deciphered, '\ndeciphered text')