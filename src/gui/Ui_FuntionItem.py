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
import resources_rc

class Ui_FunctionItem(object):
    def setupUi(self, FunctionItem):
        if not FunctionItem.objectName():
            FunctionItem.setObjectName(u"FunctionItem")
        FunctionItem.resize(180, 50)
        self.online_icon_2 = QLabel(FunctionItem)
        self.online_icon_2.setObjectName(u"online_icon_2")
        self.online_icon_2.setEnabled(True)
        self.online_icon_2.setGeometry(QRect(120, 10, 50, 50))
        self.online_icon_2.setPixmap(QPixmap(u":/icon/images/online.png"))
        self.online_icon_2.setScaledContents(True)
        self.offline_icon_2 = QLabel(FunctionItem)
        self.offline_icon_2.setObjectName(u"offline_icon_2")
        self.offline_icon_2.setEnabled(True)
        self.offline_icon_2.setGeometry(QRect(120, 10, 50, 50))
        self.offline_icon_2.setPixmap(QPixmap(u":/icon/images/offline.png"))
        self.offline_icon_2.setScaledContents(True)
        self.functionButton_2 = QPushButton(FunctionItem)
        self.functionButton_2.setObjectName(u"functionButton_2")
        self.functionButton_2.setGeometry(QRect(0, 0, 111, 51))
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.functionButton_2.sizePolicy().hasHeightForWidth())
        self.functionButton_2.setSizePolicy(sizePolicy)

        self.retranslateUi(FunctionItem)

        QMetaObject.connectSlotsByName(FunctionItem)
    # setupUi

    def retranslateUi(self, FunctionItem):
        FunctionItem.setWindowTitle(QCoreApplication.translate("FunctionItem", u"Frame", None))
        self.online_icon_2.setText("")
        self.offline_icon_2.setText("")
        self.functionButton_2.setText(QCoreApplication.translate("FunctionItem", u"PushButton", None))
    # retranslateUi

