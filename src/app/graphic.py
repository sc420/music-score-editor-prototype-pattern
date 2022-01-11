from __future__ import annotations

from typing import Any, cast, Dict, List, Optional
import math

from PySide2 import QtCore, QtGui, QtSvg, QtWidgets


class Graphic(QtWidgets.QGraphicsItemGroup):
    def __init__(
        self,
        parent: Optional[QtWidgets.QGraphicsItem] = None,
        old_graphic: Optional[Graphic] = None,
    ):
        super().__init__(parent)

        self.debug = True

        self.reuse_svg_renderers(old_graphic)

        self.init_children()
        self.init_flags()
        self.init_transform_origin_point()

    def itemChange(
        self, change: QtWidgets.QGraphicsItem.GraphicsItemChange, value: Any
    ) -> Any:
        # Reference: https://www.walletfox.com/course/qgraphicsitemsnaptogrid.php
        if (
            change == QtWidgets.QGraphicsItem.ItemPositionChange
            and self.scene()
        ):
            new_pos = cast(QtCore.QPointF, value)
            new_pos = self.constrain_item_inside_scene(new_pos)
            new_pos = self.snap_item_to_nearest_item(new_pos)
            return new_pos

        return super().itemChange(change, value)

    def reuse_svg_renderers(self, old_graphic: Optional[Graphic]):
        if old_graphic:
            # Reuse the SVG renderers so we don't need to parse the SVG files
            # again
            # Reference: https://doc.qt.io/qt-5/qgraphicssvgitem.html#setSharedRenderer
            self.svg_renderers = old_graphic.svg_renderers
        else:
            self.svg_renderers: Dict[str, QtSvg.QSvgRenderer] = {}

    def init_children(self):
        children = self.create_children()
        for child in children:
            self.addToGroup(child)

        if self.debug:
            self.add_debug_rectangles(children)

    def add_debug_rectangles(self, children: List[QtWidgets.QGraphicsItem]):
        for child in children:
            child_rect = child.sceneBoundingRect()
            child_rect.adjust(-3, -3, 3, 3)  # Inflate a little bit
            highlight_rect = QtWidgets.QGraphicsRectItem(child_rect)
            highlight_rect.setPen(QtGui.QPen(QtCore.Qt.red))
            self.addToGroup(highlight_rect)

        group_rect = self.sceneBoundingRect()
        group_rect.adjust(-3, -3, 3, 3)  # Inflate a little bit
        highlight_rect = QtWidgets.QGraphicsRectItem(group_rect)
        highlight_rect.setPen(QtGui.QPen(QtCore.Qt.blue))
        self.addToGroup(highlight_rect)

    def init_flags(self):
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, True)

    def init_transform_origin_point(self):
        self.setTransformOriginPoint(self.get_center_translation())

    def constrain_item_inside_scene(
        self, new_pos: QtCore.QPointF
    ) -> QtCore.QPointF:
        # Calculate new bounding rectangle if we apply the new position
        scene_rect = self.scene().sceneRect()
        item_rect = self.sceneBoundingRect()
        delta = new_pos - self.pos()
        item_rect.translate(delta)
        if not scene_rect.contains(item_rect):
            # Snap to the edges
            if item_rect.left() < scene_rect.left():
                adjustment_x = scene_rect.left() - item_rect.left()
            elif scene_rect.right() < item_rect.right():
                adjustment_x = scene_rect.right() - item_rect.right()
            else:
                adjustment_x = 0

            if item_rect.top() < scene_rect.top():
                adjustment_y = scene_rect.top() - item_rect.top()
            elif scene_rect.bottom() < item_rect.bottom():
                adjustment_y = scene_rect.bottom() - item_rect.bottom()
            else:
                adjustment_y = 0

            new_pos.setX(new_pos.x() + adjustment_x)
            new_pos.setY(new_pos.y() + adjustment_y)
        return new_pos

    def snap_item_to_nearest_item(
        self, new_pos: QtCore.QPointF
    ) -> QtCore.QPointF:
        if not self.can_snap_to_others():
            return new_pos

        src_snap_point = new_pos + self.get_snap_point_translation()

        scene_rect = self.scene().sceneRect()
        items = self.scene().items(scene_rect)

        # Get list of other groups
        groups = filter(
            lambda obj: (isinstance(obj, Graphic) and obj != self), items
        )

        # Keep only the groups that can be snapped
        groups = filter(lambda obj: obj.can_be_snapped(), groups)

        # Keep only the groups that have bounding rectangles on the source snap
        # point (e.g., the hole of the whole note)
        groups = filter(
            lambda obj: (obj.sceneBoundingRect().contains(src_snap_point)),
            groups,
        )

        nearest_snap_point = None
        nearest_snap_distance = float("inf")
        for group in groups:
            local_src_snap_point = group.mapFromScene(src_snap_point)
            local_dest_snap_point = group.get_dest_snap_point(
                local_src_snap_point
            )
            dest_snap_point = group.mapToScene(local_dest_snap_point)

            delta = dest_snap_point - new_pos
            snap_distance = math.sqrt((delta.x() ** 2) + (delta.y() ** 2))
            if snap_distance < nearest_snap_distance:
                nearest_snap_point = dest_snap_point
                nearest_snap_distance = snap_distance

        if nearest_snap_point:
            # We need to minus the translation since we want the point of the
            # top-left coordinate, not the snap point
            new_pos = nearest_snap_point - self.get_snap_point_translation()
        return new_pos

    def clone(self) -> Graphic:
        raise NotImplementedError()

    def create_children(self) -> List[QtWidgets.QGraphicsItem]:
        raise NotImplementedError()

    def find_or_create_svg_item(self, filename: str) -> QtSvg.QGraphicsSvgItem:
        if not filename in self.svg_renderers:
            QtCore.qDebug(f'Create QSvgRenderer(filename="{filename}")')
            self.svg_renderers[filename] = QtSvg.QSvgRenderer(filename)
        item = QtSvg.QGraphicsSvgItem(self.parentItem())
        item.setSharedRenderer(self.svg_renderers[filename])
        return item

    def set_group_attributes(self, old_item: Graphic):
        self.setFlags(old_item.flags())
        self.setPos(old_item.pos())
        self.setRotation(old_item.rotation())

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
    def __init__(
        self,
        parent: Optional[QtWidgets.QGraphicsItem] = None,
        old_graphic: Optional[Graphic] = None,
    ):
        self.num_lines = 5
        self.horizontal_distance = 300
        # The height of the whole note is approximately 10 px
        self.vertical_gap = 10
        self.lines_offset = QtCore.QPointF(45, 41)

        super().__init__(parent, old_graphic)

    def clone(self) -> Graphic:
        cloned_graphic = Staff(self.parentItem(), self)
        cloned_graphic.set_group_attributes(self)
        return cloned_graphic

    def create_children(self) -> List[QtWidgets.QGraphicsItem]:
        items = []
        item = self.find_or_create_svg_item(":/graphics_view/icons/G-clef.svg")
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
        return self.rotation() == 0

    def get_dest_snap_point(self, local_pos: QtCore.QPointF) -> QtCore.QPointF:
        lines_size = QtCore.QSizeF(
            self.horizontal_distance, self.num_lines * self.vertical_gap
        )
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
        closest_diff = float("inf")
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
        return self.rotation() == 0


class WholeNote(MusicalNote):
    def clone(self) -> Graphic:
        cloned_graphic = WholeNote(self.parentItem(), self)
        cloned_graphic.set_group_attributes(self)
        return cloned_graphic

    def create_children(self) -> List[QtWidgets.QGraphicsItem]:
        items = [
            self.find_or_create_svg_item(
                ":/graphics_view/icons/whole_note.svg")
        ]
        return items

    def get_snap_point_translation(self) -> QtCore.QPointF:
        translation = self.get_center_translation()
        return QtCore.QPointF(translation.x(), translation.y() + 13)


class HalfNote(MusicalNote):
    def clone(self) -> Graphic:
        cloned_graphic = HalfNote(self.parentItem(), self)
        cloned_graphic.set_group_attributes(self)
        return cloned_graphic

    def create_children(self) -> List[QtWidgets.QGraphicsItem]:
        items = [
            self.find_or_create_svg_item(":/graphics_view/icons/half_note.svg")
        ]
        return items

    def get_snap_point_translation(self) -> QtCore.QPointF:
        translation = self.get_center_translation()
        return QtCore.QPointF(translation.x(), translation.y() + 13)
