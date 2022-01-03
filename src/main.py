import sys

from PySide2 import QtWidgets

from views.my_main_window import MyMainWindow


def main():
    app = QtWidgets.QApplication([])
    widget = MyMainWindow()
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
