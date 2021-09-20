import socket   
import pickle
from rsa import RSAEnc
 
s = socket.socket()        
print("ALICE - RSA Server")
print("ALICE - Socket successfully created")

port = 7894               

s.bind(('', port)) # this network
print ("ALICE - Socket binded to %s" %(port))
 
s.listen(5)    
print ("ALICE - Server is waiting for a request")           
 
while True: 
  c, addr = s.accept()    
  print('ALICE - Got connection from', addr)

  plaintext = input("\nWhat message do you want to send to BOB?\n")
  e = input("Insert the already known public key 'e':\n")
  n = input("Insert the already known public key 'n'\n")

  ciphertextToSend = RSAEnc(plaintext, e, n)
  ciphertextToSendData = pickle.dumps(ciphertextToSend) #used to send list in a socket

  print('\nALICE - Sending the ciphertext...')
  c.send(ciphertextToSendData)
  print('ALICE - Sended!')

  c.close()
  
  break