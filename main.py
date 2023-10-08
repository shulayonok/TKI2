import numpy as np


# Перевод алфавита в кодировку ASCII
def alphabet_to_byte(alph):
    return " ".join(f"{ord(i.encode('cp1251')):08b}" for i in alph)


# Формирует «сдвинутый» на n-k позиций информационный многочлен
def form_inform_polynom(M, n, k):
    result = []
    for m in M:
        res = '0' * (n - k) + m
        result.append(res)
        print(np.poly1d(np.array([i for i in reversed(res)], dtype=int)))
    return result


# Находит остаток от деления этого многочлена на порождающий многочлен
def residual(M, g):
    result = []
    g_arr = np.array([i for i in reversed(g)], dtype=int)
    for m in M:
        res = np.polydiv(np.array([i for i in reversed(m)], dtype=int), g_arr)
        result.append(''.join(map(str, np.array(np.abs(res[1][::-1] % 2), dtype=int))))
        print(np.poly1d(np.array(np.abs(res[1] % 2), dtype=int)))
    return result


# Формирует кодовый многочлен
def form_code_polynom(M, residuals):
    result = []
    for j in range(len(alphabet)):
        res = np.polyadd(np.array([i for i in reversed(M[j])], dtype=int),
                         np.array([i for i in reversed(residuals[j])], dtype=int))
        print(np.poly1d(res))
        result.append(''.join(map(str, np.array(np.abs(res[::-1] % 2), dtype=int))))
    return result


# Вносит одиночную ошибку
def generate_error(M):
    errors = np.random.randint(0, 13, 7)
    err_codes = []
    for j, k in zip(M, errors):
        code = list(j)
        code[k] = (int(code[k]) + 1) % 2
        code = ''.join(map(str, code))
        err_codes.append(code)
        print(f'{j} | {code}')
    return err_codes


alphabet = "РСТУФ"
alphaBytes = alphabet_to_byte(alphabet).split(" ")
g = '100101'
print("Вывод алфавита с кодировке win 1251")
print(alphaBytes)
print()
shift_polynoms = form_inform_polynom(alphaBytes, 13, 8)
print(shift_polynoms)
print()
residuals = residual(shift_polynoms, g)
print(residuals)
print()
code_polynoms = form_code_polynom(shift_polynoms, residuals)
print(code_polynoms)
print()
error_codes = generate_error(code_polynoms)
syndroms = residual(error_codes, g)
print()
print(syndroms)
