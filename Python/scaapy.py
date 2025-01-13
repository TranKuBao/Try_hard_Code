from scapy.all import *

pcap = rdpcap("D:\TryHardCode\Python\capture.pcap")
print(pcap)
flag=[]
for p in pcap[UDP]:
    try:
        if p[IP].src=='10.0.0.2' and p[IP].dst=='10.0.0.12':
            print(p[Raw].load)
            flag.append(p[Raw].load.decode("utf-8"))
    except:
        continue

print("".join(flag))