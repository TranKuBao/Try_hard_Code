
import hashlib
from cryptography.fernet import Fernet
import base64
bUsername_trial = b"ANDERSON"
45326718
    
print(hashlib.sha256(bUsername_trial).hexdigest()[4])
print(hashlib.sha256(bUsername_trial).hexdigest()[5])
print(hashlib.sha256(bUsername_trial).hexdigest()[3])
print(hashlib.sha256(bUsername_trial).hexdigest()[6])
print(hashlib.sha256(bUsername_trial).hexdigest()[2])
print(hashlib.sha256(bUsername_trial).hexdigest()[7])
print(hashlib.sha256(bUsername_trial).hexdigest()[1])
print(hashlib.sha256(bUsername_trial).hexdigest()[8])