from __future__ import annotations

from typing import Optional

from PySide2 import QtCore, QtSvg, QtWidgets

from views.my_graphics_item_group import MyGraphicsItemGroup


class Graphic:
    def __init__(self, item: Optional[MyGraphicsItemGroup] = None):
        self.item = item or self.create_item()

    def clone(self) -> Graphic:
        raise NotImplementedError()

    def create_item(self) -> MyGraphicsItemGroup:
        raise NotImplementedError()

    def get_item(self) -> MyGraphicsItemGroup:
        return self.item

    def clone_graphic_item(self) -> MyGraphicsItemGroup:
        new_item = self.create_item()
        new_item.setFlags(self.item.flags())
        new_item.setPos(self.item.pos())
        new_item.setTransform(self.item.transform())
        return new_item

    def get_translation(self) -> QtCore.QPointF:
        return self.get_center_translation()

    def get_top_left_translation(self) -> QtCore.QPointF:
        rect = self.item.sceneBoundingRect()
        return (-rect.topLeft())

    def get_center_translation(self) -> QtCore.QPointF:
        rect = self.item.sceneBoundingRect()
        return (-rect.center())


class Staff(Graphic):
    def __init__(self, item: Optional[MyGraphicsItemGroup] = None):
        self.horizontal_distance = 300
        # The height of the whole note is approximately 10 px
        self.vertical_gap = 10
        self.lines_offset = QtCore.QPointF(45, 41)

        super().__init__(item)

    def clone(self) -> Graphic:
        new_item = self.clone_graphic_item()
        return Staff(new_item)

    def create_item(self) -> MyGraphicsItemGroup:
        group = MyGraphicsItemGroup()
        item = QtSvg.QGraphicsSvgItem(":/graphics_view/icons/G-clef.svg")
        item.setScale(2)
        group.addToGroup(item)

        for i in range(5):
            y = self.lines_offset.y() + i * self.vertical_gap
            x1 = self.lines_offset.x()
            x2 = self.lines_offset.x() + self.horizontal_distance
            line = QtWidgets.QGraphicsLineItem(x1, y, x2, y)
            group.addToGroup(line)

        group.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        group.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        group.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, True)

        return group

    def get_translation(self) -> QtCore.QPointF:
        translation = self.get_top_left_translation()
        # After adding the G clef to the group, the top left corner of the 5
        # lines is not (0, 0) anymore, the whole group now has large spacing
        # around G clef and lines, so I manually adjusted the translation by
        # trial and error
        return QtCore.QPointF(translation.x() - 69, translation.y() - 71)


class MusicalNote(Graphic):
    pass


class WholeNote(MusicalNote):
    def clone(self) -> Graphic:
        new_item = self.clone_graphic_item()
        return WholeNote(new_item)

    def create_item(self) -> MyGraphicsItemGroup:
        group = MyGraphicsItemGroup()
        item = QtSvg.QGraphicsSvgItem(":/graphics_view/icons/whole_note.svg")
        group.addToGroup(item)

        group.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        group.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        group.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, True)
        return group

    def get_translation(self) -> QtCore.QPointF:
        translation = self.get_center_translation()
        return QtCore.QPointF(translation.x(), translation.y() - 15)


class HalfNote(MusicalNote):
    def clone(self) -> Graphic:
        new_item = self.clone_graphic_item()
        return HalfNote(new_item)

    def create_item(self) -> MyGraphicsItemGroup:
        group = MyGraphicsItemGroup()
        item = QtSvg.QGraphicsSvgItem(":/graphics_view/icons/half_note.svg")
        group.addToGroup(item)

        group.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        group.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        group.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, True)
        return group

    def get_translation(self) -> QtCore.QPointF:
        translation = self.get_center_translation()
        return QtCore.QPointF(translation.x(), translation.y() - 15)
