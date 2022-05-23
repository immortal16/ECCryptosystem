# ECCryptosystem

Contains classic cryptosystems on elliptic curves: Diffie-Hellman key exchange, directional encryption protocol and El-Gamal digital signature scheme.

## Including

- params - set of parameters of the P-192 curve from ECDSA;
- helpers - EGCD and modular multiplicative inverse;
- curve - elliptic curve class;
- point - affine and projective point classes (contains all arithmetic operations);
- customAES - redefined AES for string input and output instead of bytes;
- system - (contains all functionality described above);
- main - proof of correctness of all parts with the P-192 curve.
