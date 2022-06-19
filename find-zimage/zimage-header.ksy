meta:
  id: zimage
  endian: be
  license: CC0-1.0
  title: Linux zImage wrapper
doc: |
  zImage is the compressed binary image of a linux kernel. It's what the bootloader
  will load and attempt to execute. The zImage kernel is "self extracting" in the
  sense that it can be copied to some place in RAM and run from there as-is, without
  an additional decompression step. The bulk of the kernel is still compressed, 
  (most often with gzip), however there is a small uncompressed stub prepended to it
  which does the decompression in-place.
seq:
  - id: prolog
    size: 32
  - id: header
    type: zimage_header

types:
  zimage_header:
    meta:
      endian:
        switch-on: _root.prolog
        cases: 
          '[0x00,0x00,0xa0,0xe1,0x00,0x00,0xa0,0xe1,0x00,0x00,0xa0,0xe1,0x00,0x00,0xa0,0xe1,0x00,0x00,0xa0,0xe1,0x00,0x00,0xa0,0xe1,0x00,0x00,0xa0,0xe1,0x00,0x00,0xa0,0xe1,]' : le
          '[0xe1,0xa0,0x00,0x00,0xe1,0xa0,0x00,0x00,0xe1,0xa0,0x00,0x00,0xe1,0xa0,0x00,0x00,0xe1,0xa0,0x00,0x00,0xe1,0xa0,0x00,0x00,0xe1,0xa0,0x00,0x00,0xe1,0xa0,0x00,0x00,]' : be
    seq:
      - id: unknown1
        type: u4
      - id: magic1
        type: u4
      - id: start_address
        type: u4
      - id: end_address
        type: u4
      - id: endianness
        type: u4

