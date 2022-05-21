# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindows.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLayout, QMainWindow, QPlainTextEdit, QPushButton,
    QSizePolicy, QStackedWidget, QStatusBar, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 673)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutWidget1 = QWidget(self.centralwidget)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(10, 0, 781, 651))
        self.two_split = QHBoxLayout(self.layoutWidget1)
        self.two_split.setObjectName(u"two_split")
        self.two_split.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.layoutWidget1)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.layoutWidget2 = QWidget(self.frame_2)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(10, 70, 77, 195))
        self.verticalLayout = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.layoutWidget2)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.layoutWidget2)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.layoutWidget2)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.verticalLayout.addWidget(self.pushButton_3)


        self.two_split.addWidget(self.frame_2)

        self.frame = QFrame(self.layoutWidget1)
        self.frame.setObjectName(u"frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(5)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy1)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.stackedWidget = QStackedWidget(self.frame)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(-1, -1, 641, 651))
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy2)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(103, 161, 281, 211))
        font = QFont()
        font.setFamilies([u"Agency FB"])
        font.setPointSize(48)
        self.label.setFont(font)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.label_2 = QLabel(self.page_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(0, 0, 271, 101))
        self.label_2.setFont(font)
        self.layoutWidget3 = QWidget(self.page_2)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(-10, 120, 651, 481))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.function_list_frame = QFrame(self.layoutWidget3)
        self.function_list_frame.setObjectName(u"function_list_frame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(2)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.function_list_frame.sizePolicy().hasHeightForWidth())
        self.function_list_frame.setSizePolicy(sizePolicy3)
        self.function_list_frame.setAutoFillBackground(False)
        self.function_list_frame.setFrameShape(QFrame.StyledPanel)
        self.function_list_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayoutWidget = QWidget(self.function_list_frame)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 0, 181, 481))
        self.functionListLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.functionListLayout.setSpacing(0)
        self.functionListLayout.setObjectName(u"functionListLayout")
        self.functionListLayout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.functionListLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_2.addWidget(self.function_list_frame)

        self.frame_3 = QFrame(self.layoutWidget3)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(5)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy4)
        self.frame_3.setAutoFillBackground(False)
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_2.addWidget(self.frame_3)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.label_3 = QLabel(self.page_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(240, 210, 191, 181))
        self.label_3.setFont(font)
        self.LogTextArea = QPlainTextEdit(self.page_3)
        self.LogTextArea.setObjectName(u"LogTextArea")
        self.LogTextArea.setGeometry(QRect(23, 60, 601, 571))
        font1 = QFont()
        font1.setFamilies([u"\u5b8b\u4f53"])
        font1.setPointSize(11)
        self.LogTextArea.setFont(font1)
        self.LogTextArea.setReadOnly(True)
        self.stackedWidget.addWidget(self.page_3)

        self.two_split.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u9875\u97621", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u529f\u80fd", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u65e5\u5fd7", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u754c\u97621", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u754c\u97622", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u754c\u97623", None))
        self.LogTextArea.setPlainText("")
    # retranslateUi

