from PyQt6 import QtWidgets

from view.main_ui import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QApplication

from model.main_model import MainModel
from controller.main_controller import MainController
import sys


class App:
    def __init__(self, parent):

        self.model = MainModel()
        self.controller = MainController(parent, self.model, Ui_MainWindow())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = App(MainWindow)
    # ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
