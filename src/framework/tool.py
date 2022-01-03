from typing import Optional

from PySide2 import QtCore, QtWidgets

from app.graphic import Graphic


class Tool:
    def __init__(self, scene: QtWidgets.QGraphicsScene):
        self.scene = scene
        self.new_graphic = None

    def get_new_graphic(self) -> Optional[Graphic]:
        return self.new_graphic


class GraphicTool(Tool):
    def __init__(self,
                 scene: QtWidgets.QGraphicsScene,
                 prototype_graphic: Graphic):
        super().__init__(scene)
        self.prototype_graphic = prototype_graphic

    def add_item(self, pos: QtCore.QPointF):
        self.new_graphic = self.prototype_graphic.clone()
        translated_pos = pos - self.new_graphic.get_snap_point_translation()
        self.new_graphic.setPos(translated_pos)
        self.scene.addItem(self.new_graphic)


class RotateTool(Tool):
    def __init__(self,
                 scene: QtWidgets.QGraphicsScene,
                 selected_graphic: Graphic):
        super().__init__(scene)
        self.selected_graphic = selected_graphic

    def rotate_right(self):
        self.new_graphic = self.selected_graphic.clone()
        new_rotation = (self.new_graphic.rotation() + 90) % 360
        self.new_graphic.setRotation(new_rotation)
        self.scene.removeItem(self.selected_graphic)
        self.scene.addItem(self.new_graphic)
