#!/usr/bin/env python3 
# -*- coding:utf-8 -*-

import sys
import struct
import socket

def ip2int(strip):
    """Convert a ip to a int number"""
    return struct.unpack('!I',socket.inet_aton(strip))[0]

def int2ip(intip):
    """Convert a int ip to a string ip"""
    return socket.inet_ntoa(struct.pack('!I',intip))

def str2num(s):
    """Convert a number to a chr."""

    l = 0
    try:
        for i in range(len(s)):
            l = l << 8
            if sys.version_info.major == 3:
                l += s[i]
            else:
                l += ord(s[i])
        return l
    except:
        return 0


def bytechr(i):
    if isinstance(i, bytes):
        return i
    if sys.version_info.major == 3:
        return bytes([i])
    else:
        return chr(i)


def convert_bytes_to_str(s, encoding='utf-8'):
    if isinstance(s, str):
        return s
    elif isinstance(s, bytes):
        if sys.version_info.major == 3:
            try:
                return s.decode(encoding)
            except UnicodeDecodeError:
                # print("convert_bytes_to_str error,maybe is encrypted")
                return None
        else:
            return s
    else:
        # print('不是字节，convert_bytes_to_str转换失败，返回None')
        return None

if __name__=='__main__':
    # strip = '192.168.3.12'
    # print(socket.inet_aton(strip))
    # print(socket.inet_ntoa(b'\xc0\xa8\x03\x0c'))
    # intip = ip2int(strip)
    # print(intip)
    # strip = int2ip(intip)
    # print(strip)
    b=b'\x00\x00\x00'
    s=convert_bytes_to_str(b)
    print(b)
    print(s)
    s=s.strip(b'\x00'.decode(encoding='utf-8'))
    print(len(s))


