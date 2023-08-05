# QtDesign
Custom widgets and utilities for PySide2

Most widgets are designed for use in Qt Designer through widget promotion and loaded via the `loadUi` method from `QDesignLoader`.

The `loadUi` method was included as a way to replicate the functionality of the `loadUi` method from PyQt's uic module. This allows ui files to be loaded into an existing widget instead of creating a new widget.