import numpy as np
import cv2 as cv


class Image:
    def __init__(self, bytes_img: bytes):
        pre_img = np.frombuffer(bytes_img, dtype=np.uint8)
        self.img = cv.imdecode(pre_img, cv.IMREAD_UNCHANGED)

    def reset_img(self, bytes_img: bytes):
        pre_img = np.frombuffer(bytes_img, dtype=np.uint8)
        self.img = cv.imdecode(pre_img, cv.IMREAD_UNCHANGED)


