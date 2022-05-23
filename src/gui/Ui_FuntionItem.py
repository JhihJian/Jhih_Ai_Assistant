# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FunctionItem.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QPushButton,
                               QSizePolicy, QWidget)
import gui.resources_rc


class Ui_FunctionItem(object):
    def setupUi(self, FunctionItem):
        if not FunctionItem.objectName():
            FunctionItem.setObjectName(u"FunctionItem")
        FunctionItem.resize(285, 54)
        self.online_icon = QLabel(FunctionItem)
        self.online_icon.setObjectName(u"online_icon")
        self.online_icon.setEnabled(True)
        self.online_icon.setGeometry(QRect(120, 10, 50, 50))
        self.online_icon.setPixmap(QPixmap(u":/icon/images/online.png"))
        self.online_icon.setScaledContents(True)
        self.offline_icon = QLabel(FunctionItem)
        self.offline_icon.setObjectName(u"offline_icon")
        self.offline_icon.setEnabled(True)
        self.offline_icon.setGeometry(QRect(120, 10, 50, 50))
        self.offline_icon.setPixmap(QPixmap(u":/icon/images/offline.png"))
        self.offline_icon.setScaledContents(True)
        self.function_button = QPushButton(FunctionItem)
        self.function_button.setObjectName(u"function_button")
        self.function_button.setGeometry(QRect(0, 0, 111, 51))
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.function_button.sizePolicy().hasHeightForWidth())
        self.function_button.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font.setPointSize(12)
        self.function_button.setFont(font)
        self.function_button.setFlat(True)
        self.start_button = QPushButton(FunctionItem)
        self.start_button.setObjectName(u"start_button")
        self.start_button.setGeometry(QRect(160, 0, 121, 51))
        self.quit_button = QPushButton(FunctionItem)
        self.quit_button.setObjectName(u"quit_button")
        self.quit_button.setGeometry(QRect(160, 0, 121, 51))

        self.retranslateUi(FunctionItem)

        self.function_button.setDefault(False)

        QMetaObject.connectSlotsByName(FunctionItem)

    # setupUi

    def retranslateUi(self, FunctionItem):
        FunctionItem.setWindowTitle(QCoreApplication.translate("FunctionItem", u"Frame", None))
        self.online_icon.setText("")
        self.offline_icon.setText("")
        self.function_button.setText(QCoreApplication.translate("FunctionItem", u"PushButton", None))
        self.start_button.setText(QCoreApplication.translate("FunctionItem", u"START", None))
        self.quit_button.setText(QCoreApplication.translate("FunctionItem", u"QUIT", None))
    # retranslateUi
