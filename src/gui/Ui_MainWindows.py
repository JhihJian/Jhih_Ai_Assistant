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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
                               QLabel, QLayout, QMainWindow, QPlainTextEdit,
                               QPushButton, QSizePolicy, QStackedWidget, QStatusBar,
                               QVBoxLayout, QWidget)
import gui.resources_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 673)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutWidget1 = QWidget(self.centralwidget)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(0, 10, 781, 611))
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
        self.layoutWidget2.setGeometry(QRect(0, 0, 131, 301))
        self.verticalLayout = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.layoutWidget2)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.pushButton)

        self.function_button = QPushButton(self.layoutWidget2)
        self.function_button.setObjectName(u"function_button")
        sizePolicy1.setHeightForWidth(self.function_button.sizePolicy().hasHeightForWidth())
        self.function_button.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.function_button)

        self.log_button = QPushButton(self.layoutWidget2)
        self.log_button.setObjectName(u"log_button")
        sizePolicy1.setHeightForWidth(self.log_button.sizePolicy().hasHeightForWidth())
        self.log_button.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.log_button)

        self.setting_button = QPushButton(self.layoutWidget2)
        self.setting_button.setObjectName(u"setting_button")
        sizePolicy1.setHeightForWidth(self.setting_button.sizePolicy().hasHeightForWidth())
        self.setting_button.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.setting_button)

        self.two_split.addWidget(self.Left_Component_Frame)

        self.Right_Display_Frame = QFrame(self.layoutWidget1)
        self.Right_Display_Frame.setObjectName(u"Right_Display_Frame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(5)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.Right_Display_Frame.sizePolicy().hasHeightForWidth())
        self.Right_Display_Frame.setSizePolicy(sizePolicy2)
        self.Right_Display_Frame.setFrameShape(QFrame.StyledPanel)
        self.Right_Display_Frame.setFrameShadow(QFrame.Raised)
        self.stackedWidget = QStackedWidget(self.Right_Display_Frame)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(-1, -1, 641, 651))
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy3)
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
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.function_list.sizePolicy().hasHeightForWidth())
        self.function_list.setSizePolicy(sizePolicy4)
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
        sizePolicy4.setHeightForWidth(self.function_display.sizePolicy().hasHeightForWidth())
        self.function_display.setSizePolicy(sizePolicy4)
        self.function_display.setAutoFillBackground(False)
        self.function_display.setFrameShape(QFrame.StyledPanel)
        self.function_display.setFrameShadow(QFrame.Raised)
        self.function_widget = QStackedWidget(self.function_display)
        self.function_widget.setObjectName(u"function_widget")
        self.function_widget.setGeometry(QRect(10, 10, 301, 461))
        sizePolicy3.setHeightForWidth(self.function_widget.sizePolicy().hasHeightForWidth())
        self.function_widget.setSizePolicy(sizePolicy3)
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
        self.setting_page = QWidget()
        self.setting_page.setObjectName(u"setting_page")
        self.verticalLayoutWidget_2 = QWidget(self.setting_page)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(40, 90, 201, 491))
        self.setting_layout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.setting_layout.setObjectName(u"setting_layout")
        self.setting_layout.setContentsMargins(0, 0, 0, 0)
        self.auto_start_checkbox = QCheckBox(self.verticalLayoutWidget_2)
        self.auto_start_checkbox.setObjectName(u"auto_start_checkbox")

        self.setting_layout.addWidget(self.auto_start_checkbox)

        self.stackedWidget.addWidget(self.setting_page)

        self.two_split.addWidget(self.Right_Display_Frame)

        self.Button_Display_Frame = QFrame(self.centralwidget)
        self.Button_Display_Frame.setObjectName(u"Button_Display_Frame")
        self.Button_Display_Frame.setGeometry(QRect(0, 620, 781, 31))
        self.Button_Display_Frame.setFrameShape(QFrame.StyledPanel)
        self.Button_Display_Frame.setFrameShadow(QFrame.Raised)
        self.version_label = QLabel(self.Button_Display_Frame)
        self.version_label.setObjectName(u"version_label")
        self.version_label.setGeometry(QRect(710, 0, 61, 31))
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.version_label.sizePolicy().hasHeightForWidth())
        self.version_label.setSizePolicy(sizePolicy5)
        font2 = QFont()
        font2.setFamilies([u"Nirmala UI"])
        font2.setPointSize(16)
        self.version_label.setFont(font2)
        self.version_label.setAlignment(Qt.AlignCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(3)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u9875\u97621", None))
        self.function_button.setText(QCoreApplication.translate("MainWindow", u"\u529f\u80fd", None))
        self.log_button.setText(QCoreApplication.translate("MainWindow", u"\u65e5\u5fd7", None))
        self.setting_button.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u754c\u97621", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u529f\u80fd\u5217\u8868", None))
        self.function_title.setText(QCoreApplication.translate("MainWindow", u"\u8bf4\u660e", None))
        self.function_describe.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.LogTextArea.setPlainText("")
        self.auto_start_checkbox.setText(
            QCoreApplication.translate("MainWindow", u"\u662f\u5426\u5f00\u673a\u81ea\u542f", None))
        self.version_label.setText(QCoreApplication.translate("MainWindow", u"v1.0.0", None))
    # retranslateUi
