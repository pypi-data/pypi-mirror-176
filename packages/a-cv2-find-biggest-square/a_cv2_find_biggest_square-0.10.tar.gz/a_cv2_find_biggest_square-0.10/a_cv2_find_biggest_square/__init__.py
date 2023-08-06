from typing import Any
import cv2
from a_cv_imwrite_imread_plus import open_image_in_cv
import numpy as np


def find_largest_square(
    image: Any,
    scale_percent: int = 30,
    gaussian_blur: int = 4,
    draw_result: bool = True,
) -> tuple:
    # based on https://stackoverflow.com/questions/64369800/how-to-find-the-largest-blankwhite-square-area-in-the-doc-and-return-its-coord
    im = open_image_in_cv(image, channels_in_output=2).copy()
    width = int(im.shape[1] * scale_percent / 100)
    height = int(im.shape[0] * scale_percent / 100)
    dim = (width, height)
    im = cv2.resize(im.copy(), dim, interpolation=cv2.INTER_AREA)

    im = cv2.adaptiveThreshold(
        im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, gaussian_blur,
    )
    work = im.copy()
    p = np.zeros(work.shape, np.uint16)

    for i in range(1, im.shape[0]):
        for j in range(1, im.shape[1]):
            if work[i][j] > 0:
                p[i][j] = min(p[i][j - 1], p[i - 1][j], p[i - 1][j - 1]) + 1
            else:
                p[i][j] = 0

    ind = np.unravel_index(np.argmax(p, axis=None), p.shape)
    locationbeginning = (ind[0] - p[ind]), (ind[1] - p[ind])
    locationend = ind[0], ind[1]
    sidelength = p[ind]

    lsq = (
        int(locationbeginning[1] * 100 / scale_percent),
        int(locationbeginning[0] * 100 / scale_percent),
        int(locationend[1] * 100 / scale_percent),
        int(locationend[0] * 100 / scale_percent),
    )
    imi = None
    if draw_result:
        imi = open_image_in_cv(image).copy()
        imi = cv2.rectangle(imi, (lsq[0], lsq[1]), (lsq[2], lsq[3]), (0, 0, 255), 2,)
    return lsq, imi, sidelength


def add_find_biggest_square_to_cv2():
    cv2.find_largest_square = find_largest_square
