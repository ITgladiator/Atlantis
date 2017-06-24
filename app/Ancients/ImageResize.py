#! /usr/bin/env python
# ^_^ coding: utf-8 ^_^

from PIL import Image, ImageDraw, ImageFont
from cStringIO import StringIO


def imageResize(**kwargs):
    width = kwargs.get('width') or 900
    height = kwargs.get('height') or 300
    src_img = kwargs.get('src_img')
    out_path = kwargs.get('out_path')
    with open(out_path, 'wb') as f:
        im = Image.open(StringIO(src_img))
        ori_w, ori_h = im.size
        if (ori_w and ori_w > width) or (ori_h and ori_h > height):
            if width and ori_w > width:
                widthRatio = float(width) / ori_w  # 正确获取小数的方式
            else:
                widthRatio = 1
            if height and ori_h > height:
                heightRatio = float(height) / ori_h

            if widthRatio and heightRatio:
                if widthRatio < heightRatio:
                    ratio = widthRatio
                else:
                    ratio = heightRatio

            if widthRatio and not heightRatio:
                ratio = widthRatio
            if heightRatio and not widthRatio:
                ratio = heightRatio

            newWidth = int(ori_w * ratio)
            newHeight = int(ori_h * ratio)
        else:
            newWidth = ori_w
            newHeight = ori_h
        im = im.resize((newWidth, newHeight), Image.ANTIALIAS)
        im_file = StringIO()
        draw = ImageDraw.Draw(im)
        draw.text((newWidth-80, newHeight-20), "Atlantis", (255, 255, 255, 255))
        im.save(im_file, format='png')
        im_data = im_file.getvalue()
        f.write(im_data)


# 裁剪压缩图片
def clipResizeImg(**kwargs):
    args_key = {'ori_img': '', 'dst_img': '', 'dst_w': '', 'dst_h': '', 'save_q': 75}
    arg = {}
    for key in args_key:
        if key in kwargs:
            arg[key] = kwargs[key]

    im = Image.open(arg['ori_img'])
    ori_w, ori_h = im.size

    dst_scale = float(arg['dst_h']) / arg['dst_w']  # 目标高宽比
    ori_scale = float(ori_h) / ori_w  # 原高宽比

    if ori_scale >= dst_scale:
        # 过高
        width = ori_w
        height = int(width * dst_scale)

        x = 0
        y = (ori_h - height) / 3

    else:
        # 过宽
        height = ori_h
        width = int(height * dst_scale)

        x = (ori_w - width) / 2
        y = 0

    # 裁剪
    box = (x, y, width + x, height + y)
    # 这里的参数可以这么认为：从某图的(x,y)坐标开始截，截到(width+x,height+y)坐标
    # 所包围的图像，crop方法与php中的imagecopy方法大为不一样
    newIm = im.crop(box)
    im = None

    # 压缩
    ratio = float(arg['dst_w']) / width
    newWidth = int(width * ratio)
    newHeight = int(height * ratio)
    newIm.resize((newWidth, newHeight), Image.ANTIALIAS).save(arg['dst_img'], quality=arg['save_q'])