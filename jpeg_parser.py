#!/bin/env python
#-*- coding:utf-8 -*-
import sys 

class Parser():
    def __init__(self, fd):
        self.fd = fd

    def is_jpeg(self):
        self.fd.seek(0)
        if self.fd.read(2) == '\xff\xd8':
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
        return int(''.join(['%x' % ord(x) for x in length_binary]), 16) - 2 
    
    def __get_marker_name(self, marker_binary):
        marker_table = {
            '\xff\xe0': 'APP0',
            '\xff\xe1': 'APP1',
            '\xff\xe2': 'APP2',
            '\xff\xe3': 'APP3',
            '\xff\xe4': 'APP4',
            '\xff\xe5': 'APP5',
            '\xff\xe6': 'APP6',
            '\xff\xe7': 'APP7',
            '\xff\xe8': 'APP8',
            '\xff\xe9': 'APP9',
            '\xff\xea': 'APP10',
            '\xff\xeb': 'APP11',
            '\xff\xec': 'APP12',
            '\xff\xed': 'APP13',
            '\xff\xee': 'APP14',
            '\xff\xef': 'APP15',
            '\xff\xdb': 'DQT',
            '\xff\xc0': 'SOF0',
            '\xff\xc4': 'DHT',
            '\xff\xda': 'SOS',
            '\xff\xfe': 'COM',
            '\xff\xc2': 'SOF2',
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
            image = ''
            byte_data = fd.read(1)
            while (True):
                image += byte_data
                byte_data = fd.read(1)
                if byte_data == '\xff':
                    byte_data = fd.read(1)
                    if byte_data == '\xd9':
                        break
                    else:
                        image += byte_data
                
            break
        
    fd.close()
    

