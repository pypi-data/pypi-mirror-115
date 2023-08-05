from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGridLayout, QPushButton, QWidget

from typing import Optional


class QCardWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        # Create QGridLayout as the layout manager for all Card widgets
        self.cardLayout = QGridLayout()

        # Set QPushButton as the container for Card widgets
        self.centralContainer = QPushButton()
        self.centralContainer.setLayout(self.cardLayout)

        # Create QGridLayout so QPushButton can be added to QWidget
        self.centralLayout = QGridLayout()
        self.centralLayout.addWidget(self.centralContainer)
        self.setLayout(self.centralLayout)

        # Make QPushButton fill QGridLayout
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

    def addWidget(self, widget: QWidget, row: Optional[int] = None, column: Optional[int] = None, rowSpan: Optional[int] = None, columnSpan: Optional[int] = None, alignment: Qt.Alignment() = None):
        widget.setParent(self.centralContainer)

        if(row is None and column is None and rowSpan is None and columnSpan is None and alignment is None):
            self.cardLayout.addWidget(widget)
        elif(rowSpan is None and columnSpan is None and alignment is None):
            self.cardLayout.addWidget(widget, row, column)
        elif(alignment is None):
            self.cardLayout.addWidget(widget, row, column, rowSpan, columnSpan)
        else:
            self.cardLayout.addWidget(widget, row, column, rowSpan, columnSpan, alignment)

        self.centralContainer.setMinimumSize(self.cardLayout.sizeHint())

    @property
    def clicked(self):
        return self.centralContainer.clicked