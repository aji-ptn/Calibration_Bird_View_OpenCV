"""
This class is to showing multiple streaming video using opencv and multithreading.

Writer: aji-ptn
Last updated : 04/07/2022
Under copyright: MOIL-Org
"""
import os
import sys

import cv2
import numpy as np
from threading import Thread


class VStream:
    def __init__(self, src):
        self.capture = cv2.VideoCapture(src)
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while True:
            _, self.frame = self.capture.read()

    def get_frame(self):
        return self.frame


class main_program():
    def __init__(self):
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.record = False
        self.num = 0
        self.set_record()
        # self.cam1 = VStream("http://192.168.103.211:8000/stream.mjpg")
        # self.cam2 = VStream("http://192.168.103.18:8000/stream.mjpg")
        # self.cam3 = VStream("http://192.168.103.211:8000/stream.mjpg")
        # self.cam4 = VStream("http://192.168.103.211:8000/stream.mjpg")
        self.cam1 = VStream("http://10.42.0.31:8000/stream.mjpg")
        # self.cam2 = VStream("http://10.42.0.251:8000/stream.mjpg")
        # self.cam3 = VStream("http://10.42.0.251:8000/stream.mjpg")
        # self.cam4 = VStream("http://10.42.0.251:8000/stream.mjpg")

        # 'http://10.42.0.251:8000/stream.mjpg'

        while True:
            try:
                myFrame1 = self.cam1.get_frame()
                # myFrame2 = self.cam2.get_frame()
                # myFrame3 = self.cam3.get_frame()
                # myFrame4 = self.cam4.get_frame()
                # myFrameH1 = np.hstack((myFrame1, myFrame2))
                # myFrameH2 = np.hstack((myFrame3, myFrame4))
                # myFrame = np.vstack((myFrameH1, myFrameH2))
                myFrame = cv2.resize(myFrame1, (640, 480), cv2.INTER_AREA)
                # if self.record:
                #     print("record")
                #     self.out1.write(myFrame1)
                #     self.out2.write(myFrame2)
                #     self.out3.write(myFrame3)
                #     self.out4.write(myFrame4)
                cv2.imshow("video", myFrame)
            except:

                print("not from available")
            if cv2.waitKey(1) == ord('q'):
                self.cam1.capture.release()
                # self.cam2.capture.release()
                # self.cam3.capture.release()
                # self.cam4.capture.release()
                cv2.destroyAllWindows()
                exit(1)
                break
            elif cv2.waitKey(90) == ord("a"):
                cv2.imwrite("images/cam_13_" + str(self.num) + ".jpg", self.cam1.get_frame())
                # cv2.imwrite("images/image2.jpg", self.cam2.get_frame())
                # cv2.imwrite("images/image3.jpg", self.cam3.get_frame())
                # cv2.imwrite("images/image4.jpg", self.cam4.get_frame())
                self.num += 1
                print("save")

    def set_record(self):
        h = 1944
        w = 2592
        self.out1 = cv2.VideoWriter("Videos/video_1.avi", self.fourcc, 10, (w, h))
        self.out2 = cv2.VideoWriter('Videos/video_2.avi', self.fourcc, 10, (w, h))
        self.out3 = cv2.VideoWriter('Videos/video_3.avi', self.fourcc, 10, (w, h))
        self.out4 = cv2.VideoWriter('Videos/video_4.avi', self.fourcc, 10, (w, h))


if __name__ == "__main__":
    main_program()