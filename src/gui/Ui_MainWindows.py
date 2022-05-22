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
        self.Left_Component_Frame = QFrame(self.layoutWidget1)
        self.Left_Component_Frame.setObjectName(u"Left_Component_Frame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Left_Component_Frame.sizePolicy().hasHeightForWidth())
        self.Left_Component_Frame.setSizePolicy(sizePolicy)
        self.Left_Component_Frame.setFrameShape(QFrame.StyledPanel)
        self.Left_Component_Frame.setFrameShadow(QFrame.Raised)
        self.layoutWidget2 = QWidget(self.Left_Component_Frame)
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


        self.two_split.addWidget(self.Left_Component_Frame)

        self.Right_Display_Frame = QFrame(self.layoutWidget1)
        self.Right_Display_Frame.setObjectName(u"Right_Display_Frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(5)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.Right_Display_Frame.sizePolicy().hasHeightForWidth())
        self.Right_Display_Frame.setSizePolicy(sizePolicy1)
        self.Right_Display_Frame.setFrameShape(QFrame.StyledPanel)
        self.Right_Display_Frame.setFrameShadow(QFrame.Raised)
        self.stackedWidget = QStackedWidget(self.Right_Display_Frame)
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
        self.function_page = QWidget()
        self.function_page.setObjectName(u"function_page")
        self.label_2 = QLabel(self.function_page)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(0, 0, 271, 101))
        self.label_2.setFont(font)
        self.layoutWidget3 = QWidget(self.function_page)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(-10, 120, 651, 481))
        self.function_page_layout = QHBoxLayout(self.layoutWidget3)
        self.function_page_layout.setObjectName(u"function_page_layout")
        self.function_page_layout.setContentsMargins(0, 0, 0, 0)
        self.function_list = QFrame(self.layoutWidget3)
        self.function_list.setObjectName(u"function_list")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.function_list.sizePolicy().hasHeightForWidth())
        self.function_list.setSizePolicy(sizePolicy3)
        self.function_list.setAutoFillBackground(False)
        self.function_list.setFrameShape(QFrame.StyledPanel)
        self.function_list.setFrameShadow(QFrame.Raised)
        self.verticalLayoutWidget = QWidget(self.function_list)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 0, 321, 481))
        self.functionListLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.functionListLayout.setSpacing(0)
        self.functionListLayout.setObjectName(u"functionListLayout")
        self.functionListLayout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.functionListLayout.setContentsMargins(0, 0, 0, 0)

        self.function_page_layout.addWidget(self.function_list)

        self.function_display = QFrame(self.layoutWidget3)
        self.function_display.setObjectName(u"function_display")
        sizePolicy3.setHeightForWidth(self.function_display.sizePolicy().hasHeightForWidth())
        self.function_display.setSizePolicy(sizePolicy3)
        self.function_display.setAutoFillBackground(False)
        self.function_display.setFrameShape(QFrame.StyledPanel)
        self.function_display.setFrameShadow(QFrame.Raised)
        self.function_widget = QStackedWidget(self.function_display)
        self.function_widget.setObjectName(u"function_widget")
        self.function_widget.setGeometry(QRect(10, 10, 301, 461))
        sizePolicy2.setHeightForWidth(self.function_widget.sizePolicy().hasHeightForWidth())
        self.function_widget.setSizePolicy(sizePolicy2)
        self.defaut_page = QWidget()
        self.defaut_page.setObjectName(u"defaut_page")
        self.function_title = QLabel(self.defaut_page)
        self.function_title.setObjectName(u"function_title")
        self.function_title.setGeometry(QRect(10, 0, 71, 41))
        self.function_describe = QLabel(self.defaut_page)
        self.function_describe.setObjectName(u"function_describe")
        self.function_describe.setGeometry(QRect(20, 50, 261, 41))
        self.function_widget.addWidget(self.defaut_page)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.function_widget.addWidget(self.page_3)

        self.function_page_layout.addWidget(self.function_display)

        self.stackedWidget.addWidget(self.function_page)
        self.log_page = QWidget()
        self.log_page.setObjectName(u"log_page")
        self.LogTextArea = QPlainTextEdit(self.log_page)
        self.LogTextArea.setObjectName(u"LogTextArea")
        self.LogTextArea.setGeometry(QRect(23, 60, 601, 571))
        font1 = QFont()
        font1.setFamilies([u"\u5b8b\u4f53"])
        font1.setPointSize(11)
        self.LogTextArea.setFont(font1)
        self.LogTextArea.setReadOnly(True)
        self.stackedWidget.addWidget(self.log_page)

        self.two_split.addWidget(self.Right_Display_Frame)

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
        self.function_title.setText(QCoreApplication.translate("MainWindow", u"\u8bf4\u660e", None))
        self.function_describe.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.LogTextArea.setPlainText("")
    # retranslateUi

