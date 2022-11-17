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


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"[{self.x};{self.y}]"


class Canvas:
    def __init__(self):
        self._pixel_data = [0] * 32 * 32
        self._current_resolution = 32
        self._erase_color = 0
        self._current_color = 0

    def set(self, x, y):
        self._pixel_data[y * 32 + x] = self._current_color

    def get(self, x, y):
        return self._pixel_data[y*32 + x]

    def erase(self, x, y):
        self._pixel_data[y * 32 + x] = self._erase_color

    def clear(self, colour):
        for x in range(32):
            for y in range(32):
                self.erase(x, y)

    def set_colour(self, colour):
        self._current_color = colour

    def set_resolution(self, resolution):
        self._current_resolution = resolution

    def replace_colour(self, old_color, new_colour):
        tmp = self._current_color
        self._current_color = new_colour
        for x in range(32):
            for y in range(32):
                if self.get(x, y) == old_color:
                    self.set(x, y)

        self._current_color = tmp

    def render(self, pixel_size):
        img = Image.new("RGB", (32 * pixel_size, 32 * pixel_size))
        draw = ImageDraw.Draw(img)

        for y in range(32):
            for x in range(32):
                x0 = x * pixel_size
                y0 = y * pixel_size
                pos = [(x0, y0), (x0 + pixel_size, y0 + pixel_size)]
                pixel_color_index = self.get(x, y) if self.get(x, y) < 100 else 0
                pixel_color = BGRtoRGB(COLOUR_PALETTE[pixel_color_index])
                draw.rectangle(pos, fill=pixel_color, outline=pixel_color)

        return img


class CommandHandler:
    def __init__(self, file, canvas: Canvas):
        self._file = file
        self._canvas = canvas
        self._stroke_number = 0
        self._was_a_stroke = False
        self._command_list = {
            b'\xF0': self.draw_pixels,
            b'\xF1': self.draw_line,
            b'\xF2': self.draw_circle,
            #
            b'\xF5': self.replace_color,
            b'\xF6': self.erase_pixel,
            b'\xF7': self.clear_canvas,
            b'\xF8': self.pan_canvas,
            #
            b'\xFA': self.set_color,
            b'\xFB': self.set_canvas_resolution,
        }
        self._movement_list = {
            1: Position(-1, -1),
            2: Position( 0, -1),
            3: Position( 1, -1),
            4: Position(-1,  0),
            6: Position( 1,  0),
            7: Position(-1,  1),
            8: Position( 0,  1),
            9: Position( 1,  1),
        }

    def execute(self):
        command = self._file.read(1)

        if command not in self._command_list:
            raise IndexError(f"Command {command} is not supported")

        ret = 1
        return ret + self._command_list[command]()

    def was_command_a_stroke(self):
        return self._was_a_stroke

    def _get_stroke_number(self):
        data = self._file.read(2)
        data = struct.unpack("BB", data)
        self._stroke_number = (data[1] - 0x0A) + (data[0] - 0x0A) * 0x9F

    def _get_pixel_list(self):
        data = self._file.read(3)
        data = struct.unpack("BBB", data)
        byte_read = 3
        current_pixel = Position(data[1] >> 2, data[2] >> 2)
        ret = [ current_pixel ]
        pixel_count = data[0]

        for i in range(1, pixel_count, 2):
            data = self._file.read(1)
            data = struct.unpack("B", data)
            byte_read = byte_read + 1
            pixel_couple = data[0]
            for p in range(2):
                val = pixel_couple & 0x0F
                if val in self._movement_list:
                    move = self._movement_list[val]
                    current_pixel = Position(current_pixel.x + move.x, current_pixel.y + move.y)
                    ret.append(current_pixel)

                pixel_couple = pixel_couple >> 4

        return byte_read, ret

    def draw_pixels(self):
        self._was_a_stroke = True
        self._get_stroke_number()
        byte_count, pixel_list = self._get_pixel_list()

        for pixel in pixel_list:
            self._canvas.set(pixel.x, pixel.y)

        return byte_count + 2

    def draw_line(self):
        self._was_a_stroke = True
        self._get_stroke_number()

        data = self._file.read(5)
        data = struct.unpack("5B", data)

        # TODO: Need to look what method they use to draw lines to be accurate
        print("Draw Line...")
        # Always read 7 bytes (2 for stroke, 5 for arguments)
        return 7

    def draw_circle(self):
        self._was_a_stroke = True
        self._get_stroke_number()

        data = self._file.read(5)
        data = struct.unpack("5B", data)

        # TODO: Need to look what method they use to draw circles to be accurate
        print("Draw Circle...")
        # Always read 7 bytes (2 for stroke, 5 for arguments)
        return 7

    def replace_color(self):
        self._was_a_stroke = True
        self._get_stroke_number()
        data = self._file.read(2)
        data = struct.unpack("BB", data)

        self._canvas.replace_colour(data[1] - 28, data[0] - 28)

        # Always read 4 bytes (2 for stroke, 2 for arguments)
        return 4

    def erase_pixel(self):
        self._was_a_stroke = True
        self._get_stroke_number()
        byte_count, pixel_list = self._get_pixel_list()

        for pixel in pixel_list:
            self._canvas.erase(pixel.x, pixel.y)

        return byte_count + 2

    def clear_canvas(self):
        self._was_a_stroke = True
        self._get_stroke_number()

        data = self._file.read(1)
        data = struct.unpack("B", data)
        # Not sure what to do with data here.

        self._canvas.clear(data[0])

        # Always read 3 bytes (2 for stroke, 1 for ?)
        return 3

    def pan_canvas(self):
        self._was_a_stroke = True
        self._get_stroke_number()

        # This may be panning, not sure.

        data = self._file.read(3)
        data = struct.unpack("BBB", data)

        return 5

    def set_color(self):
        self._was_a_stroke = False
        data = self._file.read(2)
        data = struct.unpack("BB", data)

        self._canvas.set_colour(data[0] - 28)

        # Always read 2 bytes
        return 2

    def set_canvas_resolution(self):
        self._was_a_stroke = False
        data = self._file.read(2)
        data = struct.unpack("BB", data)

        self._canvas.set_resolution(data[0] - 28)

        # Always read 2 bytes
        return 2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--output", "-o", default="output.gif")
    parser.add_argument("--pixelsize", "-p", default=10, type=int)
    args = parser.parse_args()

    pixel_size = args.pixelsize

    with open(args.input, "rb") as f:
        header = f.read(32)
        header_data = struct.unpack("<4cLLL12x4c", header)

        canvas = Canvas()
        cmd = CommandHandler(f, canvas)

        frames = []

        if header_data[0] == b"P" and \
           header_data[1] == b"T" and \
           header_data[2] == b"C" and \
           header_data[3] == b"R" and \
           header_data[7] == b"\xAA" and \
           header_data[8] == b"\x55" and \
           header_data[9] == b"\xAA" and \
           header_data[10] == b"\x55":

            version = header_data[4]
            number_of_strokes = header_data[5]
            data_size = header_data[6]
            pos = 0

            while pos < data_size:
                pos = pos + cmd.execute()
                if cmd.was_command_a_stroke():
                    img = canvas.render(args.pixelsize)
                    img.save("frame.png")
                    frames.append(img)

            print(f"NoS: {number_of_strokes}, last read: {cmd._stroke_number}")

            frames[0].save(args.output,
                           save_all=True,
                           append_images=frames[1:],
                           optimize=False,
                           duration=100,
                           loop=1)
        else:
            print(f"File {args.input} is not a PTCR file")


if __name__ == "__main__":
    main()