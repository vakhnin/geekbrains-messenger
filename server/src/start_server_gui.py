from PyQt5 import QtWidgets
import sys

sys.path.append('.')
from server_gui.server_gui_utils import ServerGUIWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ServerGUIWindow()
    window.show()
    sys.exit(app.exec_())
