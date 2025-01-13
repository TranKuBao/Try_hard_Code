








# excute with KEY 128bit
#extend key K
Cipher_Key='2b7e151628aed2a6abf7158809cf4f3c'
plain_text='3243f6a8885a308d313198a2e0370734'

W=[]
P=[]
for i in range(0,4):
    xxx=Cipher_Key[int(i*8):int(i*8+8)]
    W.append(xxx)
    
for i in range(0,4):
    xxx=plain_text[int(i*8):int(i*8+8)]
    P.append(xxx)

# Addroundkey
Add=[]
for i in range(0,4):
    xxx=''
    for j in range(0,4):
        a=P[i]
        b=W[i]
        result=int(a[j],16) ^ int(b[j],16);
        print(hex(result))
        result=hex(result)[2:]
        xxx=xxx+str(result)
    Add.append(xxx)

for i in range(0,4):
    print(Add[i])



