import cv2
import numpy as np
import time


class ModelVideo:
    def __init__(self, main_model):
        self.main_model = main_model

        self.ret = []
        self.cap = []
        self.main_model.data_model.properties_video = {"video": False, "streaming": False, "mode": "bird_view",
                                                       "pos_frame": 0, "frame_count": 0, "total_minute": 0,
                                                       "total_second": 0, "current_minute": 0, "current_second": 0}

        # for record video
        self.start_record = None
        self.record = False

    def initialize_video_data(self):
        self.main_model.data_model.total_camera_used = 4
        self.cap = [None] * 4
        self.ret = [None] * self.main_model.data_model.total_camera_used
        self.main_model.data_model.list_frame_video = [None] * self.main_model.data_model.total_camera_used
        self.main_model.data_model.list_frame_undistorted_video = [None] * self.main_model.data_model.total_camera_used
        self.main_model.data_model.list_perspective_video = [None] * self.main_model.data_model.total_camera_used

    def running_video(self, i, video_path):
        self.cap[i] = cv2.VideoCapture(video_path)
        self.next_frame()

    def next_frame(self):
        for i, cap in enumerate(self.cap):
            if cap is not None:
                self.ret[i], self.main_model.data_model.list_frame_video[i] = cap.read()
                # cv2.imwrite("asdavascascasc.jpg", self.main_model.data_model.list_frame_video[i])
                if self.ret[i]:
                    self.main_model.data_model.list_frame_undistorted_video[i] = self.load_maps_for_remap(
                        self.main_model.data_model.list_frame_video[i], i)
                    self.main_model.data_model.list_perspective_video[i] = self.process_perspective_image(
                        self.main_model.data_model.list_frame_undistorted_video[i], i)

                    if all(self.ret):
                        self.main_model.data_model.bird_view_video = \
                            self.main_model.process_bird_view("video")
                        self.__video_duration()
                        if self.record:
                            self.start_record.write(self.main_model.data_model.bird_view_video)

    def load_maps_for_remap(self, image, i):
        map_x = np.load(self.main_model.source_file.get_maps_x(i))
        map_y = np.load(self.main_model.source_file.get_maps_y(i))
        undistorted = cv2.remap(image, map_x, map_y,
                                interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        return undistorted

    def process_perspective_image(self, image, i):
        keys = list(self.main_model.data_model.properties_image)
        canvas = self.main_model.data_model.properties_image[keys[i]]["dst"]["Width"], \
                 self.main_model.data_model.properties_image[keys[i]]["dst"][
                     "Height"]
        matrix = np.load(self.main_model.source_file.get_matrix_perspective(i))
        perspective_image = cv2.warpPerspective(image, matrix, canvas)
        return perspective_image

    def change_mode_overlap(self, mode):
        self.main_model.data_model.properties_video["mode"] = mode
        self.main_model.update_bird_view_video()

    def stop_video(self):
        for i, cap in enumerate(self.cap):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 5)
        self.next_frame()

    def __video_duration(self):
        """
            This function is for get time of video
        Returns:

        """
        fps = self.cap[0].get(cv2.CAP_PROP_FPS)
        self.main_model.data_model.properties_video["pos_frame"] = self.cap[0].get(
            cv2.CAP_PROP_POS_FRAMES)
        self.main_model.data_model.properties_video["frame_count"] = float(
            self.cap[0].get(cv2.CAP_PROP_FRAME_COUNT))
        duration_sec = int(self.main_model.data_model.properties_video["frame_count"] / fps)

        self.main_model.data_model.properties_video["total_minute"] = int(duration_sec // 60)
        duration_sec %= 60
        self.main_model.data_model.properties_video["total_second"] = duration_sec
        sec_pos = int(self.main_model.data_model.properties_video["pos_frame"] / fps)
        self.main_model.data_model.properties_video["current_minute"] = int(sec_pos // 60)
        sec_pos %= 60
        self.main_model.data_model.properties_video["current_second"] = sec_pos

    def slider_controller(self, value, slider_maximum):
        dst = self.main_model.data_model.properties_video["frame_count"] * value / slider_maximum
        for i in range(self.main_model.data_model.total_camera_used):
            self.cap[i].set(cv2.CAP_PROP_POS_FRAMES, dst)
        self.next_frame()

    # def get_time_video(self):
    #     return self.total_minute, self.current_minute, self.total_second, self.current_second

    def get_value_slider_video(self, value):
        current_position = self.main_model.data_model.properties_video["pos_frame"] * (value + 1) / \
                           self.main_model.data_model.properties_video["frame_count"]
        return current_position

    # here need to evaluate regarding the delayed updated all frame. #######################33
    def forward_video(self):
        fps = self.cap[0].get(cv2.CAP_PROP_FPS)
        position = self.main_model.data_model.properties_video["pos_frame"] + 5 * fps
        for i in range(self.main_model.data_model.total_camera_used):
            self.cap[i].set(cv2.CAP_PROP_POS_FRAMES, position)
        self.next_frame()

    def rewind_video(self):
        fps = self.cap[0].get(cv2.CAP_PROP_FPS)
        position = self.main_model.data_model.properties_video["pos_frame"] - 5 * fps
        for i in range(self.main_model.data_model.total_camera_used):
            self.cap[i].set(cv2.CAP_PROP_POS_FRAMES, position)
        self.next_frame()

    def initial_record(self):
        h, w, _ = self.main_model.data_model.bird_view_video.shape
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        self.start_record = cv2.VideoWriter("../saved/Videos_saved/video.avi", fourcc, 5, (w, h))
