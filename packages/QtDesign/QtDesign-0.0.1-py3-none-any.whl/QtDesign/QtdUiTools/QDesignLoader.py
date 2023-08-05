# Copyright (c) 2011 Sebastian Wiesner <lunaryorn@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QDir, QMetaObject
from PySide2.QtWidgets import QWidget
from QtDesign.QtdWidgets import QCardWidget, QRichTabBar, QRichTabWidget

from typing import Optional


class QDesignLoader(QUiLoader):

    def __init__(self, baseInstance, customWidgets: QWidget = None):
        """
        Create a loader for the given ``baseInstance``.
        The user interface is created in ``baseInstance``, which must be an
        instance of the top-level class in the user interface to load, or a
        subclass thereof.
        ``customWidgets`` is a dictionary mapping from class name to class object
        for widgets that you've promoted in the Qt Designer interface. Usually,
        this should be done by calling registerCustomWidget on the QUiLoader, but
        with PySide 1.1.2 on Ubuntu 12.04 x86_64 this causes a segfault.
        ``parent`` is the parent object of this loader.
        """

        super().__init__()
        self.baseInstance = baseInstance
        self.customWidgets = customWidgets

    def createWidget(self, className, parent = None, name = ""):
        """
        Function that is called for each widget defined in ui file,
        overridden here to populate parent instead.
        """

        if parent is None and self.baseInstance:
            return self.baseInstance

        else:
            if className in self.availableWidgets() + ["Line"]:
                # If widget is native or 'Line' element from QtDesigner, create normally
                widget = QUiLoader.createWidget(self, className, parent, name)
            else:
                # If not in the list of availableWidgets, must be a custom widget
                # this will raise KeyError if the user has not supplied the
                # relevant className in the dictionary, or TypeError, if
                # customWidgets is None
                try:
                    widget = self.customWidgets[className](parent)

                except (TypeError, KeyError) as e:
                    raise Exception(
                        "No custom widget "
                        + className
                        + " found in customWidgets param of QDesignLoader __init__."
                    )

            # Add widget as attribute of parent window.
            if self.baseInstance:
                setattr(self.baseInstance, name, widget)

            return widget


def loadUi(uifile, parent = None, customWidgets: 'dict[str, QWidget]' = {}, workingDirectory: Optional[QDir] = None):
    """
    Dynamically load a user interface from the given ``uifile``.
    ``uifile`` is a string containing a file name of the UI file to load.
    If ``parent`` is ``None``, the a new instance of the top-level widget
    will be created.  Otherwise, the user interface is created within the given
    ``parent``.  In this case ``parent`` must be an instance of the
    top-level widget class in the UI file to load, or a subclass thereof.  In
    other words, if you've created a ``QMainWindow`` interface in the designer,
    ``parent`` must be a ``QMainWindow`` or a subclass thereof, too.  You
    cannot load a ``QMainWindow`` UI file with a plain
    :class:`~PySide.QtGui.QWidget` as ``parent``.
    ``customWidgets`` is a dictionary mapping from class name to class object
    for widgets that you've promoted in the Qt Designer interface. Usually,
    this should be done by calling registerCustomWidget on the QUiLoader, but
    with PySide 1.1.2 on Ubuntu 12.04 x86_64 this causes a segfault.
    :method:`~PySide.QtCore.QMetaObject.connectSlotsByName()` is called on the
    created user interface, so you can implemented your slots according to its
    conventions in your widget class.
    Return ``parent``, if ``parent`` is not ``None``.  Otherwise
    return the newly created instance of the user interface.
    """

    qtdWidgets = [QCardWidget, QRichTabBar, QRichTabWidget]

    customWidgets.update({widget.__name__: widget for widget in qtdWidgets})
    loader = QDesignLoader(parent, customWidgets)

    if workingDirectory is not None:
        loader.setWorkingDirectory(workingDirectory)

    ui = loader.load(uifile)
    QMetaObject.connectSlotsByName(ui)
    return ui
