from PyQt5 import QtCore
from .additional_function import select_file, init_ori_ratio, show_image_to_label


class UiVideoController:
    def __init__(self, view_controller):
        self.view_controller = view_controller

        self.__timer = QtCore.QTimer()
        self.__timer.timeout.connect(self.showing_to_ui)

        self.connect_button()

    # def se

    def connect_button(self):
        self.view_controller.main_ui.btn_load_video_sources.clicked.connect(self.open_video_sources)
        self.view_controller.main_ui.btn_play_pause.clicked.connect(self.play_pause_video)
        self.view_controller.main_ui.btn_stop.clicked.connect(self.onclick_stop_video)
        self.view_controller.main_ui.slider_video.valueChanged.connect(self.change_value_slider)

        self.view_controller.main_ui.btn_zoom_out_video.clicked.connect(self.view_controller.show_to_ui.
                                                                        zoom_out_bird_view_video)
        self.view_controller.main_ui.btn_zoom_in_video.clicked.connect(self.view_controller.show_to_ui.
                                                                       zoom_in_bird_view_video)
        self.view_controller.main_ui.btn_skip_video.clicked.connect(self.view_controller.controller.video_controller.forward_video)
        self.view_controller.main_ui.btn_prev_video.clicked.connect(self.view_controller.controller.video_controller.rewind_video)

        self.view_controller.main_ui.btn_Full_view.clicked.connect(self.show_full_video)

        self.view_controller.main_ui.radioButton_horizontal_video.clicked.connect(self.onclick_change_mode_overlap)
        self.view_controller.main_ui.radioButton_vertical_video.clicked.connect(self.onclick_change_mode_overlap)
        self.view_controller.main_ui.radioButton_diagonal_video.clicked.connect(self.onclick_change_mode_overlap)
        self.view_controller.main_ui.radioButton_overlap_video.clicked.connect(self.onclick_change_mode_overlap)

    def play_pause_video(self):
        if self.view_controller.main_ui.btn_play_pause.isChecked():
            self.__timer.start()
            print("start")
        else:
            self.__timer.stop()
            print("pause")

    def open_video_sources(self):
        self.view_controller.controller.video_controller.initialize_video_data()

        filepath_video = ["/home/aji/Downloads/sequence_video/7/video_3 1668069965.1640372_.avi",
                          "/home/aji/Downloads/sequence_video/7/video_2 1668069965.1640372_.avi",
                          "/home/aji/Downloads/sequence_video/7/video_4 1668069965.1640372_.avi",
                          "/home/aji/Downloads/sequence_video/7/video_1 1668069965.1640372_.avi"]
        for i in range(self.view_controller.model.total_camera_used):
            # filepath_video = select_file(None, "Select video", "", "*.avi *.mp4")
            if filepath_video:
                self.view_controller.controller.video_controller.running_video(i, filepath_video[i])
                # self.view_controller.controller.video_controller.running_video(i, filepath_video)
                if len(filepath_video) == 4:
                    self.view_controller.model.properties_video["video"] = True
            else:
                break
        self.showing_to_ui()

    def showing_to_ui(self):
        self.view_controller.controller.video_controller.next_frame()
        self.view_controller.show_to_ui.showing_video_result()
        self.set_value_timer_video()

    def change_value_slider(self, value):
        value_max = self.view_controller.main_ui.slider_video.maximum()
        self.view_controller.controller.control_video.slider_controller(value, value_max)
        self.showing_to_ui()

    def set_value_timer_video(self):
        # total_minute, current_minute, total_second, current_second = self.view_controller.controller.video_controller.get_time_video()

        current_minute = self.view_controller.model.properties_video["current_minute"]
        current_second = self.view_controller.model.properties_video["current_second"]
        total_minute = self.view_controller.model.properties_video["total_minute"]
        total_second = self.view_controller.model.properties_video["total_second"]

        self.view_controller.main_ui.label_time_recent.setText("%02d : %02d" % (current_minute, current_second))
        self.view_controller.main_ui.label_time_end.setText("%02d : %02d" % (total_minute, total_second))

    def onclick_stop_video(self):
        self.__timer.stop()
        self.view_controller.controller.video_controller.stop_video()
        self.showing_to_ui()
        self.view_controller.main_ui.btn_play_pause.setChecked(False)
        # self.view_controller.set_icon.set_icon_video_play_pause("begin")

    def record_bird_view_video(self):
        if self.view_controller.main_ui.btn_Rec.isChecked():
            self.view_controller.controller.video_controller.initial_record()
            self.view_controller.controller.video_controller.record = True
            print("start record")
        else:
            self.view_controller.controller.video_controller.record = False
            print("helo from record")

    def show_full_video(self):
        if self.view_controller.main_ui.btn_Full_view.isChecked():
            self.view_controller.main_ui.frame_4.hide()
            self.view_controller.main_ui.frame_2.hide()
        else:
            self.view_controller.main_ui.frame_4.show()
            self.view_controller.main_ui.frame_2.show()

    def onclick_change_mode_overlap(self):
        if self.view_controller.main_ui.radioButton_horizontal_video.isChecked():
            mode = "H"
        elif self.view_controller.main_ui.radioButton_vertical_video.isChecked():
            mode = "V"
        elif self.view_controller.main_ui.radioButton_diagonal_video.isChecked():
            mode = "D"
        else:
            mode = "O"
        self.view_controller.controller.video_controller.change_mode_overlap(mode)
        self.view_controller.show_to_ui.showing_video_result()
