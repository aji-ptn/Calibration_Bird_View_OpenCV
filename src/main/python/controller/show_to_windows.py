import cv2
import numpy as np
from .additional_function import show_image_to_label


class ShowToUi:
    def __init__(self, view_controller):
        self.view_controller = view_controller
        self.width_undistorted_image = 720
        self.width_union_image = 520
        self.width_preview_image = 520
        self.width_bird_view_image = 520
        self.width_bird_view_video = 520
        self.connect()

    def connect(self):
        self.view_controller.additional_button.button_zoom_out_undistorted.clicked.connect(self.zoom_out_undistorted_image)
        self.view_controller.additional_button.button_zoom_in_undistorted.clicked.connect(self.zoom_in_undistorted_image)
        self.view_controller.additional_button.button_zoom_out_union.clicked.connect(self.zoom_out_union_image)
        self.view_controller.additional_button.button_zoom_in_union.clicked.connect(self.zoom_in_union_image)
        self.view_controller.additional_button.button_zoom_out_preview.clicked.connect(self.zoom_out_preview_image)
        self.view_controller.additional_button.button_zoom_in_preview.clicked.connect(self.zoom_in_preview_image)
        self.view_controller.additional_button.button_zoom_out_bird_view.clicked.connect(self.zoom_out_bird_view_image)
        self.view_controller.additional_button.button_zoom_in_bird_view.clicked.connect(self.zoom_in_bird_view_image)

    def show_union_original_image(self):
        self.view_controller.model.update_union_original_image()
        image = self.view_controller.model.data_model.union_original_image
        if image is not None:
            show_image_to_label(self.view_controller.main_ui.wind_all_original_image, image, self.width_union_image)

    def show_image_current_calib(self):
        index = self.view_controller.main_ui.toolBox.currentIndex()
        image_original = self.view_controller.model.data_model.list_original_image[index]
        image_undistorted = self.view_controller.model.data_model.list_original_undistorted_image[index]
        if image_original is not None:
            show_image_to_label(self.view_controller.main_ui.wind_show_original, image_original, 320)
        else:
            self.view_controller.main_ui.wind_show_original.setText("No Image")
        if image_undistorted is not None:
            show_image_to_label(self.view_controller.main_ui.wind_show_undistortion, image_undistorted, 320)
        else:
            self.view_controller.main_ui.wind_show_undistortion.setText("No Image")
        self.show_image_undistorted(index)
        self.show_image_perspective(index)

    def show_image_undistorted(self, index):
        image =self.view_controller.model.data_model.list_original_image[index]
        if image is not None:
            self.view_controller.model.process_undistorted_image(index)
            # image = self.view_controller.model.data_model.list_undistorted_image[index]
            image = self.view_controller.model.data_model.list_undistorted_drawing_image[index]
            if image is not None:
                show_image_to_label(self.view_controller.main_ui.wind_show_undistortion_point, image,
                                    self.width_undistorted_image)
        else:
            self.view_controller.main_ui.wind_show_undistortion_point.setText("No image")

    def show_image_perspective(self, index):
        image = self.view_controller.model.data_model.list_perspective_drawing_image[index]
        # image = self.view_controller.model.data_model.list_perspective_image[index]
        if image is not None:
            try:
                show_image_to_label(self.view_controller.main_ui.wind_preview, image, self.width_preview_image)
            except:
                print("no perspective created")

    def show_bird_view_image(self):
        image = self.view_controller.model.data_model.overlap_image
        if image is not None:
            show_image_to_label(self.view_controller.main_ui.wind_bird_view, image, self.width_bird_view_image)

    def zoom_out_undistorted_image(self):
        index = self.view_controller.main_ui.toolBox.currentIndex()
        self.width_undistorted_image -= 100
        self.show_image_undistorted(index)

    def zoom_in_undistorted_image(self):
        index = self.view_controller.main_ui.toolBox.currentIndex()
        self.width_undistorted_image += 100
        self.show_image_undistorted(index)

    def zoom_out_union_image(self):
        self.width_union_image -= 100
        self.show_union_original_image()

    def zoom_in_union_image(self):
        self.width_union_image += 100
        self.show_union_original_image()

    def zoom_out_preview_image(self):
        index = self.view_controller.main_ui.toolBox.currentIndex()
        self.width_preview_image -= 100
        self.show_image_perspective(index)

    def zoom_in_preview_image(self):
        index = self.view_controller.main_ui.toolBox.currentIndex()
        self.width_preview_image += 100
        self.show_image_perspective(index)
    
    def zoom_out_bird_view_image(self):
        self.width_bird_view_image -= 100
        self.show_bird_view_image()

    def zoom_in_bird_view_image(self):
        self.width_bird_view_image += 100
        self.show_bird_view_image()

    def zoom_out_bird_view_video(self):
        self.width_bird_view_video -= 100
        self.showing_video_result()

    def zoom_in_bird_view_video(self):
        self.width_bird_view_video += 100
        self.showing_video_result()

    def showing_video_result(self):
        image = self.view_controller.model.data_model.bird_view_video
        if image is not None:
            show_image_to_label(self.view_controller.main_ui.wind_bird_view_video, image, self.width_bird_view_video)
