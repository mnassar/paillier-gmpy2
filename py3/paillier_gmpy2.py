'''
Created on Feb 25, 2014

@author: NASSAR
'''
import random, sys 
from primes_gmpy2 import *

from gmpy2 import mpz, powmod, invert, is_prime, random_state, mpz_urandomb, rint_round, log2, gcd 

rand=random_state(random.randrange(sys.maxsize))

class PrivateKey(object):
    def __init__(self, p, q, n):
        self.l = (p-1) * (q-1)
        self.m = invert(self.l, n)

class PublicKey(object):
    def __init__(self, n):
        self.n = n
        self.n_sq = n * n
        self.g = n + 1
        self.bits=mpz(rint_round(log2(self.n)))

def generate_keypair(bits):
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    n = p * q
    return PrivateKey(p, q, n), PublicKey(n)

def encrypt(pub, plain):
    while True:
        r=mpz_urandomb(rand, pub.bits)
        if r > 0 and r < pub.n and gcd(r,pub.n)==1:
            break
#        else: 
#            print r
# for sufficiently large pub.bits comment the previous while True loop and uncomment the following line 
#    r=mpz_urandomb(rand, pub.bits)
    x = powmod(r, pub.n, pub.n_sq)
    cipher = (powmod(pub.g, plain, pub.n_sq) * x) % pub.n_sq
    return cipher

def e_add(pub, a, b):
    """Add one encrypted integer to another"""
    return a * b % pub.n_sq

def e_add_const(pub, a, n):
    """Add constant n to an encrypted integer"""
    return a * powmod(pub.g, n, pub.n_sq) % pub.n_sq

def e_mul_const(pub, a, n):
    """Multiplies an encrypted integer by a constant"""
    return powmod(a, n, pub.n_sq)

def decrypt(priv, pub, cipher):
    x = powmod(cipher, priv.l, pub.n_sq) - 1
    plain = ((x // pub.n) * priv.m) % pub.n
    return plain

if __name__ == '__main__':
    priv, pub = generate_keypair(10)
    print(pub.n) 
