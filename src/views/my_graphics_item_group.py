from PySide2 import QtCore, QtWidgets

class MyGraphicsItemGroup(QtWidgets.QGraphicsItemGroup):
    def boundingRect(self) -> QtCore.QRectF:
        return super().childrenBoundingRect()

    def itemChange(self, change, value):
        # Reference: https://www.walletfox.com/course/qgraphicsitemsnaptogrid.php
        if change == QtWidgets.QGraphicsItem.ItemPositionChange and self.scene():
            scene_rect = self.scene().sceneRect()
            item_rect = self.boundingRect()
            item_rect.moveTopLeft(value)
            if not scene_rect.contains(item_rect):
                # Keep the item inside the scene rect
                value.setX(min(scene_rect.right() - item_rect.width(), max(value.x(), scene_rect.left())))
                value.setY(min(scene_rect.bottom() - item_rect.height(), max(value.y(), scene_rect.top())))
                return value
        return super().itemChange(change, value)
