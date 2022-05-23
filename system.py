import random as rn

from customAES import AESC
from hashlib import sha256
from helpers import mod_inv, int_to_bytes


class System:
    def __init__(self, ec, basis_point):
        self.curve = ec
        self.point = basis_point
        self.hash = lambda x: int(sha256(bytes(x, 'utf-8')).hexdigest(), 16)

        self.d = rn.randint(2, self.curve.n + 1)
        self.Q = self.point * self.d

    def extractKeys(self):
        return [self.d, self.Q]

    def getSharedSecret(self, public):
        return (public * self.d).to_affine().x

    @staticmethod
    def wrap(key, shared_secret):
        c = AESC(int_to_bytes(shared_secret))
        return c.encrypt(key)

    @staticmethod
    def unwrap(encrypted_key, shared_secret):
        c = AESC(int_to_bytes(shared_secret))
        return c.decrypt(encrypted_key)

    @staticmethod
    def _encrypt(message, key):
        c = AESC(bytes(key, 'utf-8'))
        return c.encrypt(message)

    def encrypt(self, message, public):
        key = 'get_random_bytes'

        Cm = self._encrypt(message, key)

        eA = rn.randint(2, self.curve.n + 1)
        QA = self.point * eA

        Sx = (public * eA).to_affine().x

        Ck = self.wrap(key, Sx)

        return QA, Ck, Cm

    @staticmethod
    def _decrypt(encrypted_message, key):
        c = AESC(bytes(key, 'utf-8'))
        return c.decrypt(encrypted_message)

    def decrypt(self, encrypted):
        QA, Ck, Cm = encrypted

        Sx = (QA * self.d).to_affine().x

        key = self.unwrap(Ck, Sx)

        return self._decrypt(Cm, key)

    def sign(self, message):
        h = self.hash(message)

        k = rn.randint(2, self.curve.n + 1)
        W = self.point * k
        r = W.to_affine().x % self.curve.n

        while r == 0:
            k = rn.randint(2, self.curve.n + 1)
            W = self.point * k
            r = W.to_affine().x % self.curve.n

        s = (mod_inv(k, self.curve.n) * (h + self.d * r)) % self.curve.n

        return [r, s]

    def verify(self, message, signed, public):
        r, s = signed

        h = self.hash(message)

        u1 = (mod_inv(s, self.curve.n) * h) % self.curve.n
        u2 = (mod_inv(s, self.curve.n) * r) % self.curve.n

        W = self.point * u1 + public * u2

        v = W.to_affine().x % self.curve.n

        return True if v == r else False
