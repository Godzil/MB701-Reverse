PIXB File format
================

 ## Basic structure

```
struct PIXBFile:
    struct Header:
        char[4]  = "PIXB"
        uint16_t unknown
        uint32_t Version (?)
        uint16_t Canvas size
        uint32_t unknoxn
        char[16]: unknown

    char[928]: data
```

Each pixels is stored in a 7 bit packed format which allow to store 8 pixel in 7 bytes:

| bit 56-50 | bit 49-43 | bit 42-36 | bit 35-29 | bit 28-22 | bit 21-15 | bit 14-8 | bit 7-0 |
|-----------|-----------|-----------|-----------|-----------|-----------|----------|---------|
| pixel 7   | pixel 6   | pixel 5   | pixel 4   | pixel 3   | piexl 2   | pixel 1  | pixel 0 |


Only value between 0 and 99 are valid, the palette only have 100 entry, all value equal or higher to 100 are 
considered to be color 0 

Also, the file is always the same size and always contain enough space to store the 32x32 size. 

If the image is using a 16x16 canvas or 24x24 canvas, the start of the image is shifted by a couple of pixels

Canvas size can take only 3 values:
 - 0: 16x16 canvas
 - 1: 24x24 canvas
 - 2: 32x32 canvas


## Color palette

```
0xFFFFFF, 0xE9BFA8, 0xECC7AC, 0xEFCFB0, 0xF4DDB7, 0xF7E4BB, 0xF7E4BB, 0xFAEBBE, 0xFDF2C1, 0xFFF9C4, 
0xF2F2C3, 0xE3EBC5, 0xD4E3C0, 0xC5DBBE, 0xC5DDCC, 0xC4DEDA, 0xC4E0E8, 0xC4E1F5, 0xC8D9EE, 0xCBD0E6,
0xCEC5DE, 0xD0BAD5, 0xD6BBCB, 0xDDBDC0, 0xE3BEB4, 0xD1D1D2, 0xD37859, 0xD88A5F, 0xDE9B64, 0xE3AB69,
0xE9BA6E, 0xEFC972, 0xF4D777, 0xFAE57A, 0xFFF387, 0xE4E47E, 0xC6D57D, 0xA5C57C, 0x82B47B, 0x81B798,
0x7FBAB5, 0x7DBDD0, 0x7BBFE9, 0x8AB4DD, 0x96A3CE, 0x9F8EBB, 0xA572A6, 0xB17495, 0xBD7683, 0xC8776F,
0x7D7E7F, 0xC1001F, 0xC63F1F, 0xCC5E1E, 0xD4791D, 0xDC931A, 0xE5AB14, 0xEEC200, 0xF6D800, 0xFFEC00,
0xD4D51D, 0xA2BD30, 0x6BA53A, 0x118F40, 0x009266, 0x00958E, 0x0099B7, 0x009CDD, 0x348ECB, 0x5A76B2,
0x6F5496, 0x7E177A, 0x901366, 0xA20E50, 0xB20039, 0x1F1E21, 0x551415, 0x5F2517, 0x693618, 0x754819,
0x825B1A, 0x8F701A, 0x9E8519, 0xAD9B16, 0xBAAC12, 0x98981F, 0x6F8127, 0x456C2B, 0x005A2C, 0x006145,
0x006864, 0x007086, 0x0077A4, 0x266992, 0x3F537A, 0x4A3762, 0x500D4D, 0x560C3E, 0x58102E, 0x591320
```

