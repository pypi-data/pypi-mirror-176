import sys
from qtpy import QtWidgets

from .monctl import MyWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWindow()
    widget.show()

    sys.exit(app.exec_())