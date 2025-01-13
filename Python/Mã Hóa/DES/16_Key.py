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
    key_16.append(hex(int(hoanviPC2,2))[2:])
    