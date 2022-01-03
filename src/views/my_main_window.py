from PySide2 import QtGui, QtWidgets

from app.toolkit import TOOLKIT_ITEMS, ToolkitItemModel

from ui.mainwindow import Ui_MainWindow


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.scene = QtWidgets.QGraphicsScene(self)

        self.init_list_view()
        self.init_graphics_view()
        self.connect_toolbar_actions_signals()
        self.connect_graphics_scene_signals()

        self.on_scene_selection_changed()

    def init_list_view(self):
        self.list_model = ToolkitItemModel(self.ui.listView)

        for item in TOOLKIT_ITEMS:
            icon = QtGui.QIcon(item["icon"])
            item = QtGui.QStandardItem(icon, item["text"])

            # Add the item to the model
            self.list_model.appendRow(item)

        # Apply the model to the list view
        self.ui.listView.setModel(self.list_model)

    def init_graphics_view(self):
        self.ui.graphicsView.setScene(self.scene)

    def connect_toolbar_actions_signals(self):
        self.ui.actionRotateRight.triggered.connect(
            self.on_trigger_rotate_right
        )

    def connect_graphics_scene_signals(self):
        self.scene.selectionChanged.connect(self.on_scene_selection_changed)

    def on_trigger_rotate_right(self):
        self.ui.graphicsView.rotate_selected_items_right()

    def on_scene_selection_changed(self):
        selected_items = self.scene.selectedItems()
        self.ui.actionRotateRight.setEnabled(len(selected_items) > 0)
