PTCR File:
==========

 ## Basic structure

```
struct PTCRFile:
    struct Header:
        char[4]  = "PTCR"
        uint32_t version?
        uint32_t numberOfCommands? (only drawable commands?)
        uint32_t fileSize - Header
        char[12]: unknown
        char[4] = 0xAA, 0x55, 0xAA, 0x55

    char[]: data
```

Data contain commands that correspond to all the action that can be done on the MB701.

Each command start with an opcode, then a couple of bytes following depending on the opcode

In each drawing command, the _stoke number_ (byte 1 and byte 2) seems to be sequentially increasing.

 ## Commands

 ### F0: drawPixels

| byte 0 | byte 1    | byte 2    | byte 3      | byte 4  | byte 5  | byte x     |
| ------ |-----------|-----------|-------------|---------|---------|------------|
| F0     | Stroke #1 | Stroke #2 | Pixel count | Start X | Start Y | Pixel data |

 #### Notes
 - Start position X and Y are stored *4 their real value
 - The count of pixel data is `(pixel count - 1) / 2`

Each addition pixel are calculated relative with the last drawn pixel.
Each byte store the position of two pixels, b0-b3 for the first pixel, b4-b7 for the second, if the number of pixels is odd, the last b4-b7 is ignored and should be zero.

The number you get give the direction to move the pixel according to that diagram:
```
X ------->
Y  1      2      3
|  4    Origin   6
|  7      8      9
V
```
5 is ignored as it is the origin.

*All other value are treated like 5 and ignored.*

 #### Examples
 - `F0 0A 14 01 34 40`: 1 pixel at [13;16]
 - `F0 0A 11 05 30 4C 66 66`: 5 pixels at [12;19], [13;19], [14;19], [15;19], [16;19]

 #### Note

Some of the files stored in the device seems to not store the right value for pixel count, 
but when counting they have not more than 255 pixels, so it's a bit unclear why. Need more investigation on that.
Also it is unknown at the moment what happen if there are more than 255 pixels in one stroke, which is technically
possible as 32x32 pixel = 1024.

> After some test, well it seems drawing too many pixel in one stroke do crash the art board :-)


 ### F1: drawLine

| byte 0 | byte 1    | byte 2    | byte 3 | byte 4 | byte 5 | byte 6 | byte 7 |
|--------|-----------|-----------|--------|--------|--------|--------| ------ |
| F1     | Stroke #1 | Stroke #2 | ???    | x0     | y0     | x1     | y1     |

A line is drawn between [x0;y0] and [x1; y1]

 #### Examples:
 - `F1 0A 0E 02 38 20 58 10`: Will draw a line 


 ### F2: drawCircle

| byte 0 | byte 1    | byte 2    | byte 3 | byte 4 | byte 5 | byte 6 | byte 7 |
|--------|-----------|-----------|--------|--------|--------|--------| ------ |
| F2     | Stroke #1 | Stroke #2 | ???    | x0     | y0     | x1     | y1     |

The circle is drawn in the rectangle designed by [x0;y0] - [x1; y1]

 #### Examples:
 - `F2 0A 55 02 34 24 54 44`
 - `F2 0A 57 02 50 24 50 24`


 ### F3: Not used
 ### F4: Not used


 ### F5: replaceColor
| byte 0 | byte 1    | byte 2    | byte 3    | byte 4         |
|--------|-----------|-----------|-----------|----------------|
| F5     | Stroke #1 | Stroke #2 | New color | Replaced color |

Colors are stored with an offet of 28 (0x1C). Reason unknown.
So if you read 28, the actual color to use is 0

 #### Examples:
 - `F5 0A 5B 5B 5F`
 - `F5 0A 7B 2A 5B`


 ### F6: erasePixel (?)

| byte 0 | byte 1    | byte 2    | byte 3      | byte 4  | byte 5  | byte x     |
|--------|-----------|-----------|-------------|---------|---------|------------|
| F6     | Stroke #1 | Stroke #2 | Pixel count | Start X | Start Y | Pixel data |

*Work like F0, but erase pixel instead of drawing, see F0 for the format*


 ### F7: clearCanvas

| byte 0 | byte 1    | byte 2    | byte 3                 |
|--------|-----------|-----------|------------------------|
| F7     | Stroke #1 | Stroke #2 | ??? (Color to clear?)  |

Code clear the canvas to all white whatever the value. Not sure what the byte 3 is suppose to represent.

 #### Examples:
 - `F7 0C 4B 00`
 - `F7 16 2E 00`


 ### F8: Unknown (Panning?)

| byte 0 | byte 1    | byte 2    | byte 3 | byte 4 | byte 5 | 
|--------|-----------|-----------|--------|--------|--------|
| F8     | Stroke #1 | Stroke #2 | ???    | ???    | ???    |

This command is present in at least one file (P0003_09.DAT) but is not handled by the
iOS/Android app. Having looked at the history of that image on the device at one point 
the whole image shift by 1 and 1 pixel, this could be related as the command in the file is

`F8 0F 58 04 01 01`

And we clearly have a 1 and 1 in the bytes, 4 could be related to the direction.

More test need to be done.


 ### F9: Not used


 ### FA: setColor
| byte 0 | byte 1    | byte 2 |
|--------|-----------|--------|
| FA     | new color | ???    |

Colors are stored with an offet of 28 (0x1C). Reason unknown.
So if you read 28, the actual color to use is 0

 #### examples:
 - `FA 67 6A` : now work with colour 0x4B
 - `FA 20 67` : now work with colour 0x04


 ### FB: setCanvasResolution
| byte 0 | byte 1          | byte 2        |
|--------|-----------------|---------------|
| FB     | horizontal size | vertical size |

_If the value is not 0 (16x16), 1 (24x24) or 2 (32x32) it will default back to 0_


 ### FC: Not used
 ### FD: Not used
 ### FE: Not used
 ### FF: Not used


## How stroke number work:

For some reason 0 is represented by 0x0A (10) 0x0A. 
When the number of storke is increased the second byte is incremented by 1. 
Then when the second byte reach 0x9F (159) the first one will be incremented and the
second byte reset to 0x0A.


Example:


| Hex   | Binary              | Decilam |
|-------|---------------------|---------|
| 0A 0A | 0000 1010 0000 1010 | 10  10  |
| ...   |                     |         |
| 0A 9F | 0000 1010 1001 1111 | 10  159 |
| 0B 0A | 0000 1011 0000 1010 | 11  10  |
| ...   |                     |         |
| 0B 9F | 0000 1011 1001 1111 | 11  159 |
| 0C 0A | 0000 1100 0000 1010 | 12  10  |
| ...   |                     |         |
| 18 89 | 0001 1000 1000 1001 | 24  137 |

_Why does it work this way? Your guess is as good as mine._