from PySide2 import QtCore, QtGui, QtWidgets


class MyListView(QtWidgets.QListView):
    def startDrag(self, supportedActions: QtCore.Qt.DropActions):
        # Disable the icon while dragging
        # Reference: https://stackoverflow.com/a/25433268
        listsQModelIndex = self.selectedIndexes()
        if listsQModelIndex:
            dataQMimeData = self.model().mimeData(listsQModelIndex)
            if not dataQMimeData:
                return None
            dragQDrag = QtGui.QDrag(self)
            dragQDrag.setMimeData(dataQMimeData)
            defaultDropAction = QtCore.Qt.IgnoreAction
            if supportedActions & QtCore.Qt.CopyAction:
                defaultDropAction = QtCore.Qt.CopyAction
            dragQDrag.exec_(supportedActions, defaultDropAction)
