#!/usr/bin/env python3
"""Точка входа."""

import sys

# Скрываем консоль
if sys.platform == 'win32':
    import ctypes

    ctypes.windll.user32.ShowWindow(
        ctypes.windll.kernel32.GetConsoleWindow(), 0
    )

from PyQt6.QtWidgets import QApplication
from translator_app import TranslatorApp


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    translator = TranslatorApp()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()