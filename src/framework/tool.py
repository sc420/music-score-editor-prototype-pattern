import sys

from PySide2 import QtCore, QtWidgets

from app.graphic import Graphic


class Tool:
    def __init__(self, scene: QtWidgets.QGraphicsScene):
        self.scene = scene


class GraphicTools(Tool):
    def __init__(self,
                 scene: QtWidgets.QGraphicsScene,
                 prototype_graphic: Graphic):
        super().__init__(scene)
        self.prototype_graphic = prototype_graphic

    def add_item(self, pos: QtCore.QPointF):
        new_graphic = self.prototype_graphic.clone()
        translated_pos = pos - new_graphic.get_snap_point_translation()
        new_graphic.setPos(translated_pos)
        self.scene.addItem(new_graphic)
