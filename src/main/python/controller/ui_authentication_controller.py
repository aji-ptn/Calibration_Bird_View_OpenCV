import sys

import yaml
from ..view.authentication import Ui_Authentication_password
# from .theme import *


class AuthenticationPassword(Ui_Authentication_password):
    def __init__(self, recent_win, controller):
        super(AuthenticationPassword, self).__init__()
        self.authen = None
        self.password = None
        self.recent_win = recent_win
        self.controller = controller
        self.setupUi(self.recent_win)
        # self.frame_authentification_password.setStyleSheet(open(self.controller.stylesheet).read())
        #
        # self.config_path_authentication = self.controller.app_ctxt.get_resource('data.yaml')
        # self.load_config(self.config_path_authentication)

        self.connect_button()

    def connect_button(self):
        self.buttonBox.accepted.connect(self.onclick_comboBox_oke)
        self.buttonBox.rejected.connect(self.onclick_comboBox_cancel)

    def onclick_comboBox_oke(self):
        """
        Open the camera following the parent function and close the dialog window.

        Returns:

        """
        self.password = self.lineEdit_password.text()
        self.recent_win.close()

    def onclick_comboBox_cancel(self):
        """
        close the window when you click the buttonBox cancel.

        Returns:

        """
        self.recent_win.close()
