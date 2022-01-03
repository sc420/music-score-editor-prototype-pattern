from PySide2.QtCore import QMimeData
from PySide2.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide2 import QtCore, QtGui, QtWidgets

from ui.mainwindow import Ui_MainWindow

from app.toolkit import TOOLKIT_ITEMS


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


class ToolkitItemModel(QStandardItemModel):
    def mimeData(self, indexes):
        mime_data = QMimeData()
        urls = [TOOLKIT_ITEMS[index.row()]['mimeData'] for index in indexes]
        mime_data.setUrls(urls)
        return mime_data

class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.init_list_view()
        self.init_graphics_view()

    def init_list_view(self):
        self.list_model = ToolkitItemModel(self.ui.listView)

        for item in TOOLKIT_ITEMS:
            icon = QIcon(item['icon'])
            item = QStandardItem(icon, item['text'])

            # Add the item to the model
            self.list_model.appendRow(item)

        # Apply the model to the list view
        self.ui.listView.setModel(self.list_model)

    def init_graphics_view(self):
        self.scene = QtWidgets.QGraphicsScene(self)
        self.ui.graphicsView.setScene(self.scene)

        # self.scene.addItem(Line(25, 25, 25, 50))
        # self.scene.addItem(Line(30, 30, 30, 70))
        # self.scene.addItem(Line(35, 40, 35, 65))

        self.scene.setSceneRect(self.ui.graphicsView.frameGeometry())
