#!/bin/env python
# -*- coding:utf-8 -*-

import struct
import sys
import binascii

def analyze_header(header, body):
    if header == "\xff\xc0":
        # SOF0
        height = struct.unpack('>h',body[1:3])[0]
        width = struct.unpack('>h',body[3:5])[0]
        print("\timage height: %s" % height)
        print("\timage width: %s" % width)

def convert_to_headername(header):
    header_name = {
        "\xff\xc0": 'SOF0',
        "\xff\xd8": 'SOI',
        "\xff\xe0": 'APP0',
        "\xff\xe1": 'APP1',
        "\xff\xe2": 'APP2',
        "\xff\xe3": 'APP3',
        "\xff\xe4": 'APP4',
        "\xff\xe5": 'APP5',
        "\xff\xe6": 'APP6',
        "\xff\xe7": 'APP7',
        "\xff\xe8": 'APP8',
        "\xff\xe9": 'APP9',
        "\xff\xea": 'APP10',
        "\xff\xeb": 'APP11',
        "\xff\xec": 'APP12',
        "\xff\xed": 'APP13',
        "\xff\xee": 'APP14',
        "\xff\xef": 'APP15',
        "\xff\xdb": 'DQT',
        "\xff\xc4": 'DHT',
        "\xff\xda": 'SOS',
        "\xff\xd9": 'EOI',
        "\xff\xdd": 'DRI',
    }
    return header_name[header]

filename = sys.argv[1]
fd = open(filename, 'rb')

# SOI header
if fd.read(2) != "\xff\xd8":
    print("no jpeg format")
    sys.exit(0)

while True:
    header = fd.read(2)

    if len(header) == 0:
        break
    
    EOI = False
    # SOS header
    if header == "\xff\xda":
        print("------------BEGIN IMAGE--------------")
        body = fd.read()
        img = body[:-2]
        EOI = body[-2:]
        size = len(body)
    else:
        # header分引く
        size = struct.unpack('>h', fd.read(2))[0] - 2
        body = fd.read(size)

    print("header: %s(%s)" % (binascii.hexlify(header), convert_to_headername(header)))
    print("  size: %d" % size)

    # header解析
    analyze_header(header, body)
    
    if EOI:
        print("header: %s(EOI)" % binascii.hexlify(EOI))
        
fd.close()
