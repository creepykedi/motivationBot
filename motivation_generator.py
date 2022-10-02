import platform
import numpy
from PIL import Image, ImageDraw,ImageFont
import random
import glob
import textwrap

tall_fonts = ['fonts\Pattaya-Regular.ttf']


def switch_colors(avg_color):
    if all(avg_color > 105):
        fill = (35, 35, 35)
    else:
        fill = (247, 247, 247)
    return fill


def write_to_image(text: str, sender):
    # get random image from /backgrounds
    if sender.forward_from and sender.forward_from.first_name:
        sender = sender.forward_from.first_name
    elif sender.forward_sender_name:
        sender = sender.forward_sender_name
    else:
        sender = 'Michael Scott'
    imgs: list = glob.glob('backgrounds/*')
    image: str = random.choice(imgs)
    img: Image = Image.open(image)

    # pick random font
    fonts = glob.glob('fonts/*')
    if not text.isascii():  # remove non-cyrilic fonts
        separator = '\\' if not platform.system() == 'Linux' else '/'
        fonts.remove(f'fonts{separator}PassionsConflict-Regular.ttf')
    font: str = random.choice(fonts)

    # calculate font_size proportional to image size
    width, height = img.size
    font_size: int = int(width / 16)
    position: tuple = (width // 7, height // 3)

    type_font: ImageFont = ImageFont.truetype(font, size=font_size)

    max_chars_width: int = int((width-(width/3))/(font_size/2))
    #print(f"{width} width, {max_chars_width} max_chars_width")

    draw = ImageDraw.Draw(img)
    last_position_height: int = int(position[1]+font_size+font_size/1.5+font_size)
    wrapper = textwrap.TextWrapper(width=max_chars_width)

    if len(text) > max_chars_width:
        text_wrapped = wrapper.wrap(text=text)
        lines_amt = len(text_wrapped)
        needed_height = int(last_position_height + lines_amt*(font_size+font_size/1.5+font_size))
        while needed_height > height or font_size<10:
            font_size //= 1.1
            needed_height = int(last_position_height + lines_amt * (font_size + font_size / 1.5 + font_size))
        for line in text_wrapped:
            # getting box where text will be written
            img_crop = img.crop((width / 7, last_position_height, width-width/5, last_position_height+font_size))
            # view image
            # img_crop.show()
            avg_color_per_row = numpy.average(img_crop, axis=0)
            avg_color = numpy.average(avg_color_per_row, axis=0)
            fill = switch_colors(avg_color)
            draw.text(position, line, font=type_font, fill=fill)
            position = (position[0], position[1]+font_size*2+font_size/1.5)
            if font in tall_fonts:
                position = (position[0], position[1]+font_size)
            last_position_height = position[1]
    else:
        img_crop = img.crop((width / 7, last_position_height, width - width / 5, last_position_height + font_size))
        # view image
        # img_crop.show()
        avg_color_per_row = numpy.average(img_crop, axis=0)
        avg_color = numpy.average(avg_color_per_row, axis=0)
        fill = switch_colors(avg_color)
        draw.text(position, text, font=type_font, fill=fill)
    img_crop = img.crop((width / 7, last_position_height, width - width / 5, last_position_height + font_size))
    avg_color_per_row: float = numpy.average(img_crop, axis=0)
    avg_color: float = numpy.average(avg_color_per_row, axis=0)
    fill = switch_colors(avg_color)
    last_position: tuple = width//7, last_position_height
    draw.text(last_position, f"— {sender}", font=type_font, fill=fill)
    # make image smaller
    img = img.resize((int(width/2), int(height/2)))
    i = img.save('result.jpg')
    return i