"""Главное окно переводчика."""

from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout,
    QTextEdit, QComboBox, QPushButton, QLabel,
    QSystemTrayIcon, QMenu, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QAction, QCursor
import pyperclip

from translator_service import TranslatorService
from hotkey_listener import HotkeyListener
from styles import get_stylesheet


class TranslationWorker(QThread):
    """Фоновый поток для перевода."""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, text: str, source: str, target: str):
        super().__init__()
        self.text = text
        self.source = source
        self.target = target
        self.translator = TranslatorService()

    def run(self):
        try:
            result = self.translator.translate(
                self.text, self.source, self.target
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class TranslatorApp(QMainWindow):
    """Главное окно переводчика."""

    LANGUAGES = {
        'auto': 'Авто',
        'ru': 'Русский',
        'en': 'English',
        'de': 'Deutsch',
        'fr': 'Français',
        'es': 'Español',
        'it': 'Italiano',
        'zh-CN': '中文',
        'ja': '日本語',
        'ko': '한국어',
        'uk': 'Українська',
        'pl': 'Polski',
    }

    def __init__(self):
        super().__init__()
        self.worker = None
        self.drag_position = None

        self._setup_window()
        self._setup_ui()
        self._setup_tray()
        self._setup_hotkeys()
        self._apply_styles()

    def _setup_window(self):
        """Настройка окна."""
        self.setWindowTitle('Переводчик')
        self.setFixedSize(500, 400)

        # Безрамочное окно с тенью
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def _setup_ui(self):
        """Создание интерфейса."""
        # Главный контейнер с закругленными углами
        container = QFrame(self)
        container.setObjectName('container')
        self.setCentralWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(15, 10, 15, 15)
        layout.setSpacing(10)

        # Заголовок с кнопками управления
        header = self._create_header()
        layout.addLayout(header)

        # Селекторы языков
        lang_layout = self._create_language_selectors()
        layout.addLayout(lang_layout)

        # Поле ввода
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText('Введите текст для перевода...')
        self.input_text.setObjectName('inputText')
        layout.addWidget(self.input_text)

        # Кнопки действий
        buttons = self._create_buttons()
        layout.addLayout(buttons)

        # Поле вывода
        self.output_text = QTextEdit()
        self.output_text.setPlaceholderText('Перевод появится здесь...')
        self.output_text.setReadOnly(True)
        self.output_text.setObjectName('outputText')
        layout.addWidget(self.output_text)

        # Статус бар
        self.status_label = QLabel('Ctrl+Shift+T — показать/скрыть')
        self.status_label.setObjectName('statusLabel')
        layout.addWidget(self.status_label)

    def _create_header(self) -> QHBoxLayout:
        """Создание заголовка окна."""
        layout = QHBoxLayout()

        title = QLabel('🌐 Переводчик')
        title.setObjectName('titleLabel')
        layout.addWidget(title)

        layout.addStretch()

        # Кнопка сворачивания
        minimize_btn = QPushButton('─')
        minimize_btn.setObjectName('minimizeBtn')
        minimize_btn.setFixedSize(30, 30)
        minimize_btn.clicked.connect(self.hide)
        layout.addWidget(minimize_btn)

        # Кнопка закрытия
        close_btn = QPushButton('✕')
        close_btn.setObjectName('closeBtn')
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self._quit_app)
        layout.addWidget(close_btn)

        return layout

    def _create_language_selectors(self) -> QHBoxLayout:
        """Создание селекторов языков."""
        layout = QHBoxLayout()

        # Исходный язык
        self.source_lang = QComboBox()
        for code, name in self.LANGUAGES.items():
            self.source_lang.addItem(name, code)
        layout.addWidget(self.source_lang)

        # Кнопка смены направления
        swap_btn = QPushButton('⇄')
        swap_btn.setObjectName('swapBtn')
        swap_btn.setFixedSize(40, 35)
        swap_btn.clicked.connect(self._swap_languages)
        layout.addWidget(swap_btn)

        # Целевой язык
        self.target_lang = QComboBox()
        for code, name in self.LANGUAGES.items():
            if code != 'auto':
                self.target_lang.addItem(name, code)
        self.target_lang.setCurrentText('Русский')
        layout.addWidget(self.target_lang)

        return layout

    def _create_buttons(self) -> QHBoxLayout:
        """Создание кнопок действий."""
        layout = QHBoxLayout()

        # Очистить
        clear_btn = QPushButton('🗑 Очистить')
        clear_btn.setObjectName('actionBtn')
        clear_btn.clicked.connect(self._clear_fields)
        layout.addWidget(clear_btn)

        # Вставить из буфера
        paste_btn = QPushButton('📋 Вставить')
        paste_btn.setObjectName('actionBtn')
        paste_btn.clicked.connect(self._paste_from_clipboard)
        layout.addWidget(paste_btn)

        # Перевести
        self.translate_btn = QPushButton('🔄 Перевести')
        self.translate_btn.setObjectName('translateBtn')
        self.translate_btn.clicked.connect(self._translate)
        layout.addWidget(self.translate_btn)

        # Копировать результат
        copy_btn = QPushButton('📑 Копировать')
        copy_btn.setObjectName('actionBtn')
        copy_btn.clicked.connect(self._copy_result)
        layout.addWidget(copy_btn)

        return layout

    def _setup_tray(self):
        """Настройка иконки в трее."""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(
            self.style().StandardPixmap.SP_ComputerIcon
        ))

        # Контекстное меню
        tray_menu = QMenu()

        show_action = QAction('Показать', self)
        show_action.triggered.connect(self._show_window)
        tray_menu.addAction(show_action)

        tray_menu.addSeparator()

        quit_action = QAction('Выход', self)
        quit_action.triggered.connect(self._quit_app)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self._tray_activated)
        self.tray_icon.show()

    def _setup_hotkeys(self):
        """Настройка глобальных горячих клавиш."""
        self.hotkey_listener = HotkeyListener()
        self.hotkey_listener.activated.connect(self._on_hotkey)
        self.hotkey_listener.start()

    def _apply_styles(self):
        """Применение стилей."""
        self.setStyleSheet(get_stylesheet())

    def _on_hotkey(self):
        """Обработка нажатия горячей клавиши."""
        if self.isVisible():
            self.hide()
        else:
            self._show_with_clipboard()

    def _show_with_clipboard(self):
        """Показать окно с текстом из буфера обмена."""
        try:
            clipboard_text = pyperclip.paste()
            if clipboard_text and clipboard_text.strip():
                self.input_text.setText(clipboard_text.strip())
                # Автоматический перевод
                QTimer.singleShot(100, self._translate)
        except:
            pass

        self._show_window()

    def _show_window(self):
        """Показать окно по центру экрана или у курсора."""
        # Позиционируем у курсора
        cursor_pos = QCursor.pos()
        screen = self.screen().geometry()

        x = cursor_pos.x() - self.width() // 2
        y = cursor_pos.y() - 50

        # Не выходим за границы экрана
        x = max(screen.left(), min(x, screen.right() - self.width()))
        y = max(screen.top(), min(y, screen.bottom() - self.height()))

        self.move(x, y)
        self.show()
        self.activateWindow()
        self.input_text.setFocus()

    def _translate(self):
        """Запуск перевода."""
        text = self.input_text.toPlainText().strip()
        if not text:
            return

        source = self.source_lang.currentData()
        target = self.target_lang.currentData()

        self.translate_btn.setEnabled(False)
        self.translate_btn.setText('⏳ Перевод...')
        self.status_label.setText('Переводим...')

        self.worker = TranslationWorker(text, source, target)
        self.worker.finished.connect(self._on_translation_done)
        self.worker.error.connect(self._on_translation_error)
        self.worker.start()

    def _on_translation_done(self, result: str):
        """Перевод завершен."""
        self.output_text.setText(result)
        self.translate_btn.setEnabled(True)
        self.translate_btn.setText('🔄 Перевести')
        self.status_label.setText('✓ Готово')

    def _on_translation_error(self, error: str):
        """Ошибка перевода."""
        self.output_text.setText(f'Ошибка: {error}')
        self.translate_btn.setEnabled(True)
        self.translate_btn.setText('🔄 Перевести')
        self.status_label.setText('✗ Ошибка')

    def _swap_languages(self):
        """Поменять языки местами."""
        source_idx = self.source_lang.currentIndex()
        target_idx = self.target_lang.currentIndex()

        if self.source_lang.currentData() == 'auto':
            return

        # +1 потому что в target нет 'auto'
        self.target_lang.setCurrentIndex(source_idx - 1)
        self.source_lang.setCurrentIndex(target_idx + 1)

        # Меняем тексты
        source_text = self.input_text.toPlainText()
        target_text = self.output_text.toPlainText()
        self.input_text.setText(target_text)
        self.output_text.setText(source_text)

    def _clear_fields(self):
        """Очистить поля."""
        self.input_text.clear()
        self.output_text.clear()
        self.input_text.setFocus()

    def _paste_from_clipboard(self):
        """Вставить из буфера обмена."""
        try:
            text = pyperclip.paste()
            if text:
                self.input_text.setText(text)
        except:
            pass

    def _copy_result(self):
        """Копировать результат."""
        text = self.output_text.toPlainText()
        if text:
            pyperclip.copy(text)
            self.status_label.setText('✓ Скопировано!')

    def _tray_activated(self, reason):
        """Клик по иконке в трее."""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self._show_window()

    def _quit_app(self):
        """Выход из приложения."""
        self.hotkey_listener.stop()
        self.tray_icon.hide()
        from PyQt6.QtWidgets import QApplication
        QApplication.quit()

    # Перетаскивание окна
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event):
        if self.drag_position and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)

    def mouseReleaseEvent(self, event):
        self.drag_position = None

    def keyPressEvent(self, event):
        """Обработка клавиш."""
        if event.key() == Qt.Key.Key_Escape:
            self.hide()
        elif event.key() == Qt.Key.Key_Return and \
                event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self._translate()