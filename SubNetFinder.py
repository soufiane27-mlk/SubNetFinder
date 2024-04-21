import sys
import math
import argparse

def ip2Binary(ip:str):
    return "".join(f"{int(i):08b}" for i in ip.split('.'))

def Binary2ip(binip:str):
    return '.'.join(str(int(binip[i*8:i*8+8],base=2)) for i in range(4))

def validate_ip(ip:str):
    ip_if_correct=ip
    try:
        ip=[int(i) for i in ip.split('.')]
        if len(ip)==4:
            for i in range(4):
                if 0<=ip[i]<256:
                    continue
                else:
                    raise ValueError("Invalid IP (or mask) address format. Expected: x.x.x.x ; 0 <= x < 256")
            return ip_if_correct
        else:     
            raise ValueError("Invalid IP (or mask) address format. Expected: x.x.x.x")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit()

def separate_ip(ip:str,mask:str):
    ip=ip2Binary(ip)
    mask=ip2Binary(mask)
    prefix=mask.count("1")
    networkAddr=ip[:prefix]+"0"*(32-prefix)
    NetPortion=networkAddr[:prefix]
    HostPortion=networkAddr[prefix:]
    return (HostPortion,NetPortion,prefix,networkAddr)

def NetInfo(ip:str,mask:str):
    infos=separate_ip(ip,mask)
    NetPortion=infos[1]
    HostPortion=infos[0]
    prefix=infos[2]
    networkAddr=infos[3]
    ip=ip2Binary(ip)
    mask=ip2Binary(mask)
    firstIP=NetPortion+f"{int(HostPortion)+1:0{32-prefix}}"
    broadcast=NetPortion+"1"*(32-prefix)
    lastIp=NetPortion+"1"*(31-prefix)+"0"
    MaxHosts=2**(len(HostPortion))-2
    print(f"\tNetwork address: {Binary2ip(networkAddr)}/{prefix}")
    print(f"\tBroadcast address: {Binary2ip(broadcast)}")
    print(f"\tFirst usable host: {Binary2ip(firstIP)}")
    print(f"\tLast usable host: {Binary2ip(lastIp)}")
    print(f"\tMax hosts: {MaxHosts:,}")

def subneting(ip,mask,subnets=2,onlyone=False,counter:int=0):
    infos=separate_ip(ip,mask)
    nbrsubBits=math.ceil(math.log(subnets)/math.log(2))
    prefix=infos[2] 
    if 32-prefix <= nbrsubBits:
        sys.exit()
    subnet_mask=Binary2ip("1"*(prefix+nbrsubBits)+"0"*(32-prefix-nbrsubBits))
    bin_bits=0
    for i in range(2**nbrsubBits):
        sub_netaddr=infos[1]+f"{bin_bits:0{nbrsubBits}b}"+"0"*(32-(prefix+nbrsubBits))
        print(f"subnet {i+1+counter}:\n")
        sub_netaddr=Binary2ip(sub_netaddr)
        NetInfo(sub_netaddr,subnet_mask)
        print("-_-"*15)
        onlyone-=1
        if onlyone==0:
            break
        bin_bits+=1
    sub_netaddr=infos[1]+f"{bin_bits+1:0{nbrsubBits}b}"+"0"*(32-(prefix+nbrsubBits))
    return (Binary2ip(sub_netaddr),subnet_mask)
             
def subneting_hosts(ip:str,mask:str,nbrHosts:int,onlyone=False,counter:int=0):
    infos=separate_ip(ip,mask)
    nbrsubBits=math.ceil(math.log(nbrHosts+2)/math.log(2))
    prefix=infos[2]
    if 32-prefix <= nbrsubBits:
        print("You can't subnet")
        sys.exit()
    nbrSub=32-prefix-nbrsubBits
    return subneting(ip,mask,2**nbrSub,onlyone,counter)

def subneting_hosts_per_network(ip:str,mask:str,NHPN:list):
    #NHPN : number of hosts per each network
    prefix=separate_ip(ip,mask)[2]
    NHPN=[2**math.ceil(math.log(hosts+2)/math.log(2)) for hosts in NHPN]
    if sum(NHPN)> 2**(32-prefix):
        print("You can't subnet")
        return False
    i=0
    while i<len(NHPN):
        ip,mask=subneting_hosts(ip,mask,NHPN[i]-2,NHPN.count(NHPN[i]),i)
        i+=NHPN.count(NHPN[i])
        
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('-i','--ipaddress',help="the ip address, the mask -m MASK or -p PREFIX should be specified")
    parser.add_argument('-m','--mask',help="the mask address, if the mask is not specified correctly the script will give unwanted results")
    parser.add_argument('-p','--prefix',type=int,help="the prefix length must be between 0-32")
    parser.add_argument('-H','--hosts',type=int,help="number of hosts per network, if the number of subnets (-s) is specified also it will be ignored")
    parser.add_argument('-L','--hostslist',nargs='*',type=int,help="number of hosts per each network")
    parser.add_argument('-s','--subnets',type=int,help="the number of subnets, if the number of hosts (-H) is specified also it will be prioritized")
    args=parser.parse_args()
    if not (args.ipaddress and ( args.prefix or args.mask)):
        parser.print_help()
        sys.exit(1)
    ip=validate_ip(args.ipaddress)
    prefix = args.prefix
    mask = args.mask
    if prefix and not mask:
        if not 0<=prefix<=32:
            print("Invalide prefix !!!!!!!!!!!!!!")
        mask = Binary2ip("1"*prefix + "0"*(32-prefix))
    else:
        mask=validate_ip(mask)
    
    nbrofsubnets = args.subnets
    nbrhost = args.hosts
    hostslist = args.hostslist
    if nbrhost:
        subneting_hosts(ip, mask, nbrhost)
    elif nbrofsubnets:
        subneting(ip, mask, nbrofsubnets)
    elif hostslist:
        hostslist.sort(reverse=True)
        subneting_hosts_per_network(ip, mask, hostslist)
    else:
        print("Network info : ")
        NetInfo(ip,mask)
    