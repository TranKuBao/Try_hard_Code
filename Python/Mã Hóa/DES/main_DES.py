
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]
#Hoan vi E (32->48bit)
E = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

#table S-Box
def tra_S_box(xxx):
    S1 = [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ]
    S2 = [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ]
    S3 = [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ]
    S4 = [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ]
    S5 = [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ]
    S6 = [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ]
    S7 = [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ]
    S8 = [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
    
    if xxx==1:
        return S1
    elif xxx==2:
        return S2
    elif xxx==3:
        return S3
    elif xxx==4:
        return S4
    elif xxx==5:
        return S5
    elif xxx==6:
        return S6
    elif xxx==7:
        return S7
    elif xxx==8:
        return S8
IP_1 = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]



# hoanvi P
P = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]
#PC1
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1,  58, 50, 42, 34, 26, 18,
    10, 2,  59, 51, 43, 35, 27,
    19, 11, 3,  60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7,  62, 54, 46, 38, 30, 22,
    14, 6,  61, 53, 45, 37, 29,
    21, 13, 5,  28, 20, 12, 4
]

#Shitfleft
LS_TABLE = [    1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

#function PC2 (48bit from 56bit)
PC2 = [14, 17, 11, 24, 1,  5,
       3,  28, 15, 6,  21, 10,
       23, 19, 12, 4,  26, 8,
       16, 7,  27, 20, 13, 2,
       41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53,
       46, 42, 50, 36, 29, 32]

#M='123456789abcdef' #mã hóa
M='85e813540f0ab405' #giải mã
InputKey='133457799BBCDFF1'

bitt= bin(int(InputKey,16))[2:]
if len(bitt)!=64:
    so0=64-len(bitt)
    while so0!=0:
        bitt='0'+bitt
        so0-=1

#16 key will save this
key_16=[]
#PC1
hoanviPC1=''
for k in range(56):
    xxx=PC1[k] - 1
    xx=bitt[xxx]
    hoanviPC1=hoanviPC1+xx

left=hoanviPC1[:28]
right=hoanviPC1[28:]

for shift in range(16):
    #leftshit
    number_shift_bit=LS_TABLE[shift]
    left=left[number_shift_bit:]+left[:number_shift_bit]
    right=right[number_shift_bit:]+right[:number_shift_bit]

    #Hoanvi PC2
    k=left+right
    hoanviPC2=""
    for i in range(48):
        xxx=PC2[i]-1
        xx=k[xxx]
        hoanviPC2=hoanviPC2+xx
    #Save KEY
    key_16.append(hoanviPC2)
    
###############Da TIm Khoa Xong
#bat dau ma hoa DES

#Hoanvi khoi tao IP
M=bin(int(M,16))[2:]
if len(M)!=64:
    while len(M)!=64:
        M="0"+M
        
hoanviIP=""
for i in range(64):
    x = IP[i] - 1  # Adjust index to match Python's 0-based indexing
    bit = M[x]
    hoanviIP=hoanviIP+bit
#chidoi nua trai va nua phai
L=hoanviIP[:32]
R=hoanviIP[32:]
for kiki in range(16):
    #ham F
    #ham E(from 32bit to 48bit)
    morongE=""
    for i in range(48):
        xxx=E[i]-1
        xx=R[xxx];
        morongE=morongE+xx

    #XOR with Key i
    
    #doi voi ENCRYP
    #keyi=key_16[kiki]
    
    # doi voi decryp (dao KHOA)
    keyi=key_16[-kiki-1] 
    xorkhoa=""
    for i in range(48):
        xxx=int(keyi[i]) ^ int(morongE[i])
        xorkhoa=xorkhoa+str(xxx)

    #Thay the hoan vi S-Box
    hoanviS_Box=""
    for xxx in range(8):
        k = xorkhoa[(xxx)*6:(xxx+1)*6] 
        hang= int((k[0]+k[5]),2)
        cot=int(k[1:5],2)
        xx=tra_S_box(xxx+1)
        zz=xx[hang][cot]
        zz=bin(zz)[2:]
        while len(zz)!=4:
            zz='0'+zz
        
        hoanviS_Box=hoanviS_Box+str(zz)

    #Hoanvi P
    hoanviP=""
    for i in range(32):
        xxx=P[i]-1
        xx=hoanviS_Box[xxx]
        hoanviP=hoanviP+xx
        
    #XOR with Li-1
    XORli_1=""
    for i in range(32):
        k=int(hoanviP[i]) ^ int(L[i])
        XORli_1=XORli_1+str(k)
    
    #GAN left, right for the next round 
    L=R
    R=XORli_1
    
#when finished 16 round is join togother
ciphertext=""
R=R+L
for i in range(64):
    xxx=IP_1[i]-1
    xx=R[xxx]
    ciphertext=ciphertext+str(xx)

print(hex(int(ciphertext,2))[2:])
