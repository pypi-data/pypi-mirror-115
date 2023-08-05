from PySide2.QtWidgets import QTabWidget
from QtDesign.QtdWidgets import QRichTabBar


class QRichTabWidget(QTabWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.tab = QRichTabBar(self)
        self.setTabBar(self.tab)

    def tabLabelText(self, index: int):
        return self.tab.tabLabelText(index)

    def setTabLabelText(self, index: int, text: str):
        self.tab.setTabLabelText(index, text)