# RSA Algorithm

Implementation of the RSA asimmetric encryption algorithm. 

Currently generates up to 1096 bit keys

This project has three files:
* rsa.py - it contains the key generator and the functions used to encrypt and decrypt.
* server.py - it is the socket server that sends and encrypts a message. It could be seen as the principle Alice.
* client.py - it is the socket client that receives and decrypts a message. It could be seen as the principle Bob.

This implementation assumes that client and server had already exchanged the keys generated by rsa.py in a safe and secure environment, by first executing rsa.py.

## Pre-requisites

* python3
* sympy

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install sympy.

```bash
pip install sympy
```

## Usage

* Open a terminal and execute rsa.py
  ```bash
  python ./rsa.py
  ```
  Keep the newly generated keys (in particular: e, d, n keys) aside
* In a new terminal, execute server.py and keep it open on waiting
  ```bash
  python ./server.py
  ```
* In a new terminal, execute client.py
  ```bash
  python ./client.py
  ```
  Type the private key 'd' and the public key 'n' generated by rsa.py
* Once the client has connected, type a message in the server terminal to send to the client
* In the server terminal, type the public keys 'e' and 'n', generated by rsa.py
* Now the server sends the encrypted message to the client through the socket
* The client receives the message and decrypts it, revealing the original plaintext

All the transformations done to generate the keys, encrypt and decrypt are printed and shown.
  
Further explainations and implementation choiches are described and listed in the code itself.

## Author
Deborah Pintani - DebbyX3 (deborah.pintani@studenti.univr.it)