#!/usr/bin/python3


import sys
from tabulate import tabulate
import struct


class GzipHeader:
    def __init__(self, raw_list):
        self.magic = hex(raw_list[0])
        self.compression = self.get_compression(raw_list[1])

        file_flags = '{0:08b}'.format(raw_list[2])

        self.file_flag_FTEXT = file_flags[0]
        self.file_flag_FHCRC = file_flags[1]
        self.file_flag_FEXTRA = file_flags[2]
        self.file_flag_FNAME = file_flags[3]
        self.file_flag_FCOMMENT = file_flags[4]
        self.file_flag_RES1 = file_flags[5]
        self.file_flag_RES2 = file_flags[6]
        self.file_flag_RES3 = file_flags[7]


        self.timestamp = raw_list[3]
        self.compression_flags = raw_list[4]
        self.os_id = self.get_os(raw_list[5])

    def get_compression(self, value):
        methods = {
            0: "reserved",
            1: "reserved",
            2: "reserved",
            3: "reserved",
            4: "reserved",
            5: "reserved",
            6: "reserved",
            7: "reserved",
            8: "deflate"
        }
        try:
            method = methods[value]
        except KeyError:
            method = None
        return method

    def get_os(self, value):
        systems = {
            0 : "FAT filesystem (MS-DOS, OS/2, NT/Win32)",
            1 : "Amiga",
            2 : "VMS (or OpenVMS)",
            3 : "Unix",
            4 : "VM/CMS",
            5 : "Atari TOS",
            6 : "HPFS filesystem (OS/2, NT)",
            7 : "Macintosh",
            8 : "Z-System",
            9 : "CP/M",
            10 : "TOPS-20",
            11 : "NTFS filesystem (NT)",
            12 : "QDOS",
            13 : "Acorn RISCOS",
            255 : "unknown"
        }
        try:
            system = systems[value]
        except KeyError:
            system = None
        return system

    def display(self):
        items = []
        for key, value in self.__dict__.items():
            if key[0] != "_":
                items.append([key, value])
        return items

    def validate(self):
        for key, value in self.__dict__.items():
            if key[0] != "_":
                if value == None:
                    return False
        
        return True


def parse_gzip(file_bytes):
    standard_header_length = 10
    gzip_format = "@HBBIBB"
    gzip_header_raw = struct.unpack(gzip_format, file_bytes[:standard_header_length])
    gzip_header = GzipHeader(gzip_header_raw)
    return gzip_header


def main():

    gzip_magic = b"\x1F\x8B"

    if len(sys.argv) <=1:
        print("Usage: find_gzip.py <file>")
        exit()

    f = open(sys.argv[1], "rb")
    input_file_raw = bytearray(f.read())
    f.close()

    file_index = 0
    header_count = 0
    print("Scanning file...")
    headers = []

    while file_index < len(input_file_raw):
        if input_file_raw[file_index:file_index+2] == gzip_magic:
            bytes_from_index = input_file_raw[file_index:]

            gzip_header = parse_gzip(bytes_from_index)
            
            if gzip_header.validate():
                header_count += 1
                print(f"Gzip header {header_count}")
                print(f"Address: {file_index} ({hex(file_index)})")
                headers.append([header_count, f"{file_index} ({hex(file_index)})"])
                print(tabulate(gzip_header.display()))
                print("")
                print("")
                print("Continuing scan...")

                

        file_index += 1
        


    print("File scan finished")
    print(f"Total gzip headers found: {len(headers)}")
    print(tabulate(headers))

if __name__ == "__main__":
    main()