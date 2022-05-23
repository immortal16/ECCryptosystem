def egcd(a, b):
    u, u1 = 1, 0
    v, v1 = 0, 1
    while b:
        q = a // b
        u, u1 = u1, u - q * u1
        v, v1 = v1, v - q * v1
        a, b = b, a - q * b
    return u, v, a


def mod_inv(a, m):
    u, v, g = egcd(a, m)
    return (u % m + m) % m


def solver(a, p):
    k = p - 3
    k //= 4
    ret = pow(a, k + 1, p)
    return ret


def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')