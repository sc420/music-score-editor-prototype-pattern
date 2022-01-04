from typing import Dict, List, Optional

from PySide2 import QtCore, QtGui, QtWidgets

from app.graphic import Graphic, Staff, WholeNote, HalfNote
from app.toolkit import TOOLKIT_ITEMS
from framework.tool import GraphicTool, RotateTool

# from framework.tool_without_prototype import GraphicTool, RotateTool


class MyGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.cached_prototypes: Dict[str, Graphic] = {}
        self.dragging_graphics: Optional[List[Graphic]] = None

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        # Reference: https://gist.github.com/benjaminirving/f45de3bbabbcacd3ca29
        items = self.parse_mime_data(event.mimeData())
        if items:
            event.acceptProposedAction()

            prototype_graphics = self.find_or_create_prototypes(items)
            pos = event.pos()
            scene_pos = self.mapToScene(pos.x(), pos.y())
            self.dragging_graphics = self.add_graphics(
                prototype_graphics, scene_pos
            )

    def dragMoveEvent(self, event: QtGui.QDragMoveEvent):
        items = self.parse_mime_data(event.mimeData())
        if items:
            event.acceptProposedAction()

            pos = event.pos()
            scene_pos = self.mapToScene(pos.x(), pos.y())
            for dragging_graphic in self.dragging_graphics:
                translated_pos = (
                    scene_pos - dragging_graphic.get_snap_point_translation()
                )
                dragging_graphic.setPos(translated_pos)

    def dragLeaveEvent(self, event: QtGui.QDragLeaveEvent):
        if self.dragging_graphics:
            self.remove_graphics(self.dragging_graphics)

    def dropEvent(self, event: QtGui.QDropEvent):
        items = self.parse_mime_data(event.mimeData())
        if items:
            event.acceptProposedAction()

            if not self.dragging_graphics:
                self.remove_graphics(self.dragging_graphics)

                pos = event.pos()
                scene_pos = self.mapToScene(pos.x(), pos.y())
                prototypes = self.find_or_create_prototypes(items)
                self.add_graphics(prototypes, scene_pos)

    def resizeEvent(self, event: QtGui.QResizeEvent):
        super().resizeEvent(event)

        # Update the scene rectangle to match the view
        rect = self.contentsRect()
        self.scene().setSceneRect(rect)

    def find_or_create_prototypes(
        self, items: List[Dict[str, str]]
    ) -> List[Graphic]:
        prototypes = []
        for item in items:
            name = item["name"]
            if name not in self.cached_prototypes:
                self.cached_prototypes[name] = self.create_prototype(name)
            prototypes.append(self.cached_prototypes[name])
        return prototypes

    def create_prototype(self, name: str) -> Graphic:
        if name == "staff":
            return Staff()
        elif name == "whole_note":
            return WholeNote()
        elif name == "half_note":
            return HalfNote()
        else:
            raise ValueError(f'Unknown item name "{name}"')

    def add_graphics(
        self, prototypes: List[Graphic], scene_pos: QtCore.QPoint
    ) -> List[Graphic]:
        new_graphics = []
        for prototype in prototypes:
            graphic_tool = GraphicTool(self.scene(), prototype)
            graphic_tool.add_item(scene_pos)
            new_graphic = graphic_tool.get_new_graphic()
            new_graphics.append(new_graphic)
        return new_graphics

    def remove_graphics(self, graphics: List[Graphic]):
        for graphic in graphics:
            self.scene().removeItem(graphic)

    def rotate_selected_items_right(self):
        items = self.scene().selectedItems()

        # Get list of graphics
        graphics = filter(lambda obj: isinstance(obj, Graphic), items)

        for graphic in graphics:
            rotate_tool = RotateTool(self.scene(), graphic)
            rotate_tool.rotate_right()
            new_graphic = rotate_tool.get_new_graphic()
            if new_graphic:
                new_graphic.setSelected(True)

    @staticmethod
    def parse_mime_data(mime_data: QtCore.QMimeData) -> List[Dict[str, str]]:
        if not mime_data.hasUrls():
            return []
        urls = mime_data.urls()
        items = filter(lambda item: item["mimeData"] in urls, TOOLKIT_ITEMS)
        return list(items)
