#!/usr/bin/env python3
"""Точка входа в приложение."""

import sys
import os

# Скрываем консоль на Windows
if sys.platform == 'win32':
    import ctypes

    ctypes.windll.user32.ShowWindow(
        ctypes.windll.kernel32.GetConsoleWindow(), 0
    )

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from translator_app import TranslatorApp


def main():
    # Включаем высокий DPI
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Не закрывать при скрытии окна

    translator = TranslatorApp()
    translator.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()