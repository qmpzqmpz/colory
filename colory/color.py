"""
This script tries to find the name of color using a given hex value
List of colors 'wiki_colors.csv' has been obtained from
https://en.wikipedia.org/wiki/List_of_colors:_A-F
https://en.wikipedia.org/wiki/List_of_colors:_G-M
https://en.wikipedia.org/wiki/List_of_colors:_N-Z

List of colors 'xkcd_colors.csv' has been obtained from
https://xkcd.com/color/rgb/
"""
import os
import tkinter

path = os.path.dirname(__file__)
col_files = {'wiki': path + '/wiki_colors/wiki_colors.csv',
             'xkcd': path + '/xkcd_colors/xkcd_colors.csv',
             'mat': path + '/mat_colors/mat_colors.csv'}
# read in both color lists
colors = {key: {} for key in col_files}
for key, fname in col_files.items():
    with open(fname, encoding='UTF8') as f:
        lis = [line.split(',') for line in f]
        for hex_val, name in lis:
            colors[key][hex_val] = name.rstrip()


class Color:
    """
    Fetches the name of the nearest matching color to a hexadecimal color string.

    value: str
            hex color name
    cols: str, optional (default='wiki')
            color list ('xkcd', 'wiki')
    """

    def __init__(self, value, colset='wiki'):
        self.value = value.replace('#', '0x')
        self.colset = colset

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    @property
    def name(self):
        return self.nearest_match()

    def nearest_match(self):
        # Find the nearest matching color from the list
        color = None
        min_diff = 16777215  # FFFFFF
        for hex_color, color_name in colors[self.colset].items():
            color_to_compare_hex = hex_color
            if self.euclidean_calculate(self.value, color_to_compare_hex) < min_diff:
                min_diff = self.euclidean_calculate(self.value, color_to_compare_hex)
                color = color_name
        return color

    def euclidean_calculate(self, c1, c2):
        # Check the last formula in https://en.wikipedia.org/wiki/Color_difference#Euclidean
        # c1 rgb
        c1 = self.hex_to_rgb(c1)
        # c2 rgb
        c2 = self.hex_to_rgb(c2)
        # delta square
        delta_r = (c1[0] - c2[0])
        delta_g = (c1[1] - c2[1])
        delta_b = (c1[2] - c2[2])
        r = (c1[0] + c2[0]) / 2
        delta_c = ((2 + r / 256) * delta_r ** 2 + 4 * delta_g ** 2 + (2 + (255 - r) / 256) * delta_b ** 2)
        return delta_c ** 0.5

    def hex_to_rgb(self, hex_value):
        # This method takes a hex value as an input and returns a corresponding tuple in r g b format
        hex_value = hex_value.replace('0x', '')
        r = int(hex_value[0:2], base=16)
        g = int(hex_value[2:4], base=16)
        b = int(hex_value[4:6], base=16)
        return (r, g, b)

    def inverse(self):
        rgb = self.hex_to_rgb(self.value)
        hex_value = "0x{0:02x}{1:02x}{2:02x}".format(255 - rgb[0], 255 - rgb[1], 255 - rgb[2])
        return hex_value

    def mix(self, other_color):
        # Mix the current color of object with some other color. Updates the hex value of the object.
        color_one = self.hex_to_rgb(self.value)
        color_two = self.hex_to_rgb(str(other_color).replace('#', '0x'))
        mixed_color = ((color_one[0] + color_two[0]) // 2,
                       (color_one[1] + color_two[1]) // 2,
                       (color_one[2] + color_two[2]) // 2)
        mixed_color_hex = "0x{0:02x}{1:02x}{2:02x}".format(mixed_color[0], mixed_color[1], mixed_color[2])
        self.value = mixed_color_hex

    def show(self):
        root = tkinter.Tk()
        root.title('Colory')
        root.configure(bg=self.value.replace('0x', '#'))
        hex_value = self.value.replace('0x', '#')
        foreground_color = self.inverse().replace('0x', '#')
        tkinter.Label(root, background=hex_value, justify="center",
                      text="{}\n{}\n({})".format(hex_value, self.name, self.colset),
                      padx=100, pady=100, foreground=foreground_color).pack()
        root.mainloop()

