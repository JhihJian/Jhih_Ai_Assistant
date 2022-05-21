from PySide6.QtWidgets import QWidget

from gui.Ui_FuntionItem import Ui_FunctionItem


class FunctionItem(QWidget, Ui_FunctionItem):
    def __init__(self, parent=None):
        # super(FunctionItem, self).__init__()
        QWidget.__init__(self, parent)
        self.setupUi(self)
