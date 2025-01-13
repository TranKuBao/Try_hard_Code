
with open("D:\\TryHardCode\\another\\enc","rb") as file:
    xxx=file.read()

string =xxx.decode("utf-8")
for i in string:
    print(hex(ord(i)).lstrip("0x"),end="")
