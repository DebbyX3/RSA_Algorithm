import sympy
import random

generatorNotFound = True

#find large prime: almeno 10^100 ma per noi è troppo grande quindi ne prendo uno + piccolo

INIT_RANGE_PRIME = 10**5
END_RANGE_PRIME = 10**20

q = sympy.randprime(INIT_RANGE_PRIME, END_RANGE_PRIME)

q = 761
qTotient = q-1
primeFactors = sympy.primefactors(qTotient)
expToTest = [(qTotient)/factor for factor in primeFactors]

while(generatorNotFound):
    candidateGenerator = random.randint(2, q) # forse q-1?
    print(candidateGenerator)

    for exp in expToTest:
        residual = int(int(candidateGenerator)**int(exp)) % q
        print(residual)
        if residual == 1:  
            break

    if residual != 1:
        generatorNotFound = False

g = candidateGenerator

print(q, qTotient, primeFactors, expToTest, g)

x = random.randint(1, q-1)

y = (int(g)**int(x)) % q

print(x, y)

#chiavi pubbliche: g y q
#chiave privata: x

#cifratura
#voglio cifrare il numero 23
numToEnc = 23 % q

r =  random.randint(1, q-1)
c1 = (int(g)**int(r)) % q
c2 = (int(numToEnc) * (int(y)**int(r))) % q

print(numToEnc, c1, c2)

#decry CHE NON FUNZIONA!

s = int(c1)**int(x)
sinverse = int(s)**int(q-x)
m = (c2 * sinverse)
print(m)

'''
randint(a, b)
Return a random integer N such that a <= N <= b.

One way to do this, if you're working with a multiplicative group Z∗p, is to pick a prime p so that p−1 has a large prime factor q; 
once you have this, then to generate a generator of order q, you pick a random value h, compute g=h(p−1)/q, and if that is not 1, 
then g is a generator of your group.
https://crypto.stackexchange.com/questions/22716/generation-of-a-cyclic-group-of-prime-order

prima risp
https://math.stackexchange.com/questions/124408/finding-a-primitive-root-of-a-prime-number


https://cp-algorithms.com/algebra/primitive-root.html#:~:text=First%2C%20find%20ϕ(n),g%20is%20a%20primitive%20root.

https://www.researchgate.net/publication/309268648_A_Novice's_Perception_of_Partial_Homomorphic_Encryption_Schemes

https://it.wikipedia.org/wiki/ElGamal

https://www.slideshare.net/ayyakathir/cryptography-and-network-security-52030389 slide 19

https://mathstats.uncg.edu/sites/pauli/112/HTML/secelgamal.html
'''