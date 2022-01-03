from __future__ import annotations

from typing import Optional

from PySide2 import QtCore, QtSvg, QtWidgets


class Graphic:
    def __init__(self, item: Optional[QtWidgets.QGraphicsItem] = None):
        self.item = item or self.create_item()

    def clone(self) -> Graphic:
        raise NotImplementedError()

    def create_item(self) -> QtWidgets.QGraphicsItem:
        raise NotImplementedError()

    def get_item(self) -> QtWidgets.QGraphicsItem:
        return self.item

    def clone_graphic_item(self) -> QtWidgets.QGraphicsItem:
        new_item = self.create_item()
        new_item.setPos(self.item.pos())
        new_item.setTransform(self.item.transform())
        new_item.setFlags(self.item.flags())
        return new_item

    def get_translation(self) -> QtCore.QPointF:
        return self.get_center_translation()

    def get_center_translation(self) -> QtCore.QPointF:
        rect = self.item.sceneBoundingRect()
        return (-rect.center())


class Staff(Graphic):
    def clone(self) -> Graphic:
        new_item = self.clone_graphic_item()
        return Staff(new_item)

    def create_item(self) -> QtWidgets.QGraphicsItem:
        item = QtSvg.QGraphicsSvgItem(":/graphics_view/icons/G-clef.svg")
        return item


class MusicalNote(Graphic):
    pass


class WholeNote(MusicalNote):
    def clone(self) -> Graphic:
        new_item = self.clone_graphic_item()
        return WholeNote(new_item)

    def create_item(self) -> QtWidgets.QGraphicsItem:
        item = QtSvg.QGraphicsSvgItem(":/graphics_view/icons/whole_note.svg")
        item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        return item

    def get_translation(self) -> QtCore.QPointF:
        translation = self.get_center_translation()
        return QtCore.QPointF(translation.x(), translation.y() - 15)


class HalfNote(MusicalNote):
    def clone(self) -> Graphic:
        new_item = self.clone_graphic_item()
        return HalfNote(new_item)

    def create_item(self) -> QtWidgets.QGraphicsItem:
        item = QtSvg.QGraphicsSvgItem(":/graphics_view/icons/half_note.svg")
        item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        return item

    def get_translation(self) -> QtCore.QPointF:
        translation = self.get_center_translation()
        return QtCore.QPointF(translation.x(), translation.y() - 15)
