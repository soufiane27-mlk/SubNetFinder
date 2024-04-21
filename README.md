# SubNetFinder

SubNetFinder is a command-line tool for subnetting IPv4 addresses, performing Variable Length Subnet Mask (VLSM) operations, and calculating network information.

## Features

- Subnet IP addresses based of number of subnets.
- Subnet IP addresses based of number of hosts.
- Perform VLSM subnetting.
- Calculate network information.

## Usage

```
python SubNetFinder.py [-h] [-i IPADDRESS] [-m MASK] [-p PREFIX] [-H HOSTS] [-L [HOSTSLIST ...]] [-s SUBNETS]
```

### Arguments

- `-i, --ipaddress`: The IP address to work with. If used, either the mask (`-m`) or the prefix (`-p`) should be specified.
- `-m, --mask`: The subnet mask address. If not specified correctly, the script may produce unwanted results.
- `-p, --prefix`: The prefix length, must be between 0 and 32.
- `-H, --hosts`: The number of hosts per network. If the number of subnets (`-s`) is specified, it will be ignored.
- `-L, --hostslist`: The number of hosts per each network.
- `-s, --subnets`: The number of subnets. If the number of hosts (`-H`) is specified, it will be prioritized.

### Examples

```
# Subnet an IP address with a prefix of 24 into 4 subnets
python SubNetFinder.py -i 192.168.1.0 -p 24 -s 4

# Subnet an IP address with a specific subnet mask into subnets with 30 hosts per subnet
python SubNetFinder.py -i 192.168.1.0 -m 255.255.255.0 -H 30

# show network information
python SubNetFinder.py -i 192.168.1.0 -p 24 

# Perform VLSM subnetting using a list
python SubNetFinder.py -i 192.168.1.0 -p 24 -L 30 14 126
```

## Acknowledgments

- This tool is inspired by the need to quickly perform subnetting and VLSM operations in various networking scenarios.
