from PIL import Image as image
import numpy as np
from matplotlib import pyplot as plt
import math


def getinput():
    filename = input()
    # outputname = input()
    im = 0
    try:
        im = image.open(filename)
    except FileNotFoundError:
        try:
            im = image.open(filename + ".jpg")
        except FileNotFoundError:
            try:
                im = image.open(filename + ".png")
            except FileNotFoundError:
                try:
                    im = image.open(filename + ".bmp")
                except FileNotFoundError:
                    print("file not exist")
                    exit(1)

    plt.figure(figsize=(10, 10))
    plt.imshow(im)
    left = plt.ginput(1)
    right = plt.ginput(1)

    return {'x1': int(left[0][0] + 0.5),
            'x2': int(right[0][0] + 0.5),
            'y1': int(left[0][1] + 0.5),
            'y2': int(right[0][1] + 0.5),
            'file': im,
            'output': filename + "_x_.bmp"}


def rot(center, point, theta):
    theta = -theta
    a = point - center
    b = np.array([[math.cos(theta), -math.sin(theta)],
                  [math.sin(theta), math.cos(theta)]])
    a = b.dot(a)
    return a + center


def dis(a, b):
    a = a - b
    a = np.power(a, 2)
    return math.sqrt(a.sum())


def main():
    showred = False
    rgb2gray = True
    inf = getinput()
    x1 = inf['x1']
    y1 = inf['y1']
    x2 = inf['x2']
    y2 = inf['y2']
    im = inf['file']
    name = inf['output']
    theta = math.atan2(y2 - y1, x2 - x1)
    im = im.rotate(theta / math.pi * 180.0)
    imp = np.array(im)
    center = np.array([[int(imp.shape[1] / 2.0 + 0.5)], [int(imp.shape[0] / 2.0 + 0.5)]])
    leftEye = np.array([[x1], [y1]])
    rightEye = np.array([[x2], [y2]])
    leftEye = (rot(center, leftEye, theta) + 0.5).astype(int)
    rightEye = (rot(center, rightEye, theta) + 0.5).astype(int)
    distance = dis(leftEye, rightEye)
    k = 32.0 / distance
    nx = int(imp.shape[1] * k + 0.5)
    ny = int(imp.shape[0] * k + 0.5)
    im = im.resize((nx, ny))
    leftEye = (leftEye * k + 0.5).astype(int)
    rightEye = (rightEye * k + 0.5).astype(int)
    newpic = np.array(im)
    if showred:
        newpic[leftEye[1], leftEye[0], 0] = 255
        newpic[leftEye[1], leftEye[0], 1] = 0
        newpic[leftEye[1], leftEye[0], 2] = 0

        newpic[rightEye[1], rightEye[0], 0] = 255
        newpic[rightEye[1], rightEye[0], 1] = 0
        newpic[rightEye[1], rightEye[0], 2] = 0
    newpic = newpic[int(leftEye[1] - 14):int(leftEye[1] + 50), int(leftEye[0] - 16):int(rightEye[0] + 16), :]
    ret = image.fromarray(newpic)
    if (rgb2gray):
        ret = ret.convert('L')
    ret.save(name)


if __name__ == '__main__':
    main()

#a (1)
#a (1)