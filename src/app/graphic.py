from __future__ import annotations

from typing import List
import math

from PySide2 import QtCore, QtSvg, QtWidgets


class Graphic(QtWidgets.QGraphicsItemGroup):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, True)

        children = self.create_children()
        for child in children:
            self.addToGroup(child)

    def itemChange(self,
                   change: QtWidgets.QGraphicsItem.GraphicsItemChange,
                   value):
        # Reference: https://www.walletfox.com/course/qgraphicsitemsnaptogrid.php
        if (change == QtWidgets.QGraphicsItem.ItemPositionChange
                and self.scene()):
            value = self.constrain_item_inside_scene(value)
            value = self.snap_item_to_nearest_item(value)
            return value

        return super().itemChange(change, value)

    def constrain_item_inside_scene(self, value):
        scene_rect = self.scene().sceneRect()
        item_rect = self.boundingRect()
        item_rect.moveTopLeft(value)
        if not scene_rect.contains(item_rect):
            # Keep the item inside the scene rect
            value.setX(min(scene_rect.right() - item_rect.width(),
                       max(value.x(), scene_rect.left())))
            value.setY(min(scene_rect.bottom() - item_rect.height(),
                       max(value.y(), scene_rect.top())))
            return value
        return value

    def snap_item_to_nearest_item(self, value):
        src_snap_point = value + self.get_snap_point_translation()

        scene_rect = self.scene().sceneRect()
        items = self.scene().items(scene_rect)

        # Get list of other groups
        groups = filter(lambda obj: (
            isinstance(obj, Graphic) and obj != self
        ), items)

        # Keep only the groups that can be snapped
        groups = filter(lambda obj: obj.can_be_snapped(), groups)

        # Keep only the groups that have bounding rectangles on the source snap
        # point (e.g., the hole of the whole note)
        groups = filter(lambda obj: (
            obj.sceneBoundingRect().contains(src_snap_point)
        ), groups)

        nearest_snap_point = None
        nearest_snap_distance = float('inf')
        for group in groups:
            local_src_snap_point = group.mapFromScene(src_snap_point)
            local_dest_snap_point = group.get_dest_snap_point(
                local_src_snap_point)
            dest_snap_point = group.mapToScene(local_dest_snap_point)

            delta = dest_snap_point - value
            snap_distance = math.sqrt((delta.x() ** 2) + (delta.y() ** 2))
            if snap_distance < nearest_snap_distance:
                nearest_snap_point = dest_snap_point
                nearest_snap_distance = snap_distance

        if nearest_snap_point:
            # We need to minus the translation since we want the point of the
            # top-left coordinate, not the snap point
            value = (nearest_snap_point -
                     self.get_snap_point_translation())
        return value

    def clone(self) -> Graphic:
        raise NotImplementedError()

    def create_children(self) -> List[QtWidgets.QGraphicsItem]:
        raise NotImplementedError()

    def set_group_attributes(self, old_item: Graphic):
        self.setFlags(old_item.flags())
        self.setPos(old_item.pos())
        self.setTransform(old_item.transform())

    def get_snap_point_translation(self) -> QtCore.QPointF:
        """Gets translation from the top-left point (0,0) to the snap point
        (x,y) that should have positive values.

        For example, a 10x10 graphic can return (5,5) to make the snap point
        at the center.
        """
        return self.get_center_translation()

    def get_center_translation(self) -> QtCore.QPointF:
        rect = self.boundingRect()
        return rect.center()

    def can_snap_to_others(self) -> bool:
        return False

    def can_be_snapped(self) -> bool:
        return False

    def get_dest_snap_point(self, local_pos: QtCore.QPointF) -> QtCore.QPointF:
        return local_pos


class Staff(Graphic):
    def __init__(self, parent=None):
        self.num_lines = 5
        self.horizontal_distance = 300
        # The height of the whole note is approximately 10 px
        self.vertical_gap = 10
        self.lines_offset = QtCore.QPointF(45, 41)

        super().__init__(parent)

    def clone(self) -> Graphic:
        cloned_graphic = Staff(self.parentItem())
        cloned_graphic.set_group_attributes(self)
        return cloned_graphic

    def create_children(self) -> List[QtWidgets.QGraphicsItem]:
        items = []
        item = QtSvg.QGraphicsSvgItem(":/graphics_view/icons/G-clef.svg")
        item.setScale(2)
        items.append(item)

        for i in range(self.num_lines):
            y = self.lines_offset.y() + i * self.vertical_gap
            x1 = self.lines_offset.x()
            x2 = self.lines_offset.x() + self.horizontal_distance
            line = QtWidgets.QGraphicsLineItem(x1, y, x2, y)
            items.append(line)

        return items

    def get_snap_point_translation(self) -> QtCore.QPointF:
        # After adding the G clef to the group, the top left corner of the 5
        # lines is not (0, 0) anymore, the whole group now has large spacing
        # around G clef and lines, so I manually adjusted the translation by
        # trial and error
        return QtCore.QPointF(69, 71)

    def can_be_snapped(self) -> bool:
        return True

    def get_dest_snap_point(self, local_pos: QtCore.QPointF) -> QtCore.QPointF:
        lines_size = QtCore.QSizeF(
            self.horizontal_distance, self.num_lines * self.vertical_gap)
        snap_area = QtCore.QRectF(self.lines_offset, lines_size)

        # Slightly expand the snap area
        snap_area.setLeft(snap_area.left() - 5)
        snap_area.setRight(snap_area.right() + 5)
        snap_area.setTop(snap_area.top() - 5)
        snap_area.setBottom(snap_area.bottom() + 5)

        # We only want to snap the point inside the snap area, not inside the
        # entire bounding rectangle
        if not snap_area.contains(local_pos):
            return local_pos

        snap_y = None
        closest_diff = float('inf')
        # Line notes
        for i in range(self.num_lines):
            y = self.lines_offset.y() + i * self.vertical_gap
            diff = abs(y - local_pos.y())
            if diff < closest_diff:
                snap_y = y
                closest_diff = diff

        # Space notes
        for i in range(self.num_lines - 1):
            y = self.lines_offset.y() + (i + 0.5) * self.vertical_gap
            diff = abs(y - local_pos.y())
            if diff < closest_diff:
                snap_y = y
                closest_diff = diff

        return QtCore.QPointF(local_pos.x(), snap_y)


class MusicalNote(Graphic):
    def can_snap_to_others(self) -> bool:
        return True


class WholeNote(MusicalNote):
    def clone(self) -> Graphic:
        cloned_graphic = WholeNote(self.parentItem())
        cloned_graphic.set_group_attributes(self)
        return cloned_graphic

    def create_children(self) -> List[QtWidgets.QGraphicsItem]:
        items = [
            QtSvg.QGraphicsSvgItem(":/graphics_view/icons/whole_note.svg")
        ]
        return items

    def get_snap_point_translation(self) -> QtCore.QPointF:
        translation = self.get_center_translation()
        return QtCore.QPointF(translation.x(), translation.y() + 13)


class HalfNote(MusicalNote):
    def clone(self) -> Graphic:
        cloned_graphic = HalfNote(self.parentItem())
        cloned_graphic.set_group_attributes(self)
        return cloned_graphic

    def create_children(self) -> List[QtWidgets.QGraphicsItem]:
        items = [
            QtSvg.QGraphicsSvgItem(":/graphics_view/icons/half_note.svg")
        ]
        return items

    def get_snap_point_translation(self) -> QtCore.QPointF:
        translation = self.get_center_translation()
        return QtCore.QPointF(translation.x(), translation.y() + 13)
