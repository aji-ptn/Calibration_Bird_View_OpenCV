class ConfigurationImage3:
    def __init__(self, controller):
        self.controller = controller
        self.controller.main_ui.doubleSpinBox_fy_2.setEnabled(False)
        self.connect_action()

    def connect_action(self):
        # ================== intrinsic parameter ==================
        self.controller.main_ui.doubleSpinBox_fx_2.valueChanged.connect(self.change_intrinsic_from_ui_fx_fy)
        self.controller.main_ui.doubleSpinBox_fy_2.valueChanged.connect(self.change_intrinsic_from_ui_fx_fy)
        self.controller.main_ui.doubleSpinBox_icx_2.valueChanged.connect(self.change_intrinsic_from_ui_icx_icy_w_h)
        self.controller.main_ui.doubleSpinBox_icy_2.valueChanged.connect(self.change_intrinsic_from_ui_icx_icy_w_h)
        self.controller.main_ui.spinBox_width_2.valueChanged.connect(self.change_intrinsic_from_ui_icx_icy_w_h)
        self.controller.main_ui.spinBox_height_2.valueChanged.connect(self.change_intrinsic_from_ui_icx_icy_w_h)

        # ================== src parameter ==================
        self.controller.main_ui.spinBox_src_point1_x_2.valueChanged.connect(self.change_properties_src_from_ui)
        self.controller.main_ui.spinBox_src_point1_y_2.valueChanged.connect(self.change_properties_src_from_ui)
        self.controller.main_ui.spinBox_src_point2_x_2.valueChanged.connect(self.change_properties_src_from_ui)
        self.controller.main_ui.spinBox_src_point2_y_2.valueChanged.connect(self.change_properties_src_from_ui)
        self.controller.main_ui.spinBox_src_point3_x_2.valueChanged.connect(self.change_properties_src_from_ui)
        self.controller.main_ui.spinBox_src_point3_y_2.valueChanged.connect(self.change_properties_src_from_ui)
        self.controller.main_ui.spinBox_src_point4_x_2.valueChanged.connect(self.change_properties_src_from_ui)
        self.controller.main_ui.spinBox_src_point4_y_2.valueChanged.connect(self.change_properties_src_from_ui)

        # ================== dst parameter ==================
        self.controller.main_ui.spinBox_dst_point1_x_2.valueChanged.connect(self.change_properties_dst_from_ui)
        self.controller.main_ui.spinBox_dst_point1_y_2.valueChanged.connect(self.change_properties_dst_from_ui)
        self.controller.main_ui.spinBox_dst_point2_x_2.valueChanged.connect(self.change_properties_dst_from_ui)
        self.controller.main_ui.spinBox_dst_point2_y_2.valueChanged.connect(self.change_properties_dst_from_ui)
        self.controller.main_ui.spinBox_dst_point3_x_2.valueChanged.connect(self.change_properties_dst_from_ui)
        self.controller.main_ui.spinBox_dst_point3_y_2.valueChanged.connect(self.change_properties_dst_from_ui)
        self.controller.main_ui.spinBox_dst_point4_x_2.valueChanged.connect(self.change_properties_dst_from_ui)
        self.controller.main_ui.spinBox_dst_point4_y_2.valueChanged.connect(self.change_properties_dst_from_ui)
        self.controller.main_ui.spinBox_width_dst_2.valueChanged.connect(self.change_properties_dst_from_ui)
        self.controller.main_ui.spinBox_height_dst_2.valueChanged.connect(self.change_properties_dst_from_ui)

    def update_properties_intrinsic(self):
        self.controller.model.data_model.properties_image["Image_3"] = {}
        self.controller.model.data_model.properties_image["Image_3"]["Ins"] = {}
        self.update_properties_src()
        self.update_properties_dst()
        self.change_properties_intrinsic()

    def update_properties_src(self):
        self.controller.model.data_model.properties_image["Image_3"]["src"] = {}
        self.change_properties_src()

    def update_properties_dst(self):
        self.controller.model.data_model.properties_image["Image_3"]["dst"] = {}
        self.change_properties_dst()

    def change_intrinsic_from_ui_fx_fy(self):
        if self.controller.model.data_model.list_original_image[2] is not None:
            if self.controller.model.data_model.properties_image["Image_3"]["Ins"]["Fx"] is not None:
                print("here")
                deviation = self.controller.main_ui.doubleSpinBox_fx_2.value() - \
                            self.controller.model.data_model.properties_image["Image_3"]["Ins"]["Fx"]
                self.controller.model.data_model.properties_image["Image_3"]["Ins"]["Fy"] = self.controller.model.data_model.properties_image["Image_3"]["Ins"]["Fy"] + deviation
                self.controller.model.data_model.properties_image["Image_3"]["Ins"]["Fx"] = self.controller.main_ui.doubleSpinBox_fx_2.value()
                self.set_intrinsic_parameter_to_ui()
            self.change_properties_intrinsic()
            index = self.controller.main_ui.toolBox.currentIndex()
            self.controller.model.process_perspective_image(index)
            self.controller.show_to_ui.show_image_current_calib()
            self.controller.change_overlap_or_bird_view()

    def change_intrinsic_from_ui_icx_icy_w_h(self):
        if self.controller.model.data_model.list_original_image[2] is not None:
            self.change_properties_intrinsic()
            index = self.controller.main_ui.toolBox.currentIndex()
            self.controller.model.process_perspective_image(index)
            self.controller.show_to_ui.show_image_current_calib()
            self.controller.change_overlap_or_bird_view()

    def change_properties_src_from_ui(self):
        if self.controller.model.data_model.list_original_image[2] is not None:
            self.change_properties_src()
            index = self.controller.main_ui.toolBox.currentIndex()
            self.controller.model.process_perspective_image(index)
            self.controller.show_to_ui.show_image_current_calib()
            self.controller.change_overlap_or_bird_view()

    def change_properties_dst_from_ui(self):
        if self.controller.model.data_model.list_original_image[2] is not None:
            self.change_properties_dst()
            index = self.controller.main_ui.toolBox.currentIndex()
            self.controller.model.process_perspective_image(index)
            self.controller.show_to_ui.show_image_current_calib()
            self.controller.change_overlap_or_bird_view()

    def load_config_from_file(self):
        self.set_intrinsic_parameter_to_ui()
        self.set_properties_src_to_ui()
        self.set_properties_dst_to_ui()

    def change_properties_intrinsic(self):
        self.controller.model.data_model.properties_image["Image_3"]["Ins"]["Fx"] = self.controller.main_ui.doubleSpinBox_fx_2.value()
        self.controller.model.data_model.properties_image["Image_3"]["Ins"]["Fy"] = self.controller.main_ui.doubleSpinBox_fy_2.value()
        self.controller.model.data_model.properties_image["Image_3"]["Ins"]["Icx"] = self.controller.main_ui.doubleSpinBox_icx_2.value()
        self.controller.model.data_model.properties_image["Image_3"]["Ins"]["Icy"] = self.controller.main_ui.doubleSpinBox_icy_2.value()
        self.controller.model.data_model.properties_image["Image_3"]["Ins"]["Width"] = self.controller.main_ui.spinBox_width_2.value()
        self.controller.model.data_model.properties_image["Image_3"]["Ins"]["Height"] = self.controller.main_ui.spinBox_height_2.value()

    def change_properties_src(self):
        self.controller.model.data_model.properties_image["Image_3"]["src"]["point1_x"] = self.controller.main_ui.spinBox_src_point1_x_2.value()
        self.controller.model.data_model.properties_image["Image_3"]["src"]["point1_y"] = self.controller.main_ui.spinBox_src_point1_y_2.value()
        self.controller.model.data_model.properties_image["Image_3"]["src"]["point2_x"] = self.controller.main_ui.spinBox_src_point2_x_2.value()
        self.controller.model.data_model.properties_image["Image_3"]["src"]["point2_y"] = self.controller.main_ui.spinBox_src_point2_y_2.value()
        self.controller.model.data_model.properties_image["Image_3"]["src"]["point3_x"] = self.controller.main_ui.spinBox_src_point3_x_2.value()
        self.controller.model.data_model.properties_image["Image_3"]["src"]["point3_y"] = self.controller.main_ui.spinBox_src_point3_y_2.value()
        self.controller.model.data_model.properties_image["Image_3"]["src"]["point4_x"] = self.controller.main_ui.spinBox_src_point4_x_2.value()
        self.controller.model.data_model.properties_image["Image_3"]["src"]["point4_y"] = self.controller.main_ui.spinBox_src_point4_y_2.value()

    def change_properties_dst(self):
        self.controller.model.data_model.properties_image["Image_3"]["dst"]["point1_x"] = self.controller.main_ui.spinBox_dst_point1_x_2.value()
        self.controller.model.data_model.properties_image["Image_3"]["dst"]["point1_y"] = self.controller.main_ui.spinBox_dst_point1_y_2.value()
        self.controller.model.data_model.properties_image["Image_3"]["dst"]["point2_x"] = self.controller.main_ui.spinBox_dst_point2_x_2.value()
        self.controller.model.data_model.properties_image["Image_3"]["dst"]["point2_y"] = self.controller.main_ui.spinBox_dst_point2_y_2.value()
        self.controller.model.data_model.properties_image["Image_3"]["dst"]["point3_x"] = self.controller.main_ui.spinBox_dst_point3_x_2.value()
        self.controller.model.data_model.properties_image["Image_3"]["dst"]["point3_y"] = self.controller.main_ui.spinBox_dst_point3_y_2.value()
        self.controller.model.data_model.properties_image["Image_3"]["dst"]["point4_x"] = self.controller.main_ui.spinBox_dst_point4_x_2.value()
        self.controller.model.data_model.properties_image["Image_3"]["dst"]["point4_y"] = self.controller.main_ui.spinBox_dst_point4_y_2.value()
        self.controller.model.data_model.properties_image["Image_3"]["dst"]["Width"] = self.controller.main_ui.spinBox_width_dst_2.value()
        self.controller.model.data_model.properties_image["Image_3"]["dst"]["Height"] = self.controller.main_ui.spinBox_height_dst_2.value()

    def set_intrinsic_parameter_to_ui(self):
        self.block_signal_intrinsic_param()
        self.controller.main_ui.doubleSpinBox_fx_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["Ins"]["Fx"])
        self.controller.main_ui.doubleSpinBox_fy_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["Ins"]["Fy"])
        self.controller.main_ui.doubleSpinBox_icx_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["Ins"]["Icx"])
        self.controller.main_ui.doubleSpinBox_icy_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["Ins"]["Icy"])
        self.controller.main_ui.spinBox_width_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["Ins"]["Width"])
        self.controller.main_ui.spinBox_height_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["Ins"]["Height"])
        self.unblock_signal_intrinsic_param()

    def set_properties_src_to_ui(self):
        self.block_signal_src()
        self.controller.main_ui.spinBox_src_point1_x_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["src"]["point1_x"])
        self.controller.main_ui.spinBox_src_point1_y_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["src"]["point1_y"])
        self.controller.main_ui.spinBox_src_point2_x_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["src"]["point2_x"])
        self.controller.main_ui.spinBox_src_point2_y_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["src"]["point2_y"])
        self.controller.main_ui.spinBox_src_point3_x_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["src"]["point3_x"])
        self.controller.main_ui.spinBox_src_point3_y_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["src"]["point3_y"])
        self.controller.main_ui.spinBox_src_point4_x_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["src"]["point4_x"])
        self.controller.main_ui.spinBox_src_point4_y_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["src"]["point4_y"])
        self.unblock_signal_src()

    def set_properties_dst_to_ui(self):
        self.block_signal_dst()
        self.controller.main_ui.spinBox_dst_point1_x_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["dst"]["point1_x"])
        self.controller.main_ui.spinBox_dst_point1_y_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["dst"]["point1_y"])
        self.controller.main_ui.spinBox_dst_point2_x_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["dst"]["point2_x"])
        self.controller.main_ui.spinBox_dst_point2_y_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["dst"]["point2_y"])
        self.controller.main_ui.spinBox_dst_point3_x_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["dst"]["point3_x"])
        self.controller.main_ui.spinBox_dst_point3_y_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["dst"]["point3_y"])
        self.controller.main_ui.spinBox_dst_point4_x_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["dst"]["point4_x"])
        self.controller.main_ui.spinBox_dst_point4_y_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["dst"]["point4_y"])
        self.controller.main_ui.spinBox_width_dst_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["dst"]["Width"])
        self.controller.main_ui.spinBox_height_dst_2.setValue(self.controller.model.data_model.properties_image["Image_3"]["dst"]["Height"])
        self.unblock_signal_dst()

    def block_signal_intrinsic_param(self):
        self.controller.main_ui.doubleSpinBox_fx_2.blockSignals(True)
        self.controller.main_ui.doubleSpinBox_fy_2.blockSignals(True)
        self.controller.main_ui.doubleSpinBox_icx_2.blockSignals(True)
        self.controller.main_ui.doubleSpinBox_icy_2.blockSignals(True)
        self.controller.main_ui.spinBox_width_2.blockSignals(True)
        self.controller.main_ui.spinBox_height_2.blockSignals(True)

    def unblock_signal_intrinsic_param(self):
        self.controller.main_ui.doubleSpinBox_fx_2.blockSignals(False)
        self.controller.main_ui.doubleSpinBox_fy_2.blockSignals(False)
        self.controller.main_ui.doubleSpinBox_icx_2.blockSignals(False)
        self.controller.main_ui.doubleSpinBox_icy_2.blockSignals(False)
        self.controller.main_ui.spinBox_width_2.blockSignals(False)
        self.controller.main_ui.spinBox_height_2.blockSignals(False)

    def block_signal_src(self):
        self.controller.main_ui.spinBox_src_point1_x_2.blockSignals(True)
        self.controller.main_ui.spinBox_src_point1_y_2.blockSignals(True)
        self.controller.main_ui.spinBox_src_point2_x_2.blockSignals(True)
        self.controller.main_ui.spinBox_src_point2_y_2.blockSignals(True)
        self.controller.main_ui.spinBox_src_point3_x_2.blockSignals(True)
        self.controller.main_ui.spinBox_src_point3_y_2.blockSignals(True)
        self.controller.main_ui.spinBox_src_point4_x_2.blockSignals(True)
        self.controller.main_ui.spinBox_src_point4_y_2.blockSignals(True)

    def unblock_signal_src(self):
        self.controller.main_ui.spinBox_src_point1_x_2.blockSignals(False)
        self.controller.main_ui.spinBox_src_point1_y_2.blockSignals(False)
        self.controller.main_ui.spinBox_src_point2_x_2.blockSignals(False)
        self.controller.main_ui.spinBox_src_point2_y_2.blockSignals(False)
        self.controller.main_ui.spinBox_src_point3_x_2.blockSignals(False)
        self.controller.main_ui.spinBox_src_point3_y_2.blockSignals(False)
        self.controller.main_ui.spinBox_src_point4_x_2.blockSignals(False)
        self.controller.main_ui.spinBox_src_point4_y_2.blockSignals(False)

    def block_signal_dst(self):
        self.controller.main_ui.spinBox_dst_point1_x_2.blockSignals(True)
        self.controller.main_ui.spinBox_dst_point1_y_2.blockSignals(True)
        self.controller.main_ui.spinBox_dst_point2_x_2.blockSignals(True)
        self.controller.main_ui.spinBox_dst_point2_y_2.blockSignals(True)
        self.controller.main_ui.spinBox_dst_point3_x_2.blockSignals(True)
        self.controller.main_ui.spinBox_dst_point3_y_2.blockSignals(True)
        self.controller.main_ui.spinBox_dst_point4_x_2.blockSignals(True)
        self.controller.main_ui.spinBox_dst_point4_y_2.blockSignals(True)
        self.controller.main_ui.spinBox_width_dst_2.blockSignals(True)
        self.controller.main_ui.spinBox_height_dst_2.blockSignals(True)

    def unblock_signal_dst(self):
        self.controller.main_ui.spinBox_dst_point1_x_2.blockSignals(False)
        self.controller.main_ui.spinBox_dst_point1_y_2.blockSignals(False)
        self.controller.main_ui.spinBox_dst_point2_x_2.blockSignals(False)
        self.controller.main_ui.spinBox_dst_point2_y_2.blockSignals(False)
        self.controller.main_ui.spinBox_dst_point3_x_2.blockSignals(False)
        self.controller.main_ui.spinBox_dst_point3_y_2.blockSignals(False)
        self.controller.main_ui.spinBox_dst_point4_x_2.blockSignals(False)
        self.controller.main_ui.spinBox_dst_point4_y_2.blockSignals(False)
        self.controller.main_ui.spinBox_width_dst_2.blockSignals(False)
        self.controller.main_ui.spinBox_height_dst_2.blockSignals(False)
