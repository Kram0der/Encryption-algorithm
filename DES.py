import random


class DES:
    def __init__(self, ori_key):
        self._key = [[] for i in range(16)]
        key = self.ori_key_to_key(ori_key)
        for i in range(16):
            self._key[i] = self.key_to_child_key(i, key)

    _move = [1, 2, 4, 6, 8, 10, 12, 14, 15, 17, 19, 21, 23, 25, 27, 28]

    # 置换选择矩阵1
    _perm_matrix_before = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
                           10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
                           63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
                           14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]

    # 置换选择矩阵2
    _perm_matrix_after = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
                          23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
                          41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
                          44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

    # 初始置换矩阵
    _ip_matrix = [[58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
                   62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
                   57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
                   61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7],
                  [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
                   38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
                   36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
                   34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]]

    # 选择运算E矩阵
    _expand_e = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9,
                 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
                 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
                 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

    # 代替函数组
    s = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
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
          [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

    # 置换运算矩阵P
    _p = [16, 7, 20, 21, 29, 12, 28, 17,
          1, 15, 23, 26, 5, 18, 31, 10,
          2, 8, 24, 14, 32, 27, 3, 9,
          19, 13, 30, 6, 22, 11, 4, 25]

    # 置换选择1
    def ori_key_to_key(self, ori_key):
        key = [0] * 56
        matrix_change(ori_key, key, 56, self._perm_matrix_before)
        return key

    # 循环左移 + 置换选择2
    def key_to_child_key(self, m, key):
        def mov(a):
            i = self._move[m]
            if a > 55 - i or (27 - i < a < 28):
                return a - 28 + i
            else:
                return a + i

        child_key = [0] * 48
        for _ in range(48):
            child_key[_] = key[mov(self._perm_matrix_after[_] - 1)]
        return child_key

    # 选择运算E
    def expand(self, file):
        res = [0] * 48
        matrix_change(file, res, 48, self._expand_e)
        return res

    # 单轮加密函数
    def crypt(self, file, i):
        res = [0] * 32
        temp = self.expand(file)
        m = n = 0

        for _ in range(48):
            temp[_] ^= self._key[i][_]
        for _ in range(8):
            m = (temp[6 * _] << 1) + temp[6 * _ + 5]
            n = sum(temp[6 * _ + a] << (4 - a) for a in range(1, 5))
            for a in range(4):
                temp[a + 4 * _] = (self.s[_][m][n] >> (3 - a)) & 1
        matrix_change(temp, res, 32, self._p)
        return res

    # 初始置换+逆初始置换
    def ex_ip(self, file, i):
        res = [0] * 64
        matrix_change(file, res, 64, self._ip_matrix[i])
        return res


#  置换
def matrix_change(input, output, length, matrix):
    for _ in range(length):
        output[_] = int(input[matrix[_] - 1])


# flag: 加密 0 解密 1
def DES_CRYPT(ori_key, file, flag):
    arr = [range(16), range(15, -1, -1)]
    s = DES(ori_key)
    file_r = [int(x) for x in file]
    res = s.ex_ip(file_r, 0)
    l_list, r_list = res[:32], res[32:]

    for _ in arr[flag]:
        temp = s.crypt(r_list, _)
        for i in range(32):
            temp[i] ^= l_list[i]
        l_list = r_list
        r_list = temp
    f_list = r_list + l_list
    res = s.ex_ip(f_list, 1)
    return ''.join(str(i) for i in res)


def S_box(input):
    m = (input >> 4 & 2) | (input & 1)
    n = input >> 1 & 0xf
    return [DES.s[i][m][n] for i in range(4)]


if __name__ == '__main__':
    k = "0011000100110010001100110011010000110101001101100011011100111000"
    m = "0011000000110001001100100011001100110100001101010011011000110111"
    result = DES_CRYPT(k, m, 0)
    result0 = DES_CRYPT(k, result, 1)
    print(f'原信息为:{m}')
    print(f'加密后为:{result}')
    print(f'解密后为:{result0}')

    result = DES_CRYPT(k, m, 1)
    result0 = DES_CRYPT(k, result, 0)
    print(f'\n逆过程:\n原信息为:{m}')
    print(f'解密后为:{result}')
    print(f'加密后为:{result0}')
