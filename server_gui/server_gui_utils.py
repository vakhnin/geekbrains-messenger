import os

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

cur_path = os.path.abspath(__file__)
cur_dir, _ = os.path.split(cur_path)
cur_dir += os.sep


class ServerGUIWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi(cur_dir + 'serverUI.ui', self)
