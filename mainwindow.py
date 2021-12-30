import sys

from PySide2.QtCore import QSize
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide2 import QtCore, QtGui, QtWidgets

from ui.mainwindow import Ui_MainWindow

# Reference: https://stackoverflow.com/questions/46999042/select-items-in-qgraphicsscene-using-pyside
class Line(QtWidgets.QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2, parent=None):
        super().__init__(x1, y1, x2, y2, parent)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setPen(QtGui.QPen(QtCore.Qt.black, 3))

    def mousePressEvent(self, e):
        self.setPen(QtGui.QPen(QtCore.Qt.red, 5))
        QtWidgets.QGraphicsLineItem.mousePressEvent(self, e)

    def mouseReleaseEvent(self, e):
        self.setPen(QtGui.QPen(QtCore.Qt.black, 3))
        QtWidgets.QGraphicsLineItem.mouseReleaseEvent(self, e)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.init_list_view()
        self.init_graphics_view()

    def init_list_view(self):
        self.list_model = QStandardItemModel(self.ui.listView)

        items = [
            {
                "icon": u":/toolkit/icons/staff.png",
                "text": "Staff"
            },
            {
                "icon": u":/graphics_view/icons/half_note.svg",
                "text": "Half Note"
            },
            {
                "icon": u":/graphics_view/icons/whole_note.svg",
                "text": "Whole Note"
            }
        ]

        for item in items:
            icon = QIcon(item["icon"])
            item = QStandardItem(icon, item["text"])

            # Add the item to the model
            self.list_model.appendRow(item)

        # Apply the model to the list view
        self.ui.listView.setModel(self.list_model)

    def init_graphics_view(self):
        self.scene = QtWidgets.QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)

        self.ui.graphicsView.scene().addItem(Line(25, 25, 25, 50))
        self.ui.graphicsView.scene().addItem(Line(30, 30, 30, 70))
        self.ui.graphicsView.scene().addItem(Line(35, 40, 35, 65))


if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
