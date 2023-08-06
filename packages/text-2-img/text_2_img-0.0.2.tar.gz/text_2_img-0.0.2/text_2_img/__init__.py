#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'text_2_img'

import os
import re
from PIL import Image, ImageDraw, ImageFont
import cjkwrap
import hashlib

def getFilename(text, dirname = 'tmp'):
    text = re.sub(r'[-\s]+', '', text)
    h = hashlib.sha224(text.encode('utf-8')).hexdigest()[:3]
    return text[:10] + '_' + h

other_font_loc = '~/Library/Fonts/SourceHanSerifSC-Light.otf' # 思源宋体

def splitText(text, line_char_max, line_max):
    text = text.strip()
    lines = []
    for line in text.split('\n'):
        new_lines = cjkwrap.fill(line, line_char_max).split('\n')
        if len(lines) + len(new_lines) > line_max:
            yield '\n'.join(lines).strip()
            lines = []
        lines += new_lines
        if not lines[0]:
            del lines[0]
    last = '\n'.join(lines).strip()
    if last:
        yield last

def gen(text, dirname = 'tmp', font_loc=other_font_loc, color=(0, 0, 0), 
        background=(252, 250, 222), img_size=(3600, 6400), margin=200,
        font_size=160, padding=10, line_char_max=40, line_max=30):
    os.system('mkdir %s > /dev/null 2>&1' % dirname)
    fn_base = dirname + '/' + getFilename(text)
    result = []
    texts = list(splitText(text, line_char_max, line_max))
    for index, subText in enumerate(texts):
        lines = subText.split('\n')
        font = ImageFont.truetype(font_loc, font_size)
        height = margin
        text_height = font.getsize(lines[0])[1]
        if len(texts) == 1:
            img_size[1] = len(lines) * (padding + text_height) + margin * 2
        img = Image.new('RGB', img_size, color=background)
        for line in lines:
            ImageDraw.Draw(img).text((margin, height), line, font=font, fill=color)
            height += text_height + padding
        fn = '%s_%d.png' % (fn_base, index)
        img.save(fn)
        result.append(fn)
    return result

