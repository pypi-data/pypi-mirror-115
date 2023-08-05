from PySide2.QtCore import Qt
from PySide2.QtGui import QTextDocument
from PySide2.QtWidgets import QLabel, QTabBar


class QRichTabBar(QTabBar):
    def __init__(self, parent):
        super().__init__(parent)

    def tabLabelText(self, index: int):
        doc = QTextDocument()
        doc.setHtml(self.tabButton(index, QTabBar.LeftSide).text())
        return doc.toPlainText()

    def setTabLabelText(self, index: int, text: str):
        label = QLabel(self)
        label.setText(text)
        label.setAttribute(Qt.WA_TranslucentBackground)
        label.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.setTabButton(index, QTabBar.LeftSide, label)