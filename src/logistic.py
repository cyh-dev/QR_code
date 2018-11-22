import numpy as np
from PIL import Image
import cv2

'''
加密:
	-key: 密钥
	-imgpath: 待加密图像路径
	-start: 将生成的混沌序列，从第start个之后开始作为加密用序列
'''


def encryption(key, img, start=500, x0=0.1):
    if key > 4 or key < 3.57:
        print('[Error]: Key must between <3.57-4>...')
        return None
    if x0 >= 1 or x0 <= 0:
        print('[Error]: x0 must between <0-1>...')
        return None

    img_en = Image.new(mode=img.mode, size=img.size)
    width, height = img.size
    chaos_seq = np.zeros(width * height)
    for _ in range(start):
        x = key * x0 * (1 - x0)
        x0 = x
    for i in range(width * height):
        x = key * x0 * (1 - x0)
        x0 = x
        chaos_seq[i] = x
    idxs_en = np.argsort(chaos_seq)
    i, j = 0, 0
    for idx in idxs_en:
        col = int(idx % width)
        row = int(idx // width)
        img_en.putpixel((i, j), img.getpixel((col, row)))
        i += 1
        if i >= width:
            j += 1
            i = 0
    # img_en.save('encryption.%s' % imgpath.split('.')[-1], quality=100)
    data = img_en.getdata()

    data = np.array(data,dtype=int)

    new_data = np.reshape(data, (width, height))

    return new_data



'''
解密:
	-key: 密钥
	-imgpath: 待解密图像路径
	-start: 将生成的混沌序列，从第start个之后开始作为解密用序列
'''


def decryption(key, img, start=500, x0=0.1):
    if key > 4 or key < 3.57:
        print('[Error]: Key must between <3.57-4>...')
        return None
    if x0 >= 1 or x0 <= 0:
        print('[Error]: x0 must between <0-1>...')
        return None

    img_de = Image.new(img.mode, img.size)
    width, height = img.size
    chaos_seq = np.zeros(width * height)
    for _ in range(start):
        x = key * x0 * (1 - x0)
        x0 = x
    for i in range(width * height):
        x = key * x0 * (1 - x0)
        x0 = x
        chaos_seq[i] = x
    idxs_de = np.argsort(chaos_seq)
    i, j = 0, 0
    for idx in idxs_de:
        col = int(idx % width)
        row = int(idx // width)
        img_de.putpixel((col, row), img.getpixel((i, j)))
        i += 1
        if i >= width:
            j += 1
            i = 0

    # img_de.save('decryption.%s' % imgpath.split('.')[-1], quality=100)
    data = img_de.getdata()
    data = np.array(data)
    new_data = np.reshape(data, (width, height))

    return new_data


if __name__ == '__main__':
    path = 'watermark.png'

    image = cv2.imread(path, 0)

    image = image/255


    print(image)

    img = Image.fromarray(image)


    img=encryption(key=3.8,img=img)

    cv2.imshow('2',img)

    print(img)

    img = Image.fromarray(img)

    img = decryption(key=3.8,img=img)

    cv2.imshow('3', img)

    print(img)





