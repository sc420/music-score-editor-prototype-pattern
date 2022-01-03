from typing import List, Dict

from PySide2 import QtCore, QtGui, QtWidgets

from app.graphic import Staff, WholeNote, HalfNote
from app.toolkit import TOOLKIT_ITEMS
from framework.tool import GraphicTools


class MyGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        # Reference: https://gist.github.com/benjaminirving/f45de3bbabbcacd3ca29
        items = self.parse_mime_data(event.mimeData())
        if items:
            event.acceptProposedAction()

    def dragLeaveEvent(self, event: QtGui.QDragLeaveEvent):
        """
        Does nothing but can disable the Qt warning
        "QGraphicsView::dragLeaveEvent: drag leave received before drag enter".
        """
        pass

    def dragMoveEvent(self, event: QtGui.QDragMoveEvent):
        items = self.parse_mime_data(event.mimeData())
        if items:
            event.acceptProposedAction()

    def dropEvent(self, event: QtGui.QDropEvent):
        items = self.parse_mime_data(event.mimeData())
        if items:
            event.acceptProposedAction()

            pos = event.pos()
            scene_pos = self.mapToScene(pos.x(), pos.y())
            self.add_items(items, scene_pos)

    def resizeEvent(self, event: QtGui.QResizeEvent):
        super().resizeEvent(event)

        # Update the scene rectangle to match the view
        rect = self.contentsRect()
        self.scene().setSceneRect(rect)

    def add_items(self, items: List[Dict[str, str]], scene_pos: QtCore.QPoint):
        for item in items:
            if item['name'] == 'staff':
                obj = Staff()
            elif item['name'] == 'whole_note':
                obj = WholeNote()
            elif item['name'] == 'half_note':
                obj = HalfNote()
            else:
                raise ValueError(f'Unknown item name "{item["name"]}"')

            graphic_tool = GraphicTools(self.scene(), obj)
            graphic_tool.add_item(scene_pos)

    @staticmethod
    def parse_mime_data(mime_data: QtCore.QMimeData) -> List[Dict[str, str]]:
        if not mime_data.hasUrls():
            return []
        urls = mime_data.urls()
        items = filter(lambda item: item['mimeData'] in urls, TOOLKIT_ITEMS)
        return list(items)
