import numpy as np
import cv2 as cv
import math


class Image:
    def __init__(self):
        self.img = None
        self.watermark = None
        self.code = False
        self.decode = False
        self.is_watermark = False

    def set_value(self, bytes_img: bytes):
        pre_img = np.frombuffer(bytes_img, dtype=np.uint8)
        self.img = cv.imdecode(pre_img, cv.IMREAD_UNCHANGED)

    def show(self):
        if self.img:
            cv.imshow("img", self.img)
            cv.waitKey(0)
        else:
            print("Image value is none")

    def set_watermark(self, bytes_watermark: bytes):
        pre_watermark = np.frombuffer(bytes_watermark, dtype=np.uint8)
        self.watermark = cv.imdecode(pre_watermark, cv.IMREAD_UNCHANGED)

        pre_mask = np.empty_like(self.img)
        water_wight = self.watermark.shape[0]
        water_height = self.watermark.shape[1]

        for i in range(math.ceil(self.img.shape[0] / water_wight)):

            if (i + 1) * water_wight > self.img.shape[0]:
                border_width = self.img.shape[0]
            else:
                border_width = (i + 1) * water_wight

            for j in range(math.ceil(self.img.shape[1] / water_height)):

                if (j + 1) * water_height > self.img.shape[1]:
                    border_height = self.img.shape[1]
                else:
                    border_height = (j + 1) * water_height

                pre_mask[i * water_wight: border_width, j * water_height:border_height] = \
                    self.watermark[0: border_width - i * water_wight, 0: border_height - j * water_height]

        gray_mask = cv.cvtColor(pre_mask, cv.COLOR_BGR2GRAY)
        (_, bw_mask) = cv.threshold(gray_mask,
                                    127,
                                    255,
                                    cv.THRESH_BINARY)
        mask = bw_mask // 255

        red_chanel = self.img[:, :, 1] % 2
        self.img[:, :, 1] += -red_chanel + mask.astype('uint8')
        _, img_encode = cv.imencode(".jpg", self.img)
        return img_encode.tobytes()

    def get_watermark(self, bytes_img: bytes):
        self.set_value(bytes_img)
        red_chanel = self.img[:, :, 1]%2
        get_watermark_img = (red_chanel*255).astype('uint8')
        _, get_watermark_img_encode = cv.imencode(".jpg", get_watermark_img)
        return get_watermark_img_encode.tobytes()