"""Стили приложения."""


def get_stylesheet() -> str:
    """Возвращает таблицу стилей."""
    return """
    #container {
        background-color: #1e1e2e;
        border-radius: 12px;
        border: 1px solid #313244;
    }

    #titleLabel {
        color: #cdd6f4;
        font-size: 16px;
        font-weight: bold;
        padding: 5px;
    }

    #minimizeBtn, #closeBtn {
        background-color: transparent;
        border: none;
        border-radius: 15px;
        color: #6c7086;
        font-size: 14px;
        font-weight: bold;
    }

    #minimizeBtn:hover {
        background-color: #45475a;
        color: #f9e2af;
    }

    #closeBtn:hover {
        background-color: #f38ba8;
        color: #1e1e2e;
    }

    QComboBox {
        background-color: #313244;
        border: 1px solid #45475a;
        border-radius: 6px;
        color: #cdd6f4;
        padding: 8px 12px;
        font-size: 13px;
        min-width: 120px;
    }

    QComboBox:hover {
        border-color: #89b4fa;
    }

    QComboBox::drop-down {
        border: none;
        width: 30px;
    }

    QComboBox::down-arrow {
        image: none;
        border: none;
    }

    QComboBox QAbstractItemView {
        background-color: #313244;
        border: 1px solid #45475a;
        border-radius: 6px;
        color: #cdd6f4;
        selection-background-color: #45475a;
    }

    #swapBtn {
        background-color: #45475a;
        border: none;
        border-radius: 6px;
        color: #89b4fa;
        font-size: 18px;
        font-weight: bold;
    }

    #swapBtn:hover {
        background-color: #585b70;
    }

    QTextEdit {
        background-color: #313244;
        border: 1px solid #45475a;
        border-radius: 8px;
        color: #cdd6f4;
        font-size: 14px;
        padding: 10px;
        selection-background-color: #585b70;
    }

    QTextEdit:focus {
        border-color: #89b4fa;
    }

    #inputText {
        min-height: 80px;
    }

    #outputText {
        min-height: 80px;
        background-color: #181825;
    }

    #actionBtn {
        background-color: #45475a;
        border: none;
        border-radius: 6px;
        color: #cdd6f4;
        font-size: 12px;
        padding: 8px 12px;
    }

    #actionBtn:hover {
        background-color: #585b70;
    }

    #translateBtn {
        background-color: #89b4fa;
        border: none;
        border-radius: 6px;
        color: #1e1e2e;
        font-size: 13px;
        font-weight: bold;
        padding: 8px 16px;
    }

    #translateBtn:hover {
        background-color: #b4befe;
    }

    #translateBtn:disabled {
        background-color: #45475a;
        color: #6c7086;
    }

    #statusLabel {
        color: #6c7086;
        font-size: 11px;
        padding: 2px;
    }

    QScrollBar:vertical {
        background-color: #313244;
        width: 8px;
        border-radius: 4px;
    }

    QScrollBar::handle:vertical {
        background-color: #45475a;
        border-radius: 4px;
        min-height: 20px;
    }

    QScrollBar::handle:vertical:hover {
        background-color: #585b70;
    }

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    """