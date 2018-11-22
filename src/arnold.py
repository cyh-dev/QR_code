import copy
import cv2
import numpy as np


def show_img(img, title='TEST'):
    cv2.imshow(title, img)
    cv2.waitKey(0)


def arnold(img, key):
    N, a, b, c, d = key

    h, w = img.shape[: 2]
    new_img = copy.deepcopy(img)
    # 置换N次
    for i in range(N):
        for x in range(h):
            for y in range(w):
                nx = ((a * x + b * y) % w + w) % w
                ny = ((c * x + d * y) % w + w) % w
                nx = int(nx)
                ny = int(ny)
                new_img[nx, ny] = img[x, y]
        img = copy.deepcopy(new_img)
    return new_img


def iarnold(img, key):
    N, a, b, c, d = key
    # 求矩阵逆
    matrix = np.mat([[a, b], [c, d]]).I
    # 精度问题
    [[a, b], [c, d]] = matrix.tolist()
    return arnold(img, [N, a, b, c, d])


if __name__ == '__main__':
    path='watermark.png'
    image = cv2.imread(path, 0)

    image = image/255

    cv2.imshow('1',image)

    SCRAMBLING_KEY=[15, 1, 1, 1, 2]

    img=arnold(image,SCRAMBLING_KEY)

    cv2.imshow('2', img)

    img=iarnold(img=img,key=SCRAMBLING_KEY)

    cv2.imshow('3', img)

    cv2.waitKey(0)





