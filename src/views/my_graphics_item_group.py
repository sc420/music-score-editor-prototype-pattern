from PySide2 import QtWidgets

class MyGraphicsItemGroup(QtWidgets.QGraphicsItemGroup):
    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemPositionChange and self.scene():
            rect = self.scene().sceneRect()
            print(f'rect = {rect}, value = {value}')
            if not rect.contains(value):
                # Keep the item inside the scene rect.
                value.setX(min(rect.right() - 20, max(value.x(), rect.left())))
                value.setY(min(rect.bottom() - 20, max(value.y(), rect.top())))
                return value
        return super().itemChange(change, value)
