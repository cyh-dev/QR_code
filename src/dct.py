import numpy as np
import cv2
from PIL import Image

from src.arnold import arnold, iarnold
from src.logistic import encryption, decryption


def dct(a):

    m, n = a.shape

    hdata = np.vsplit(a, n / 8)  # 垂直分成高度度为8 的块

    v = None
    for i in range(0, n // 8):
        blockdata = np.hsplit(hdata[i], m / 8)

        h = None
        # 垂直分成高度为8的块后,在水平切成长度是8的块, 也就是8x8 的块
        for j in range(0, m // 8):
            block = blockdata[j]
            Yb = cv2.dct(block.astype(np.float))
            Y = cv2.idct(Yb)
            if h is None:
                h=Yb

            else:
                h=np.hstack((h,Yb))

        if v is None:
            v=h
        else:
            v=np.vstack((v,h))

    return v


def idct(a):
    # a = cv2.imread(img_path, 0)
    m, n = a.shape

    hdata = np.vsplit(a, n / 8)  # 垂直分成高度度为8 的块

    v = None
    for i in range(0, n // 8):
        blockdata = np.hsplit(hdata[i], m / 8)

        h = None
        # 垂直分成高度为8的块后,在水平切成长度是8的块, 也就是8x8 的块
        for j in range(0, m // 8):
            block = blockdata[j]
            Yb = cv2.idct(block.astype(np.float))

            if h is None:
                h=Yb
            else:
                h=np.hstack((h,Yb))

        if v is None:
            v=h
        else:
            v=np.vstack((v,h))

    return v


def insert_msg(qr_path,wa_path):

    a = cv2.imread(qr_path, 0)

    a = a / 255

    y1 = dct(a)  # 加密后图像矩阵

    image = cv2.imread(wa_path, 0)

    image = image / 255

    img = Image.fromarray(image)

    img = encryption(key=3.8, img=img)

    SCRAMBLING_KEY = [15, 1, 1, 1, 2]

    watermark = arnold(img, SCRAMBLING_KEY)


    m,n=y1.shape
    hdata = np.vsplit(y1, n / 8)
    for index,vdata in enumerate(hdata):
        hdata[index] = np.hsplit(vdata, m / 8)

    w = None

    for i in range(int(m/8)):
        h = None

        for j in range(int(n/8)):

            m0=np.zeros((2,2))
            m0[0][0] = hdata[i][j][3][3]
            m0[0][1] = hdata[i][j][3][4]
            m0[1][0] = hdata[i][j][4][3]
            m0[1][1] = hdata[i][j][4][4]
            u, s, v = np.linalg.svd(m0)
            x=watermark[i][j]
            temp=np.zeros((2,2))
            temp[0][0]=x*1
            m1=u*(temp+s)*v
            hdata[i][j][3][3] = m1[0][0]
            hdata[i][j][3][4] = m1[0][1]
            hdata[i][j][4][3] = m1[1][0]
            hdata[i][j][4][4] = m1[1][1]

            if h is None:
                h = hdata[i][j]
            else:
                h = np.hstack((h, hdata[i][j]))

        if w is None:
            w=h

        else:

            w=np.vstack((w,h))

    return w


def get_watermark(qr_path,en_qr_path):
    qr = cv2.imread(qr_path, 0)/255
    en_qr = cv2.imread(en_qr_path, 0)/255

    dct_qr = dct(qr)
    dct_en_qr = dct(en_qr)

    m, n = dct_qr.shape

    qr_data = np.vsplit(dct_qr, n / 8)
    for index, vdata in enumerate(qr_data):
        qr_data[index] = np.hsplit(vdata, m / 8)

    en_qr_data = np.vsplit(dct_en_qr, n / 8)
    for index, vdata in enumerate(en_qr_data):
        en_qr_data[index] = np.hsplit(vdata, m / 8)

    w = None

    watermark = np.zeros((int(m/8),int(n/8)))

    for i in range(int(m / 8)):
        h = None
        for j in range(int(n / 8)):

            m0 = np.zeros((2, 2))
            m0[0][0] = qr_data[i][j][3][3]
            m0[0][1] = qr_data[i][j][3][4]
            m0[1][0] = qr_data[i][j][4][3]
            m0[1][1] = qr_data[i][j][4][4]

            m1 = np.zeros((2, 2))
            m1[0][0] = en_qr_data[i][j][3][3]
            m1[0][1] = en_qr_data[i][j][3][4]
            m1[1][0] = en_qr_data[i][j][4][3]
            m1[1][1] = en_qr_data[i][j][4][4]

            u, s, v = np.linalg.svd(m0)
            u1, s1, v1 = np.linalg.svd(m1)

            watermark[i][j]=(s1[0]+s1[1]-s[1]-s[0])/1


    SCRAMBLING_KEY = [15, 1, 1, 1, 2]
    watermark = iarnold(watermark,SCRAMBLING_KEY)

    watermark = Image.fromarray(watermark)

    watermark = decryption(img=watermark,key=3.8)

    watermark = watermark * 255
    watermark = np.array(watermark, dtype=np.int)

    for i in range(m):
        for j in range(n):
            if watermark[i][j] > 0:
                watermark[i][j] = 255
            else:
                watermark[i][j] = 0

    return watermark



if __name__ == '__main__':
    qr_path = 'QR_code.png'
    en_qr_path = 'en_QR_code.png'
    wa_path = 'watermark.png'

    en_img=insert_msg(qr_path,wa_path)

    new_img=idct(en_img)

    watermark=get_watermark(qr_path,en_qr_path)

    cv2.imwrite('watermark1.png', watermark)




















