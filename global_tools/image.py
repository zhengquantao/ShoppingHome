"""
随机生成图片，用于验证
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import string


def color1():  # 图片颜色
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


def color2():  # 字体颜色
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


def img():
    num = random.sample(string.digits, 4)
    width = 240  # 宽
    height = 60  # 高
    image = Image.new("RGB", (width, height), (255, 255, 255))
    font = ImageFont.truetype("arial.ttf", 36)  # font对象
    draw = ImageDraw.Draw(image)  # 创建Draw对象
    for x in range(width):  # 填充像素
        # for y in range(30, random.randint(20, 40)):
        draw.point((x, 30), fill=color1())
    for w in range(4):  # 输出文字
        draw.text((60*w + 10, 10), num[w], font=font, fill=color2())
    image = image.filter(ImageFilter.DETAIL)
    image.save('./static/images/code.jpg')
    return num

