def ApplyPC1(my_list):
    """ Applies the PC1 permutation to the given list of length 64.
    Discards parity check bits, returns a list of length 56.
    """
    pc1_map = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42,
               34, 26, 18, 10, 2, 59, 51, 43, 35, 27,
               19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39,
               31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
               14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20,
               12, 4]
    new_list  = []
    for i,elem in enumerate(my_list):
        if (i+1)%8 != 0:
            new_list.append(elem)
    tmp = [i for i in range(64)]
    for i,elem in enumerate(new_list):
        new_index = pc1_map[i] - 1
        tmp[new_index] = elem
    to_return = []
    for i, elem in enumerate(tmp):
        if (i+1)%8 != 0:
            to_return.append(tmp[i])
    return to_return


def ApplyPC2(my_list):
    """ Applies the PC2 permutation to the given list of length 56.
    Returns a list of length 48.    
    """
    tmp = [-1 for i in range(56)]
    pc2_map = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23,
                19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52,
                31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44,
                49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
    for i,elem in enumerate(pc2_map):
        tmp[i] = my_list[pc2_map[i] - 1]
    to_return = []
    for elem in tmp:
        if elem > -1:
            to_return.append(elem)
    return to_return


def DESApplyP(my_list):
    """ Applies the permutation as defined by P to the given
    list of length 32. Returns a list of length 32.
    """
    p = [15, 6, 19, 20, 28, 11, 27, 16, 0, 14, 22, 25, 4, 17, 30, 9,
         1, 7, 23, 13, 31, 26, 2, 8, 18, 12, 29, 5, 21, 10, 3, 24]
    return [my_list[index] for index in p]


def DESKeySchedule(key):
    """ Generates the key schedule for a given key of length 64.
    Returns a list of length 16 where each element of the list is 
    a list of length 48 representing a subkey in the key schedule.
    """
    
    def LeftShift(my_list, i):
        """ Shifts the given list i places to the left.
        """
        LS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
        shift_amt = LS[i]
        return my_list[shift_amt:] + my_list[:shift_amt]
    
    pc1 = ApplyPC1(key)
    y = (pc1[:28], pc1[28:])
    key_schedule = []
    for i in range(16):
        c_i = LeftShift(y[0], i)
        d_i = LeftShift(y[1], i)
        y = (c_i, d_i)
        key_schedule.append(ApplyPC2(c_i + d_i))
    return key_schedule


def DESCipherFunction(R, sub_key):
    """ Executes the round function on the provided R (of length 32)
    with the provided subkey. Returns a list of length 32.
    """
    def expand(my_list):
        """ Expands the provided list of length 32 to a list of
        length 48 as defined by E.
        """
        E = [32,   1,   2,   3,   4,   5,
              4,   5,   6,   7,   8,   9,
              8,   9,  10,  11,  12,  13,
             12,  13,  14,  15,  16,  17,
             16,  17,  18,  19,  20,  21,
             20,  21,  22,  23,  24,  25,
             24,  25,  26,  27,  28,  29,
             28,  29,  30,  31,  32,   1]
        return [my_list[index-1] for index in E]
    
    y = expand(R)
    y = [str(y[i] ^ sub_key[i]) for i in range(len(y))]
    b1, b2, b3, b4, b5, b6, b7, b8 = (y[:6], y[6:12], y[12:18], y[18:24], y[24:30], y[30:36], y[36:42], y[42:48])
    def s(b, i):
        """ Passes the provided block b of length 6 through the ith S_box.
        Returns a list of length 4.
        """
        b = ''.join(b)
        s_boxes = {1:
                    [[14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
                     [ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
                     [ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
                     [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13]],
                  2:
                    [[15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
                     [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
                     [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
                     [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9]],
                  3:
                    [[10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
                     [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
                     [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
                     [ 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12]],
                  4:
                    [[ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
                     [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
                     [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
                     [ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14]],
                  5:
                    [[ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
                     [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
                     [ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
                     [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3]],
                  6:
                    [[12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
                     [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
                     [ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
                     [ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13]],
                  7:
                    [[ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
                     [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],
                     [ 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
                     [ 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12]],
                  8:
                    [[13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
                     [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
                     [ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
                     [ 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11]]}
        
        
        row = int(str(b[0]) + str(b[-1]), 2)
        column = int(str(b[1:-1]), 2)
        to_return = bin(s_boxes[i][row][column])[2:].zfill(4)
        return to_return
    
    z = s(b1, 1) + s(b2, 2) + s(b3, 3) + s(b4, 4) + s(b5, 5) + s(b6, 6) + s(b7, 7) + s(b8, 8)
    to_return = [0 for i in range(32)]
    P = [16,   7,  20,  21,
         29,  12,  28,  17,
          1,  15,  23,  26,
          5,  18,  31,  10,
          2,   8,  24,  14,
         32,  27,   3,   9,
         19,  13,  30,   6,
         22,  11,   4,  25]
    for i, elem in enumerate(P):
        to_return[i] = z[elem-1]
    return to_return
     

def DES(msg, key):
    """ Performs the DES encryption algorithm on the provided message
    of length 64 with the provided key of length 64. Outputs a ciphertext
    of length 64.
    """
    key_schedule = DESKeySchedule(key)
    IP = [58,  50,  42,  34,  26,  18,  10,   2,
      60,  52,  44,  36,  28,  20,  12,   4,
      62,  54,  46,  38,  30,  22,  14,   6,
      64,  56,  48,  40,  32,  24,  16,   8,
      57,  49,  41,  33,  25,  17,   9,   1,
      59,  51,  43,  35,  27,  19,  11,   3,
      61,  53,  45,  37,  29,  21,  13,   5,
      63,  55,  47,  39,  31,  23,  15,   7]
    
    x = [msg[IP[i]-1] for i in range(64)]
    
    L = x[:32]
    R = x[32:]
    for i in range(16):
        L_next = R
        round_function = DESCipherFunction(R, key_schedule[i])
        R = [int(L[j]) ^ int(round_function[j]) for j in range(32)]
        L = L_next
    x = R + L
    IP_INVERSE = [40,   8,  48,  16,  56,  24,  64,  32,
                  39,   7,  47,  15,  55,  23,  63,  31,
                  38,   6,  46,  14,  54,  22,  62,  30,
                  37,   5,  45,  13,  53,  21,  61,  29,
                  36,   4,  44,  12,  52,  20,  60,  28,
                  35,   3,  43,  11,  51,  19,  59,  27,
                  34,   2,  42,  10,  50,  18,  58,  26,
                  33,   1,  41,   9,  49,  17,  57,  25]
    return [x[IP_INVERSE[i]-1] for i in range(64)]