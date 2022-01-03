from PySide2 import QtCore, QtGui

TOOLKIT_ITEMS = [
    {
        "name": "staff",
        "mimeData": "data://toolkit/?item=staff",
        "icon": ":/toolkit/icons/staff.png",
        "text": "Staff",
    },
    {
        "name": "half_note",
        "mimeData": "data://toolkit/?item=half_note",
        "icon": ":/graphics_view/icons/half_note.svg",
        "text": "Half Note",
    },
    {
        "name": "whole_note",
        "mimeData": "data://toolkit/?item=whole_note",
        "icon": ":/graphics_view/icons/whole_note.svg",
        "text": "Whole Note",
    },
]


class ToolkitItemModel(QtGui.QStandardItemModel):
    def mimeData(self, indexes):
        mime_data = QtCore.QMimeData()
        urls = [TOOLKIT_ITEMS[index.row()]["mimeData"] for index in indexes]
        mime_data.setUrls(urls)
        return mime_data
