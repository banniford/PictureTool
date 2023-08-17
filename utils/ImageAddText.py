from PIL import Image, ImageDraw, ImageFont

FontPosition = {"右上角": "right", "右下角": "right", "左上角": "left", "左下角": "left"}
def ImageAddText(img_path, text, text_color, text_size, position):
    img = Image.open(img_path)
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