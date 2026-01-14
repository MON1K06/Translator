"""Слушатель глобальных горячих клавиш."""

from PyQt6.QtCore import QThread, pyqtSignal
import keyboard


class HotkeyListener(QThread):
    """Фоновый поток для отслеживания горячих клавиш."""

    activated = pyqtSignal()

    def __init__(self, hotkey: str = 'alt+t'):
        super().__init__()
        self.hotkey = hotkey
        self.running = True

    def run(self):
        """Запуск прослушивания."""
        keyboard.add_hotkey(self.hotkey, self._emit_signal)

        while self.running:
            keyboard.wait()

    def _emit_signal(self):
        """Отправка сигнала в главный поток."""
        self.activated.emit()

    def stop(self):
        """Остановка прослушивания."""
        self.running = False
        keyboard.unhook_all()
        self.quit()
        self.wait()