#/usr/bin/python3

import argparse
import struct
from tabulate import tabulate

class PTable():
    def __init__(self, data):
        self.headerLength = 48

        header_data = data[:self.headerLength]
        entries_data = data[self.headerLength:]

        self.header = PTableHeader(header_data)
        self.entries = PTableEntries(entries_data)

class PTableHeader():
    def __init__(self, header_data):
        struct_format = ">12sI16s16s"
        self.pTableHead, \
        self.property, \
        self.bootrom_version, \
        self.ptable_version = struct.unpack(struct_format, header_data)

    def __len__(self):
        return self.length

class PTableEntries():
    def __init__(self, entries_data):
        self.entryLength = 48
        self.entries = []

        index = 0
        while index < len(entries_data):
            entryStart = index
            entryEnd = index + self.entryLength
            entry = PTableEntry(entries_data[entryStart:entryEnd])
            self.entries.append(entry)
            index += self.entryLength
        
    def __iter__(self):
        self.entryIndex = 0
        return self

    def __next__(self):
        if self.entryIndex < len(self.entries):
            currentEntry = self.entries[self.entryIndex]
            self.entryIndex += 1
            return currentEntry
        else:
            raise StopIteration

    

class PTableEntry():
    def __init__(self, data):
        struct_format = ">16sIIIIIIII"
        self.name, \
        self.offset, \
        self.loadsize, \
        self.capacity, \
        self.loadaddr, \
        self.entry, \
        self.image, \
        self.property, \
        self.count = struct.unpack(struct_format, data)



def extract_pTable(firmware_data):
    pTableHead = b"pTableHead"
    pTableTail = b"pTableTail"

    try:
        pTableStart = firmware_data.index(pTableHead)
        pTableEnd = firmware_data.index(pTableTail)

        pTableSize = pTableEnd - pTableStart

    except:
        pTableSize = 0

    if pTableSize == 0:
        return None
    
    pTable = firmware_data[pTableStart:pTableEnd]
    return pTable





def main():

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('firmware', help='firmware binary file to scan')
    parser.add_argument('-o', "--outfile", help='output results to file')

    args = parser.parse_args()

    with open(args.firmware, mode='rb') as file:
        firmware_data = file.read()
    

    pTableData = extract_pTable(firmware_data)
    
    if pTableData == None:
        print("Partition table not found.")
        return

    pTable = PTable(pTableData)

    rows = []
    
    for entry in pTable.entries:
        row = []
        row_headers = []
        fieldnames = dir(entry)
        for name in fieldnames:
            if not name[0] == "_":
                val = getattr(entry, name)
                row_headers.append(name)
                if isinstance(val, int):
                    val = hex(val)
                row.append(val)
                
        rows.append(row)

    print("Huawei Partition Table")
    print(tabulate(rows, headers=row_headers))









if __name__ == "__main__":
    main()