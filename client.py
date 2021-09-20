import socket            
import pickle
from rsa import RSADec

d = input("Insert the already known private key 'd':\n")
n = input("Insert the already known public key 'n'\n")

s = socket.socket()       
print("BOB - RSA Client")

port = 7894               
s.connect(('127.0.0.1', port))

print("BOB - Connected to port ", port)
print("BOB - Waiting for a ciphertext")

ciphertext = pickle.loads(s.recv(4096)) #used to receive list in a socket

print("BOB - Ciphertext receved")

RSADec(ciphertext, d, n)

print("\nBOB - Thank you!")
s.close()    