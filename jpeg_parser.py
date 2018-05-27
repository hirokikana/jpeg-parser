#!/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function
import struct
import sys
import binascii
import StringIO

def analyze_header(header, body):
    bodyIo = StringIO.StringIO(body)
    if header == "\xff\xc0":
        # SOF0
        height = struct.unpack('>h',body[1:3])[0]
        width = struct.unpack('>h',body[3:5])[0]
        print("\timage height: %s" % height)
        print("\timage width: %s" % width)

    if header == "\xff\xe0":
        format = bodyIo.read(5)
        major = binascii.hexlify(bodyIo.read(1))
        minor = binascii.hexlify(bodyIo.read(1))
        density = bodyIo.read(1)
        x = bodyIo.read(2)
        y = bodyIo.read(2)
        thumbnailX = bodyIo.read(2)
        thumbnailY = bodyIo.read(2)

        print("\tformat: %s" % format)
        print("\tversion: v%s.%s" % (major, minor))

    # DQT
    if header == "\xff\xdb":
        numOfTable = len(body) / 65
        for i in range(0,numOfTable):
            bodyIo.read(1)
            table = bodyIo.read(64)
            print("\tTable #%d" % i, end="") 
            for i in range(0,64):
                if (i % 8 == 0):
                    print()
                    print("\t", end="")
                print(binascii.hexlify(table[i]), end="")
            print("\n")

    # DHT
    if header == "\xff\xc4":
        classAndIndex =  bodyIo.read(1)
        tableIndex = struct.unpack('b', classAndIndex)[0] & 0b0001111
        tableClass = "AC" if (struct.unpack('b', classAndIndex)[0] & 0b11110000) >> 4 == 1 else "DC"

        print("\tTable class: %s" % tableClass)
        print("\tTable index: %s" % tableIndex)

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
