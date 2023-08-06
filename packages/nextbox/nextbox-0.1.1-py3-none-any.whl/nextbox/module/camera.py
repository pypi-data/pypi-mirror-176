import cv2
import numpy as np
import time
import os
from loguru import logger


class Camera:
    def __init__(self, uri, record_dir=None):
        self._uri = uri
        # 连续尝试重连最大次数
        self.re_conn_max_times = 5
        self.cap = cv2.VideoCapture(self._uri)
        self.record_dir = record_dir

        # 摄像头宽高信息
        self.w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 当前帧
        self._frame = None
        self._frame_at = time.time_ns()

    def is_open(self):
        return self.cap.isOpened()

    def release(self):
        logger.info("release")
        self.cap.release()

    def _re_conn(self):
        """
        TODO 断线重连机制
        :return:
        """
        pass

    def _read(self):
        """
        读取摄像头画面
        :return:
        """
        ret, self._frame = self.cap.read()
        self._frame_at = time.time_ns()

        # 尝试重连
        re_conn_times = 0
        while not ret:
            if re_conn_times > self.re_conn_max_times:
                raise Exception(f"camera {self._uri} connect error!")
            # 尝试重连
            self._re_conn()
            ret, self._frame = self.cap.read()
            self._frame_at = time.time_ns()
            re_conn_times += 1

        return self._frame, self._frame_at

    def read(self):
        """
        读取摄像头画面
        :return:
        """
        frame, time_at_ns = self._read()
        return frame

    def take_picture(self):
        """
        拍摄画面
        :return:
        """
        logger.info("take_picture")
        if self.record_dir:
            # 初始化目录
            dir = os.path.join(self.record_dir, "pic")
            os.makedirs(dir, exist_ok=True)

            fp = os.path.join(dir, f"{self._frame_at}.jpg")
            cv2.imwrite(fp, self._frame)
        else:
            raise Exception(f"record_dir is {self.record_dir}, please set!")

    def show(self):
        while self.is_open():
            frame = self.read()
            cv2.imshow('frame', frame)  # 显示读取到的这一帧画面
            key = cv2.waitKey(25)  # 等待一段时间，并且检测键盘输入
            if key == ord(' '):
                # 拍照
                c.take_picture()
            elif key == ord('q'):  # 若是键盘输入'q',则退出，释放视频
                # 退出
                c.release()  # 释放视频
                break


class MaskedCamera(Camera):
    """
    带有mask信息的摄像头
    """

    def __init__(self, uri, mask_points=[], record_dir=None):
        super().__init__(uri, record_dir)

        if mask_points and len(mask_points) > 0:
            points = [[int(p[0]), int(p[1])] for p in mask_points]
            self.mask = cv2.fillPoly(np.zeros(shape=(self.h, self.w), dtype=np.uint8), [np.array(points)], 1)
        else:
            self.mask = np.ones(shape=(self.h, self.w), dtype=np.uint8)

    def take_picture(self, with_mask=True):
        # TODO 带有mask信息的拍照
        self.take_picture()


if __name__ == '__main__':
    c = Camera(uri=1, record_dir="record")
    c.show()
