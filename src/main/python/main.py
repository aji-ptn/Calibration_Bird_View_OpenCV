from view.main_ui import Ui_MainWindow
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from model.model_data import MainData
from model.main_model import MainController
from controller.main_controller import MainView
import sys


class App:
    def __init__(self, parent, appctxt):
        self.model = MainData
        self.controller = MainController(appctxt, self.model)
        self.view = MainView(parent, appctxt, self.model, self.controller, Ui_MainWindow())


# if __name__ == "__main__":
#     app = App(sys.argv)
#     sys.exit(app.exec_())

if __name__ == '__main__':
    appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
    window = QMainWindow()
    ui = App(window, appctxt)
    window.show()
    exit_code = appctxt.app.exec_()  # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
