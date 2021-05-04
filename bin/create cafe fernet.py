from cryptography.fernet import Fernet
import pickle
import datetime
import os  
  
# generate a key for encryption and decryption
# You can use fernet to generate 
# the key or use random key generator
# here I'm using fernet to generate key
  
key = Fernet.generate_key()
  
# Instance the Fernet class with the key
print(f'{key}')
with open("key.pickle", "wb") as pickle_out:
	pickle.dump(key, pickle_out)