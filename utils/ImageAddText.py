from PIL import Image, ImageDraw, ImageFont, ExifTags

FontPosition = {"右上角": "right", "右下角": "right", "左上角": "left", "左下角": "left"}
def ImageAddText(img_path, text, text_color, text_size, position):
    # 打开图片
    img = Image.open(img_path)
    # 校验exif信息
    # 检查是否存在 EXIF 信息
    if hasattr(img, '_getexif'):
        exif = img._getexif()
        if exif is not None:
            for tag, value in exif.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                if tag_name == 'Orientation':
                    # 如果存在 Orientation 标签，则根据标签值进行旋转
                    if value == 3:
                        img = img.rotate(180, expand=True)
                    elif value == 6:
                        img = img.rotate(-90, expand=True)
                    elif value == 8:
                        img = img.rotate(90, expand=True)
                    break  # 一旦找到 Orientation 标签，就不需要再继续查找

    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式 这里的SimHei.ttf需要有这个字体
    fontStyle = ImageFont.truetype("./assets/font/simhei.ttf", text_size, encoding="utf-8")
    # 计算坐标
    if position=="右下角":
        left = img.size[0]-draw.textsize(text,font=fontStyle)[0]-30
        top = img.size[1]-draw.textsize(text,font=fontStyle)[1]-30
    elif position=="左下角":
        left = 30
        top = img.size[1]-draw.textsize(text,font=fontStyle)[1]-30
    elif position=="左上角":
        left = 30
        top = 30
    else:
        # 默认"右上角"
        left = img.size[0] - draw.textsize(text, font=fontStyle)[0] - 30
        top = 30
    # 绘制文本
    draw.text((left, top), text, text_color, font=fontStyle, align=FontPosition[position])
    return img