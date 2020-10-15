import cv2
import numpy as np
import math

BORDER_WIDTH = 20
BORDER_COLOR = np.array([0, 0, 0])

COLOR_WIDTH = 200
COLOR_HEIGHT = 200


def random_color():
    # return np.random.randint(0, 255, 3).astype('uint8')
    return np.random.randint(128, 255, 3).astype('uint8')


def generate_random_map(width, height, border_size, show=False, savepath=None):
    img = np.zeros((height, width, 3)).astype('uint8')
    print(img.shape)

    # 绘制随机的底色块
    for i in range(math.ceil(height / COLOR_WIDTH)):
        for j in range(math.ceil(width / COLOR_HEIGHT)):
            x_end = (i + 1) * COLOR_WIDTH if (i + 1) * COLOR_WIDTH < height else height
            y_end = (j + 1) * COLOR_HEIGHT if (j + 1) * COLOR_HEIGHT < width else width
            img[i * COLOR_WIDTH: x_end, j * COLOR_HEIGHT: y_end, :] = random_color()

    # 绘制地图边缘线
    border_dx = (height - border_size[1]) // 2
    border_dy = (width - border_size[0]) // 2
    img[border_dx - BORDER_WIDTH: border_dx,
        border_dy - BORDER_WIDTH: width - border_dy + BORDER_WIDTH, :] = BORDER_COLOR
    img[height - border_dx: height - border_dx + BORDER_WIDTH,
        border_dy - BORDER_WIDTH: width - border_dy + BORDER_WIDTH, :] = BORDER_COLOR
    img[border_dx - BORDER_WIDTH: height - border_dx + BORDER_WIDTH,
        border_dy - BORDER_WIDTH: border_dy, :] = BORDER_COLOR
    img[border_dx - BORDER_WIDTH: height - border_dx + BORDER_WIDTH,
        width - border_dy: width - border_dy + BORDER_WIDTH, :] = BORDER_COLOR

    # 显示图片
    if show:
        cv2.imshow('map', img)
        cv2.waitKey(0)
        cv2.destroyWindow('map')

    # 保存图片
    if savepath:
        cv2.imwrite(savepath, img)

    return img


if __name__ == '__main__':
    width = 1000
    height = 1200
    border_size = np.array([800, 1000])

    generate_random_map(width, height, border_size, show=True, savepath='map.png')
