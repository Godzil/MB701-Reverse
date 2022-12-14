import argparse
import struct
from PIL import Image, ImageDraw


COLOUR_PALETTE = [
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
]


def BGRtoRGB(val):
    return (val & 0xFF0000) >> 16 | (val & 0x00FF00) | ((val & 0x0000FF) << 16)


def unpack7to8(data):
    ret = []
    val = struct.unpack("<Q", data + b"\0")[0]
    for i in range(8):
        ret.append(val & 0x7F)
        val = val >> 7
    return ret


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--output", "-o", default="output.png")
    parser.add_argument("--pixelsize", "-p", default=10, type=int)
    parser.add_argument("--drawfull", default=False, type=bool)
    args = parser.parse_args()

    pixel_size = args.pixelsize

    with open(args.input, "rb") as f:
        header = f.read(32)
        header_data = struct.unpack("<4cxxH24x", header)

        if header_data[0] == b"P" and \
           header_data[1] == b"I" and \
           header_data[2] == b"X" and \
           header_data[3] == b"B":
            canvasSize = header_data[4]

            img = Image.new("RGB", (32*pixel_size, 32*pixel_size))
            draw = ImageDraw.Draw(img)

            # TODO: skip pixels not used if the canvas is not 32x32
            for y in range(32):
                for x in range(0, 32, 8):
                    img_block = f.read(7)
                    pixels = unpack7to8(img_block)
                    for p in range(8):
                        x0 = (x + p) * pixel_size
                        y0 = y * pixel_size
                        pos = [(x0, y0), (x0 + pixel_size, y0 + pixel_size)]
                        pixel_color_index = pixels[p] if pixels[p] < 100 else 0
                        pixel_color = BGRtoRGB(COLOUR_PALETTE[pixel_color_index])
                        draw.rectangle(pos, fill=pixel_color, outline=pixel_color)

            img.save(args.output)
        else:
            print(f"File {args.inpug} is not a PIXB file")

if __name__ == "__main__":
    main()