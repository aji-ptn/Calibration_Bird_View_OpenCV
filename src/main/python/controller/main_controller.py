import os
from pwd import getpwuid
from os import stat

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QLabel
from PyQt6.QtCore import Qt
from .additional_function import select_file, init_ori_ratio, show_image_to_label
# from .ui_authentication_controller import AuthenticationPassword
from .calib_properties import CalibProperties
from .show_to_windows import ShowToUi
from .additional_ui import AdditionalButton
from .ui_video_controller import UiVideoController
from .get_sources import GetResourcesFile


class MainController(QMainWindow):
    def __init__(self, parent, model, ui):
        """

        Class of main controller

        Args:
            parent: QMainWindow
            model: class model
            ui: user interface
        """
        super(MainController, self).__init__()
        self.main_ui = ui
        self.main_ui.setupUi(parent)

        self.model = model
        self.additional_button = AdditionalButton(self)
        self.calib_properties = CalibProperties(self)
        self.show_to_ui = ShowToUi(self)
        self.main_ui.wind_show_undistortion_point.setMouseTracking(True)
        self.ui_video_controller = UiVideoController(self)
        self.list_btn_point = [self.main_ui.button_select_point_0, self.main_ui.button_select_point_1,
                               self.main_ui.button_select_point_2, self.main_ui.button_select_point_3]
        self.list_add_value_src_to_ui = [self.calib_properties.config_image_1,
                                         self.calib_properties.config_image_2,
                                         self.calib_properties.config_image_3,
                                         self.calib_properties.config_image_4]
        self.data_point_click = []
        self.model.data_model.gradient_image = "O"
        self.model.data_model.data_config = False
        self.model.data_model.list_original_image = []
        self.model.data_model.overlap_image = []
        self.hide()
        self.add_label_zoom()
        self.source_file = GetResourcesFile()
        self.model.set_source_file(self.source_file)
        self.connect()

    def connect(self):
        """
        This function is for connect even for action from user interface
        """
        self.main_ui.button_open_image.clicked.connect(self.open_image)
        self.main_ui.toolBox.currentChanged.connect(self.activate_toolbox)
        # self.main_ui.checkBox_show_overlapping.clicked.connect(self.change_overlap_or_bird_view)
        self.main_ui.wind_show_undistortion_point.mouseMoveEvent = self.mouse_event_move
        # self.main_ui.wind_show_undistortion_point.mousePressEvent = self.mouse_event_click
        self.main_ui.wind_show_undistortion_point.mousePressEvent = self.get_position_in_image

        self.main_ui.button_select_point_0.clicked.connect(lambda: self.onclick_select_point(0))
        self.main_ui.button_select_point_1.clicked.connect(lambda: self.onclick_select_point(1))
        self.main_ui.button_select_point_2.clicked.connect(lambda: self.onclick_select_point(2))
        self.main_ui.button_select_point_3.clicked.connect(lambda: self.onclick_select_point(3))

        self.main_ui.radioButton_horizontal_image.clicked.connect(self.onclick_mode_gradient_image)
        self.main_ui.radioButton_vertical_image.clicked.connect(self.onclick_mode_gradient_image)
        self.main_ui.radioButton_diagonal_image.clicked.connect(self.onclick_mode_gradient_image)
        self.main_ui.radioButton_overlap_image.clicked.connect(self.onclick_mode_gradient_image)

        self.main_ui.button_clear_0.clicked.connect(self.onclick_clear_point)
        self.main_ui.button_clear_1.clicked.connect(self.onclick_clear_point)
        self.main_ui.button_clear_2.clicked.connect(self.onclick_clear_point)
        self.main_ui.button_clear_3.clicked.connect(self.onclick_clear_point)

        self.main_ui.button_save_image.clicked.connect(self.onclick_save_image)

    def open_image(self):  # function that program use
        """
        This function is for open image and parameter to the program
        """
        if self.model.data_model.data_config:
            self.main_ui.toolBox.setCurrentIndex(0)
            self.model.data_model.total_camera_used = 4
            # self.check_authentication()
            self.model.initial_properties()
            self.calib_properties.update_config()
            QMessageBox.information(None, "Information", "Select Source and parameter Image\nImage front -> left -> right "
                                                         "-> rear")
            for i in range(self.model.data_model.total_camera_used):
                path_image = select_file(None, "Select image !", "../../../", "Image file (*.jpeg *.jpg *.png)")

                if path_image:
                    path_parameter = select_file(None, "Select Parameter !", "../../../", "Parameter Files (*.yaml)")

                    if path_parameter:
                        self.model.list_intrinsic_data(path_parameter)
                        self.model.list_image_data(path_image, i)
                        if self.model.data_model.data_config is None:
                            self.model.update_intrinsic_parameter(i)
                        self.model.process_undistorted_image(i)
                        self.model.process_perspective_image(i)
                        self.show_to_ui.show_union_original_image()
                        self.show_to_ui.show_image_current_calib()
                else:
                    pass

            if len(self.model.data_model.list_original_image) == self.model.data_model.total_camera_used:
                self.model.data_model.overlap_image = self.model.process_bird_view("image")
                self.show_to_ui.show_bird_view_image()
            else:
                print("Not enough image resources")

            self.calib_properties.set_intrinsic_parameter_to_ui()
            print(self.model.data_model.properties_image)
        else:
            QMessageBox.information(None, "Information", "Please Select Configuration First")

    def activate_toolbox(self):
        """
        Select activate image calibration
        Returns:

        """
        if self.model.data_model.list_original_image:
            self.show_to_ui.show_image_current_calib()

    def change_overlap_or_bird_view(self):
        """
        Change overlap view or bird view image
        """
        self.model.update_overlap_or_bird_view()
        self.show_to_ui.show_bird_view_image()
        if self.model.data_model.properties_video["video"]:
            self.show_to_ui.showing_video_result()

    def add_label_zoom(self):
        """
        add label zoom in user interface
        """
        self.add_label = QLabel(self.main_ui.wind_show_undistortion_point)
        self.add_label.setGeometry(QtCore.QRect(5, 5, 100, 100))
        self.add_label.setFrameShape(QLabel.Shape.Box)
        self.add_label.setFrameShadow(QLabel.Shadow.Raised)
        self.add_label.hide()

    def mouse_event_move(self, e):
        """
        Mouse move event in undistortion image

        Args:
            e: True click event

        Returns:

        """
        index = self.main_ui.toolBox.currentIndex()
        if self.model.data_model.list_original_image:
            try:
                pos_x = round(e.x())
                pos_y = round(e.y())
                image_undistorted = self.model.data_model.list_undistorted_drawing_image[index]
            except:
                image_undistorted = None
            if image_undistorted is not None:
                ratio_x, ratio_y = init_ori_ratio(self.main_ui.wind_show_undistortion_point, image_undistorted)
                X = round(pos_x * ratio_x)
                Y = round(pos_y * ratio_y)
                try:
                    if X > 70 and Y > 70:
                        self.add_label.show()
                        self.add_label.setGeometry(QtCore.QRect(pos_x + 15, pos_y - 15, 100, 100))
                        if self.main_ui.wind_show_undistortion_point.height() - pos_y < 200:
                            self.add_label.setGeometry(QtCore.QRect(pos_x + 15, pos_y - 150, 100, 100))

                        if self.main_ui.wind_show_undistortion_point.width() - pos_x < 200:
                            self.add_label.setGeometry(QtCore.QRect(pos_x - 150, pos_y + 15, 100, 100))

                        if self.main_ui.wind_show_undistortion_point.height() - pos_y < 200 and self.main_ui. \
                                wind_show_undistortion_point.width() - pos_x < 200:
                            self.add_label.setGeometry(QtCore.QRect(pos_x - 150, pos_y - 150, 100, 100))

                        if self.main_ui.wind_show_undistortion_point.height() - pos_y < 20 and self.main_ui. \
                                wind_show_undistortion_point.width() - pos_x < 20:
                            self.add_label.hide()

                        img = self.model.crop_image(image_undistorted, X, Y)
                        # image_ = cv2.circle(self.image.copy(), (X, Y), 2, (200, 5, 200), -1)
                        # image = image_undistorted.copy()[Y - 70: (Y - 70) + 140, X - 70:(X - 70) + 140]
                        # self.show_to_ui.show_image_point_selection(self.add_label, image, 140)
                        show_image_to_label(self.add_label, img, 140)

                    else:
                        self.add_label.hide()
                except:
                    pass

    def get_position_in_image(self, e):
        """
        left click in mouse button

        Args:
            e: True click mouse

        Returns:

        """
        index = self.main_ui.toolBox.currentIndex()
        try:
            ratio_x, ratio_y = init_ori_ratio(self.main_ui.wind_show_undistortion_point,
                                              self.model.data_model.list_undistorted_drawing_image[index])
            if e.button() == Qt.MouseButton.LeftButton:
                pos_x = round(e.x() * ratio_x)
                pos_y = round(e.y() * ratio_y)
                if self.list_btn_point[index].isChecked():
                    coordinate = [pos_x, pos_y]
                    self.data_point_click.append(coordinate)
                    if len(self.data_point_click) == 4:
                        self.disable_button_select_point()
                        self.model.get_data_position(index, self.data_point_click)
                        self.list_add_value_src_to_ui[index].set_properties_src_to_ui()
        except:
            print("image not available")

    def disable_button_select_point(self):
        """
        disable button select point
        Returns:

        """
        self.main_ui.button_select_point_0.setChecked(False)
        self.main_ui.button_select_point_1.setChecked(False)
        self.main_ui.button_select_point_2.setChecked(False)
        self.main_ui.button_select_point_3.setChecked(False)

    def onclick_select_point(self, i):
        """
        This function if input from button select point
        Args:
            i: True select point

        Returns:

        """
        self.list_btn_point[i].setChecked(True)
        self.data_point_click = []

    def onclick_clear_point(self):
        """
        This function is for clear point selected
        Returns:

        """
        index = self.main_ui.toolBox.currentIndex()
        self.data_point_click = []
        for ih in range(4):
            self.data_point_click.append([0, 0])
        self.model.get_data_position(index, self.data_point_click)
        self.list_add_value_src_to_ui[index].set_properties_src_to_ui()

    def onclick_mode_gradient_image(self):
        """
        This function is for change mode of gradient
        Returns:

        """
        if self.model.data_model.list_original_image:
            if self.main_ui.radioButton_horizontal_image.isChecked():
                mode = "H"
            elif self.main_ui.radioButton_vertical_image.isChecked():
                mode = "V"
            elif self.main_ui.radioButton_diagonal_image.isChecked():
                mode = "D"
            else:
                mode = "O"
            print(mode)
            self.model.change_mode_gradient_image(mode)
            self.show_to_ui.show_bird_view_image()

    def hide(self):
        """
        hide user interface button and action
        Returns:

        """
        self.main_ui.radioButton_diagonal_image.hide()
        self.main_ui.toolBox.setItemEnabled(4, False)
        self.main_ui.toolBox.setItemEnabled(5, False)
        # self.main_ui.checkBox_show_overlapping.hide()
        self.main_ui.tabWidget_bird_view_video.setTabVisible(3, False)
        self.main_ui.label_38.hide()
        self.main_ui.spinBox_shift_x_1.hide()
        self.main_ui.label_40.hide()
        self.main_ui.spinBox_shift_y_1.hide()
        self.main_ui.label_41.hide()
        self.main_ui.spinBox_shift_x_2.hide()
        self.main_ui.label_42.hide()
        self.main_ui.spinBox_shift_y_2.hide()
        self.main_ui.label_219.hide()
        self.main_ui.spinBox_shift_x_3.hide()
        self.main_ui.label_220.hide()
        self.main_ui.spinBox_shift_y_3.hide()
        self.main_ui.label_223.hide()
        self.main_ui.spinBox_shift_x_5.hide()
        self.main_ui.label_224.hide()
        self.main_ui.spinBox_shift_y_5.hide()
        self.main_ui.radioButton_vertical_image.hide()

    def onclick_save_image(self):
        """
        Click save image bird view
        Returns:

        """
        if self.model.data_model.overlap_image is not None:
            self.model.save_image()

    def change_permission_root_file(self):
        """
        Get permission to access sudo root opt
        Returns:

        """
        target = "/opt/Calib Bird View/"
        user = getpwuid(os.stat(target).st_uid).pw_name
        if user == "root":
            passwd = self.get_password()
            if passwd is None:
                QtWidgets.QMessageBox.information(None,
                                                  "Warning!!", "you not write the password!!")
                return False
            else:
                os.system("echo " + passwd + "| sudo -S chown $USER /opt/Calib Bird View/")
                user = getpwuid(os.stat(target).st_uid).pw_name
                if user == "root":
                    QtWidgets.QMessageBox.information(None,
                                                      "Warning!!", "Your Password Is Wrong!!")
                    return False

                else:
                    for filename in os.listdir(target):
                        os.system("echo " + passwd + "| sudo -S chown $USER /opt/Calib Bird View/" + filename)
                    os.system("echo " + passwd + "| sudo -S chown $USER "
                                                 "/opt/Calib Bird View/")
                    return True

        else:
            return True

    @classmethod
    def get_password(cls):
        passwd, ok = QtWidgets.QInputDialog.getText(None, "First Authentication", "Write your Password?",
                                                    QtWidgets.QLineEdit.Password)
        if ok and passwd != '':
            return passwd

        else:
            return None

   # def open_image(self):  # for fast input only. the use one in bellow function
    #     self.model.data_model.total_camera_used = 4
    #     self.check_authentication()
    #     self.model.initial_properties()
    #     self.calib_properties.update_config()
    #     QMessageBox.information(None, "Information", "Select Source and parameter Image\nImage front -> left -> right "
    #                                                  "-> rear")
    #
    #     # data taken in 111912022
    #     # path_image = ["/home/aji/Documents/MyGithub/OpenCV_bird_view_main/11192022/123/image3.jpg",
    #     #               "/home/aji/Documents/MyGithub/OpenCV_bird_view_main/11192022/123/image2.jpg",
    #     #               "/home/aji/Documents/MyGithub/OpenCV_bird_view_main/11192022/123/image4.jpg",
    #     #               "/home/aji/Documents/MyGithub/OpenCV_bird_view_main/11192022/123/image1.jpg"]
    #     #
    #     # path_parameter = ["/home/aji/Documents/MyGithub/OpenCV_bird_view_main/for_sequence/front_entaniya_12_.yaml",
    #     #               "/home/aji/Documents/MyGithub/OpenCV_bird_view_main/for_sequence/left_entaniya_4_.yaml",
    #     #               "/home/aji/Documents/MyGithub/OpenCV_bird_view_main/calibration/entaniya_11.yaml",
    #     #               "/home/aji/Documents/MyGithub/OpenCV_bird_view_main/calibration/entaniya_13_new_11192022.yaml"]
    #     #
    #     path_image = ["/home/aji/Documents/MyGithub/OpenCV_bird_view_main/1/front_true_.jpg",
    #                   "/home/aji/Documents/MyGithub/OpenCV_bird_view_main/1/left_true_.jpg",
    #                   "/home/aji/Documents/MyGithub/OpenCV_bird_view_main/1/right_true_.jpg",
    #                   "/home/aji/Documents/MyGithub/OpenCV_bird_view_main/1/back_true_.jpg"]
    #     path_parameter = ["/home/aji/Documents/MyGithub/OpenCV_bird_view_main/1/front.yaml",
    #                       "/home/aji/Documents/MyGithub/OpenCV_bird_view_main/1/left.yaml",
    #                       "/home/aji/Documents/MyGithub/OpenCV_bird_view_main/1/right.yaml",
    #                       "/home/aji/Documents/MyGithub/OpenCV_bird_view_main/1/rear.yaml"]
    #
    #     for i in range(self.model.data_model.total_camera_used):
    #         # path_image = select_file(None, "Select image !", "../", "Image file (*.jpeg *.jpg *.png)")
    #         #
    #         # if path_image:
    #         #     path_parameter = select_file(None, "Select Parameter !", "../", "Parameter Files (*.yaml)")
    #
    #         if path_parameter:
    #             self.model.list_intrinsic_data(path_parameter[i])
    #             self.model.list_image_data(path_image[i], i)
    #             if self.model.data_model.data_config is None:
    #                 self.model.update_intrinsic_parameter(i)
    #             self.model.process_undistorted_image(i)
    #             self.model.process_perspective_image(i)
    #             self.show_to_ui.show_union_original_image()
    #             self.show_to_ui.show_image_current_calib()
    #     # try:
    #     self.onclick_mode_gradient_image()
    #     # self.model.data_model.overlap_image = self.model.process_bird_view("image")
    #     # self.show_to_ui.show_bird_view_image()
    #     # except:
    #     #     pass
    #     self.calib_properties.set_intrinsic_parameter_to_ui()
    #     print("=------------------------------------")
    #     print(self.model.data_model.properties_image)
    #     print("=------------------------------------")