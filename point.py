from curve import EC
from helpers import mod_inv


class AffinePoint:
    def __init__(self, x, y):
        self.curve = EC

        self.x = x % self.curve.p
        self.y = y % self.curve.p

        if not self.on_curve():
            raise Exception('Point is not on the given curve.')

    def on_curve(self):
        return (self.y ** 2) % self.curve.p == \
               (self.x ** 3 + self.curve.a * self.x + self.curve.b) % self.curve.p

    def __str__(self):
        return f'({self.x};{self.y})'

    def to_projective(self):
        return ProjectivePoint(self.x, self.y, 1)


class ProjectivePoint:
    def __init__(self, x, y, z=1):
        self.curve = EC

        self.x = x % self.curve.p
        self.y = y % self.curve.p
        self.z = z % self.curve.p

        if not self.on_curve():
            raise Exception('Point is not on the given curve.')

    def on_curve(self):
        return (self.y**2 * self.z) % self.curve.p == \
               (self.x**3 + self.curve.a * self.x * self.z**2 + self.curve.b * self.z**3) % self.curve.p

    def __str__(self):
        return f'({self.x};{self.y};{self.z})'

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.z == other.z and self.curve == other.curve:
            return True
        else:
            return False

    def __add__(self, other):

        if self == ProjectivePoint(0, 1, 0):
            return other
        if other == ProjectivePoint(0, 1, 0):
            return self

        U1 = other.y * self.z
        U2 = self.y * other.z
        V1 = other.x * self.z
        V2 = self.x * other.z

        if V1 == V2:
            if U1 != U2:
                return ProjectivePoint(0, 1, 0)
            else:
                return self.PointDouble()

        U = U1 - U2
        V = V1 - V2
        W = self.z * other.z
        A = U**2 * W - V**3 - 2 * V**2 * V2

        return ProjectivePoint(V * A, U * (V**2 * V2 - A) - V**3 * U2, V**3 * W)

    def __mul__(self, n):
        res = ProjectivePoint(0, 1, 0)
        temp = self

        while n != 0:
            if n & 1 != 0:
                res += temp
            temp = temp.PointDouble()
            n >>= 1

        return res

    def PointDouble(self):

        if self.y == 0 or self == ProjectivePoint(0, 1, 0):
            return ProjectivePoint(0, 1, 0)

        W = self.curve.a * self.z**2 + 3 * self.x**2
        S = self.y * self.z
        B = self.x * self.y * S
        H = W**2 - 8 * B

        return ProjectivePoint(2 * H * S, W * (4 * B - H) - 8 * self.y**2 * S**2, 8 * S**3)

    def to_affine(self):
        if self == ProjectivePoint(0, 1, 0) or self.z == 0:
            return 'Point at infinity.'

        mi = mod_inv(self.z, self.curve.p)

        return AffinePoint(self.x * mi, self.y * mi)
