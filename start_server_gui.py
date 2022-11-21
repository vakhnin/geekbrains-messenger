from PyQt5 import QtWidgets
import sys


from server_gui.server_gui_utils import ServerGUIindow


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ServerGUIindow()
    window.show()
    sys.exit(app.exec_())
