"""Окно переводчика."""

from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout,
    QTextEdit, QComboBox, QPushButton, QLabel,
    QSystemTrayIcon, QMenu, QFrame, QApplication
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QAction, QCursor, QIcon
import pyperclip

from translator_service import TranslatorService
from hotkey_listener import HotkeyListener
from styles import get_stylesheet

import os
import sys

def resource_path(relative_path):
    """ Получает абсолютный путь к ресурсу, работает и для dev, и для PyInstaller """
    try:
        # PyInstaller создает временную папку и хранит путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class TranslationWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, text, source, target):
        super().__init__()
        self.text = text
        self.source = source
        self.target = target

    def run(self):
        try:
            result = TranslatorService().translate(self.text, self.source, self.target)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class TranslatorApp(QMainWindow):
    LANGUAGES = {
        'auto': 'Авто', 'ru': 'Русский', 'en': 'English',
        'de': 'Deutsch', 'fr': 'Français', 'es': 'Español',
        'uk': 'Українська', 'pl': 'Polski',
    }

    def __init__(self):
        super().__init__()
        self.worker = None
        self.drag_position = None

        self._setup_window()
        self._build_ui()
        self._setup_tray()
        self._setup_hotkeys()

        print("TranslatorApp инициализирован")

    def _setup_window(self):
        self.setWindowTitle('Переводчик')
        self.setFixedSize(550, 450)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowIcon(QIcon("Icon.ico"))

    def _build_ui(self):
        container = QFrame(self)
        container.setObjectName('container')
        self.setCentralWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(15, 10, 15, 15)
        layout.setSpacing(12)

        # Заголовок
        header = QHBoxLayout()
        title = QLabel('🌐 Переводчик')
        title.setObjectName('titleLabel')
        header.addWidget(title)
        header.addStretch()

        minimize_btn = QPushButton('─')
        minimize_btn.setObjectName('minimizeBtn')
        minimize_btn.setFixedSize(32, 32)
        minimize_btn.clicked.connect(self.hide)
        header.addWidget(minimize_btn)

        close_btn = QPushButton('✕')
        close_btn.setObjectName('closeBtn')
        close_btn.setFixedSize(32, 32)
        close_btn.clicked.connect(self._quit_app)
        header.addWidget(close_btn)
        layout.addLayout(header)

        # Языки
        lang_layout = QHBoxLayout()
        self.source_lang = QComboBox()
        for code, name in self.LANGUAGES.items():
            self.source_lang.addItem(name, code)
        lang_layout.addWidget(self.source_lang)

        swap_btn = QPushButton('⇄')
        swap_btn.setObjectName('swapBtn')
        swap_btn.setFixedSize(45, 40)
        swap_btn.clicked.connect(self._swap_languages)
        lang_layout.addWidget(swap_btn)

        self.target_lang = QComboBox()
        for code, name in self.LANGUAGES.items():
            if code != 'auto':
                self.target_lang.addItem(name, code)
        self.target_lang.setCurrentText('Русский')
        lang_layout.addWidget(self.target_lang)
        layout.addLayout(lang_layout)

        # Ввод
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText('Введите текст...')
        self.input_text.setObjectName('inputText')
        layout.addWidget(self.input_text)

        # Кнопки
        buttons = QHBoxLayout()

        clear_btn = QPushButton('🗑 Очистить')
        clear_btn.setObjectName('actionBtn')
        clear_btn.clicked.connect(self._clear_fields)
        buttons.addWidget(clear_btn)

        paste_btn = QPushButton('📋 Вставить')
        paste_btn.setObjectName('actionBtn')
        paste_btn.clicked.connect(self._paste)
        buttons.addWidget(paste_btn)

        self.translate_btn = QPushButton('🔄 Перевод')
        self.translate_btn.setObjectName('translateBtn')
        self.translate_btn.clicked.connect(self._translate)
        buttons.addWidget(self.translate_btn)

        copy_btn = QPushButton('📑 Копировать')
        copy_btn.setObjectName('actionBtn')
        copy_btn.clicked.connect(self._copy)
        buttons.addWidget(copy_btn)
        layout.addLayout(buttons)

        # Вывод
        self.output_text = QTextEdit()
        self.output_text.setPlaceholderText('Перевод...')
        self.output_text.setReadOnly(True)
        self.output_text.setObjectName('outputText')
        layout.addWidget(self.output_text)

        self.status_label = QLabel('Alt+T — показать/скрыть')
        self.status_label.setObjectName('statusLabel')
        layout.addWidget(self.status_label)

        self.setStyleSheet(get_stylesheet())

    def _setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(resource_path("Icon.ico")))

        menu = QMenu()
        show_action = QAction('Показать', self)
        show_action.triggered.connect(self._show_window)
        menu.addAction(show_action)
        menu.addSeparator()
        quit_action = QAction('Выход', self)
        quit_action.triggered.connect(self._quit_app)
        menu.addAction(quit_action)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.activated.connect(self._tray_click)
        self.tray_icon.show()

    def _setup_hotkeys(self):
        print("Настройка хоткеев...")
        self.hotkey_listener = HotkeyListener()
        self.hotkey_listener.activated.connect(self._on_hotkey)
        self.hotkey_listener.start()

    def _on_hotkey(self):
        print(">>> Сигнал получен в _on_hotkey")
        if self.isVisible():
            self.hide()
        else:
            self._show_window()

    def _show_window(self):
        print("Показываем окно")

        try:
            text = pyperclip.paste()
            if text and text.strip():
                self.input_text.setText(text.strip())
        except:
            pass

        cursor = QCursor.pos()
        screen = self.screen().geometry()
        x = max(screen.left(), min(cursor.x() - self.width()//2, screen.right() - self.width()))
        y = max(screen.top(), min(cursor.y() - 50, screen.bottom() - self.height()))

        self.move(x, y)
        self.show()
        self.activateWindow()
        self.raise_()
        self.input_text.setFocus()

    def _translate(self):
        text = self.input_text.toPlainText().strip()
        if not text or (self.worker and self.worker.isRunning()):
            return

        self.translate_btn.setEnabled(False)
        self.translate_btn.setText('⏳...')

        self.worker = TranslationWorker(
            text,
            self.source_lang.currentData(),
            self.target_lang.currentData()
        )
        self.worker.finished.connect(self._on_done)
        self.worker.error.connect(self._on_error)
        self.worker.start()

    def _on_done(self, result):
        self.output_text.setText(result)
        self.translate_btn.setEnabled(True)
        self.translate_btn.setText('🔄 Перевод')
        self.status_label.setText('✓ Готово')
        self.worker = None

    def _on_error(self, error):
        self.output_text.setText(f'Ошибка: {error}')
        self.translate_btn.setEnabled(True)
        self.translate_btn.setText('🔄 Перевод')
        self.worker = None

    def _swap_languages(self):
        if self.source_lang.currentData() == 'auto':
            return
        src, tgt = self.source_lang.currentIndex(), self.target_lang.currentIndex()
        self.target_lang.setCurrentIndex(src - 1)
        self.source_lang.setCurrentIndex(tgt + 1)
        self.input_text.setText(self.output_text.toPlainText())
        self.output_text.clear()

    def _clear_fields(self):
        self.input_text.clear()
        self.output_text.clear()

    def _paste(self):
        try:
            self.input_text.setText(pyperclip.paste())
        except:
            pass

    def _copy(self):
        text = self.output_text.toPlainText()
        if text:
            pyperclip.copy(text)
            self.status_label.setText('✓ Скопировано')

    def _tray_click(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self._show_window()

    def _quit_app(self):
        self.hotkey_listener.stop()
        self.tray_icon.hide()
        QApplication.quit()

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.drag_position = e.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, e):
        if self.drag_position:
            self.move(e.globalPosition().toPoint() - self.drag_position)

    def mouseReleaseEvent(self, e):
        self.drag_position = None

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Escape:
            self.hide()
        elif e.key() == Qt.Key.Key_Return and e.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self._translate()