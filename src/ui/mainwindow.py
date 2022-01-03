# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from views.my_graphics_view import MyGraphicsView
from views.my_list_view import MyListView

import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionRotateRight = QAction(MainWindow)
        self.actionRotateRight.setObjectName(u"actionRotateRight")
        icon = QIcon()
        icon.addFile(u":/toolbar/icons/outline_rotate_right_black_48dp.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionRotateRight.setIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.listView = MyListView(self.splitter)
        self.listView.setObjectName(u"listView")
        self.listView.setMinimumSize(QSize(100, 300))
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listView.setDragEnabled(True)
        self.listView.setDragDropMode(QAbstractItemView.DragOnly)
        self.listView.setIconSize(QSize(64, 64))
        self.listView.setSpacing(10)
        self.listView.setUniformItemSizes(True)
        self.splitter.addWidget(self.listView)
        self.graphicsView = MyGraphicsView(self.splitter)
        self.graphicsView.setObjectName(u"graphicsView")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setMinimumSize(QSize(300, 300))
        self.splitter.addWidget(self.graphicsView)

        self.verticalLayout.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 25))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.actionRotateRight)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionRotateRight.setText(QCoreApplication.translate("MainWindow", u"Rotate Right", None))
#if QT_CONFIG(tooltip)
        self.actionRotateRight.setToolTip(QCoreApplication.translate("MainWindow", u"Rotate Right", None))
#endif // QT_CONFIG(tooltip)
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

