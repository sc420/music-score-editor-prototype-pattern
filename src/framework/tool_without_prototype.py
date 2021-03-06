from typing import Optional

from PySide2 import QtCore, QtWidgets

from app.graphic import Graphic, Staff, WholeNote, HalfNote


class Tool:
    def __init__(self, scene: QtWidgets.QGraphicsScene):
        self.scene = scene
        self.new_graphic = None

    def get_new_graphic(self) -> Optional[Graphic]:
        return self.new_graphic


class GraphicTool(Tool):
    def __init__(
        self, scene: QtWidgets.QGraphicsScene, prototype_graphic: Graphic
    ):
        """
        NOTE: It should not have prototype_graphic argument if we are not using
        prototype pattern. But we make the interface compatible with tool.py
        so that the client doesn't need to change code if the client imports
        this file.
        """
        super().__init__(scene)
        self.prototype_graphic = prototype_graphic

    def add_item(self, pos: QtCore.QPointF):
        self.new_graphic = self.fake_create_graphic()
        translated_pos = pos - self.new_graphic.get_snap_point_translation()
        self.new_graphic.setPos(translated_pos)
        self.scene.addItem(self.new_graphic)

    def fake_create_graphic(self) -> Graphic:
        """
        NOTE: It should be the client that creates the graphic tools. You can
        see that the client would create a bunch of subclasses in parallel of
        the Graphic subclasses if we move these code outside this file.
        """
        if isinstance(self.prototype_graphic, Staff):
            graphic_tool = StaffGraphicTool(self.scene, self.prototype_graphic)
        elif isinstance(self.prototype_graphic, WholeNote):
            graphic_tool = WholeNoteGraphicTool(
                self.scene, self.prototype_graphic
            )
        elif isinstance(self.prototype_graphic, HalfNote):
            graphic_tool = HalfNoteGraphicTool(
                self.scene, self.prototype_graphic
            )
        else:
            raise ValueError("Unknown type of prototype graphic")
        return graphic_tool.create_graphic()

    def create_graphic(self) -> Graphic:
        ...


class StaffGraphicTool(GraphicTool):
    def create_graphic(self) -> Graphic:
        return Staff()


class MusicalNoteGraphicTool(GraphicTool):
    ...


class WholeNoteGraphicTool(MusicalNoteGraphicTool):
    def create_graphic(self) -> Graphic:
        return WholeNote()


class HalfNoteGraphicTool(MusicalNoteGraphicTool):
    def create_graphic(self) -> Graphic:
        return HalfNote()


class RotateTool(Tool):
    def __init__(
        self, scene: QtWidgets.QGraphicsScene, selected_graphic: Graphic
    ):
        super().__init__(scene)
        self.selected_graphic = selected_graphic

    def rotate_right(self):
        self.new_graphic = self.selected_graphic.clone()
        new_rotation = (self.new_graphic.rotation() + 90) % 360
        self.new_graphic.setRotation(new_rotation)
        self.scene.removeItem(self.selected_graphic)
        self.scene.addItem(self.new_graphic)
