#!/bin/env python
#-*- coding:utf-8 -*-
import sys 

class Parser():
    def __init__(self, fd):
        self.fd = fd

    def is_jpeg(self):
        self.fd.seek(0)
        if self.fd.read(2) == b'\xff\xd8':
            return True
        else:
            return False

    def get_next_segment(self):
        if self.fd.tell() == 0:
            self.is_jpeg()

        marker_name = self.__get_marker_name(self.fd.read(2))
        if marker_name != 'SOS':
            segment_length = self.__get_segment_length(self.fd.read(2))
            body = self.fd.read(segment_length)

            return {'name': marker_name,
                    'length': segment_length,
                    'body': body}
        return ''

    def __get_segment_length(self, length_binary):
        return int.from_bytes(length_binary, 'big') - 2
    
    def __get_marker_name(self, marker_binary):
        marker_table = {
            b'\xff\xe0': 'APP0',
            b'\xff\xe1': 'APP1',
            b'\xff\xe2': 'APP2',
            b'\xff\xe3': 'APP3',
            b'\xff\xe4': 'APP4',
            b'\xff\xe5': 'APP5',
            b'\xff\xe6': 'APP6',
            b'\xff\xe7': 'APP7',
            b'\xff\xe8': 'APP8',
            b'\xff\xe9': 'APP9',
            b'\xff\xea': 'APP10',
            b'\xff\xeb': 'APP11',
            b'\xff\xec': 'APP12',
            b'\xff\xed': 'APP13',
            b'\xff\xee': 'APP14',
            b'\xff\xef': 'APP15',
            b'\xff\xdb': 'DQT',
            b'\xff\xc0': 'SOF0',
            b'\xff\xc4': 'DHT',
            b'\xff\xda': 'SOS',
            b'\xff\xfe': 'COM',
            b'\xff\xc2': 'SOF2',
        }
        if marker_binary in marker_table.keys():
            return marker_table[marker_binary]
        else:
            print(marker_binary)
            import pdb;pdb.set_trace()
            return ''
        
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("filename is required")
        sys.exit(1)

    filename = sys.argv[1]
    fd = open(filename, 'rb')
    parser = Parser(fd)

    if parser.is_jpeg() == False:
        print("%s is not jpeg file" % filename)
        fd.close()
        sys.exit(1)

    while(True):
        result = parser.get_next_segment()
        if result != '':
            print('semgment_name: %s' % result['name'])
            print('semgment_body_length: %s' % result['length'])
            #print('semgment_body: %s' % result['body'])
            print('-----------------------------------')
        else:
            image = b''
            byte_data = fd.read(1)
            while (True):
                image += byte_data
                byte_data = fd.read(1)
                if byte_data == b'\xff':
                    byte_data = fd.read(1)
                    if byte_data == b'\xd9':
                        break
                    else:
                        image += byte_data
            print('image length: %s' % len(image))
            break
        
    fd.close()
    

