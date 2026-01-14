"""Слушатель хоткеев через keyboard."""

import keyboard
from PyQt6.QtCore import QObject, QTimer, pyqtSignal


class HotkeyListener(QObject):
    """Слушатель Alt+T."""

    activated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.timer = None
        self.was_pressed = False

    def start(self):
        """Запуск."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._check)
        self.timer.start(50)

    def _check(self):
        """Проверка нажатия."""
        try:
            pressed = keyboard.is_pressed('alt+t')

            if pressed and not self.was_pressed:
                self.activated.emit()

            self.was_pressed = pressed
        except:
            pass

    def stop(self):
        """Остановка."""
        if self.timer:
            self.timer.stop()
            self.timer = None