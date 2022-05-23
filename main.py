from curve import EC
from point import ProjectivePoint
from system import System

x, y = EC.get_random_point()
P = ProjectivePoint(x, y)

Alice = System(EC, P)
Bobbi = System(EC, P)

_, QA = Alice.extractKeys()
_, QB = Bobbi.extractKeys()

#######################################################################################################################

print('\nTask 1\n')

s1 = Alice.getSharedSecret(QB)
s2 = Bobbi.getSharedSecret(QA)

print('shared secret identical =', s1 == s2)

#######################################################################################################################

print('\nTask 2\n')

encr1 = Alice.encrypt('elliptic', QB)
print('decrypted text1 =', Bobbi.decrypt(encr1))
encr2 = Bobbi.encrypt('curves', QA)
print('decrypted text2 =', Alice.decrypt(encr2))

#######################################################################################################################

print('\nTask 2\n')

message = 'signature'

signed = Alice.sign(message)
verified = Bobbi.verify(message, signed, QA)
print('verified =', verified)
