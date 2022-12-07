from PyQt5 import QtWidgets, QtCore


class AdditionalButton:
    def __init__(self, view_controller):
        self.view_controller = view_controller
        self.zoom_for_undistorted_image()
        self.zoom_for_union_original_image()
        self.zoom_for_preview_image()
        self.zoom_for_bird_view_image()

    def zoom_for_undistorted_image(self):
        self.button_zoom_out_undistorted = QtWidgets.QPushButton(self.view_controller.main_ui.scrollArea_2)
        self.button_zoom_out_undistorted.setGeometry(QtCore.QRect(40, 10, 25, 25))
        self.button_zoom_out_undistorted.setMinimumSize(QtCore.QSize(25, 25))
        self.button_zoom_out_undistorted.setMaximumSize(QtCore.QSize(25, 25))
        self.button_zoom_out_undistorted.setObjectName("button_zoom_out_undistorted")
        self.button_zoom_in_undistorted = QtWidgets.QPushButton(self.view_controller.main_ui.scrollArea_2)
        self.button_zoom_in_undistorted.setGeometry(QtCore.QRect(10, 10, 25, 25))
        self.button_zoom_in_undistorted.setMinimumSize(QtCore.QSize(25, 25))
        self.button_zoom_in_undistorted.setMaximumSize(QtCore.QSize(25, 25))
        self.button_zoom_in_undistorted.setObjectName("button_zoom_in_undistorted")
        _translate = QtCore.QCoreApplication.translate
        self.button_zoom_out_undistorted.setText(_translate("MainWindow", "-"))
        self.button_zoom_in_undistorted.setText(_translate("MainWindow", "+"))

    def zoom_for_union_original_image(self):
        self.button_zoom_out_union = QtWidgets.QPushButton(self.view_controller.main_ui.scrollArea_5)
        self.button_zoom_out_union.setGeometry(QtCore.QRect(40, 10, 25, 25))
        self.button_zoom_out_union.setMinimumSize(QtCore.QSize(25, 25))
        self.button_zoom_out_union.setMaximumSize(QtCore.QSize(25, 25))
        self.button_zoom_out_union.setObjectName("button_zoom_out_union")
        self.button_zoom_in_union = QtWidgets.QPushButton(self.view_controller.main_ui.scrollArea_5)
        self.button_zoom_in_union.setGeometry(QtCore.QRect(10, 10, 25, 25))
        self.button_zoom_in_union.setMinimumSize(QtCore.QSize(25, 25))
        self.button_zoom_in_union.setMaximumSize(QtCore.QSize(25, 25))
        self.button_zoom_in_union.setObjectName("button_zoom_in_union")
        _translate = QtCore.QCoreApplication.translate
        self.button_zoom_out_union.setText(_translate("MainWindow", "-"))
        self.button_zoom_in_union.setText(_translate("MainWindow", "+"))

    def zoom_for_preview_image(self):
        self.button_zoom_out_preview = QtWidgets.QPushButton(self.view_controller.main_ui.scrollArea_3)
        self.button_zoom_out_preview.setGeometry(QtCore.QRect(40, 10, 25, 25))
        self.button_zoom_out_preview.setMinimumSize(QtCore.QSize(25, 25))
        self.button_zoom_out_preview.setMaximumSize(QtCore.QSize(25, 25))
        self.button_zoom_out_preview.setObjectName("button_zoom_out_preview")
        self.button_zoom_in_preview = QtWidgets.QPushButton(self.view_controller.main_ui.scrollArea_3)
        self.button_zoom_in_preview.setGeometry(QtCore.QRect(10, 10, 25, 25))
        self.button_zoom_in_preview.setMinimumSize(QtCore.QSize(25, 25))
        self.button_zoom_in_preview.setMaximumSize(QtCore.QSize(25, 25))
        self.button_zoom_in_preview.setObjectName("button_zoom_in_preview")
        _translate = QtCore.QCoreApplication.translate
        self.button_zoom_out_preview.setText(_translate("MainWindow", "-"))
        self.button_zoom_in_preview.setText(_translate("MainWindow", "+"))

    def zoom_for_bird_view_image(self):
        self.button_zoom_out_bird_view = QtWidgets.QPushButton(self.view_controller.main_ui.scrollArea_4)
        self.button_zoom_out_bird_view.setGeometry(QtCore.QRect(40, 10, 25, 25))
        self.button_zoom_out_bird_view.setMinimumSize(QtCore.QSize(25, 25))
        self.button_zoom_out_bird_view.setMaximumSize(QtCore.QSize(25, 25))
        self.button_zoom_out_bird_view.setObjectName("button_zoom_out_bird_view")
        self.button_zoom_in_bird_view = QtWidgets.QPushButton(self.view_controller.main_ui.scrollArea_4)
        self.button_zoom_in_bird_view.setGeometry(QtCore.QRect(10, 10, 25, 25))
        self.button_zoom_in_bird_view.setMinimumSize(QtCore.QSize(25, 25))
        self.button_zoom_in_bird_view.setMaximumSize(QtCore.QSize(25, 25))
        self.button_zoom_in_bird_view.setObjectName("button_zoom_in_bird_view")
        _translate = QtCore.QCoreApplication.translate
        self.button_zoom_out_bird_view.setText(_translate("MainWindow", "-"))
        self.button_zoom_in_bird_view.setText(_translate("MainWindow", "+"))
