#!/bin/env python
#-*- coding:utf-8 -*-
import sys 

class ExifParser():
    def __init__(self, data):
        self.data = data
        exif_spec = result['body'][0:6]
        exif_body = result['body'][6:]
        byte_order = exif_body[0:2]
        aa = exif_body[2:4]
        self.exif_body = exif_body

    def parse(self):
        exif_body = self.exif_body
        ifd_offset = int.from_bytes(exif_body[4:8], 'big')
        field_count = int.from_bytes(exif_body[ifd_offset:ifd_offset+2],'big')
        field_start = ifd_offset+2
        for i in range(field_count):
            start = field_start + i * 12
            field_data = exif_body[start:start+12]
            field_tag = field_data[0:2]
            field_type = field_data[2:4]
            field_count = int.from_bytes(field_data[4:8],'big')
            field_offset = field_data[8:12]
            data = exif_body[int.from_bytes(field_offset,'big'):int.from_bytes(field_offset,'big')+field_count * type_size[int.from_bytes(field_type,'big') - 1]]
            print('tag: %s / type: %s / data %s' % (binascii.hexlify(field_tag), binascii.hexlify(field_type), data))

        


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


    tag_mapping = {
    }
    type_size = [1,1,2,4,8,1,1,2,4,8,4,8]
    import binascii
    
    while(True):
        result = parser.get_next_segment()
        if result != '':
            if result['name'] == 'APP1':
                exif_parser = ExifParser(result['body'])
                exif_parser.parse()


                
                exif_spec = result['body'][0:6]
                exif_body = result['body'][6:]
                byte_order = exif_body[0:2]
                aa = exif_body[2:4]
                ifd_offset = int.from_bytes(exif_body[4:8], 'big')
                field_count = int.from_bytes(exif_body[ifd_offset:ifd_offset+2],'big')
                field_start = ifd_offset+2
                for i in range(field_count):
                    start = field_start + i * 12
                    field_data = exif_body[start:start+12]
                    field_tag = field_data[0:2]
                    field_type = field_data[2:4]
                    field_count = int.from_bytes(field_data[4:8],'big')
                    field_offset = field_data[8:12]
                    data = exif_body[int.from_bytes(field_offset,'big'):int.from_bytes(field_offset,'big')+field_count * type_size[int.from_bytes(field_type,'big') - 1]]
                    print('tag: %s / type: %s / data %s' % (binascii.hexlify(field_tag), binascii.hexlify(field_type), data))
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
    

