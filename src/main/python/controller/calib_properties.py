from .configuration_image_1 import ConfigurationImage1
from .configuration_image_2 import ConfigurationImage2
from .configuration_image_3 import ConfigurationImage3
from .configuration_image_4 import ConfigurationImage4
from .additional_function import select_file


class CalibProperties:
    def __init__(self, view_controller):
        self.view_controller = view_controller
        self.list_properties = []
        self.config_path = None

        self.config_image_1 = ConfigurationImage1(self.view_controller)
        self.config_image_2 = ConfigurationImage2(self.view_controller)
        self.config_image_3 = ConfigurationImage3(self.view_controller)
        self.config_image_4 = ConfigurationImage4(self.view_controller)

        self.view_controller.main_ui.button_save_config.clicked.connect(self.save_data_configuration)
        self.view_controller.main_ui.button_load_config.clicked.connect(self.load_configuration)

    def save_data_configuration(self):
        if self.config_path is not None:
            self.view_controller.model.save_config_to_file(self.config_path)

    def load_configuration(self):
        print("hereeee")
        self.config_path = select_file(self.view_controller, "Select config !!", "../data_config",
                                       "config file (*.yaml)")
        if self.config_path:
            try:
                self.view_controller.model.load_config(self.config_path)
                print(self.view_controller.model.data_model.properties_image)
                self.config_image_1.load_config_from_file()
                self.config_image_2.load_config_from_file()
                self.config_image_3.load_config_from_file()
                self.config_image_4.load_config_from_file()
            except:
                print("data not found")

    def set_intrinsic_parameter_to_ui(self):
        self.config_image_1.set_intrinsic_parameter_to_ui()
        self.config_image_2.set_intrinsic_parameter_to_ui()
        self.config_image_3.set_intrinsic_parameter_to_ui()
        self.config_image_4.set_intrinsic_parameter_to_ui()

    def update_config(self):
        self.config_image_1.update_properties_intrinsic()
        self.config_image_2.update_properties_intrinsic()
        self.config_image_3.update_properties_intrinsic()
        self.config_image_4.update_properties_intrinsic()
