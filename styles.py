"""Стили приложения."""


def get_stylesheet() -> str:
    return """
    #container {
        background-color: #1e1e2e;
        border-radius: 12px;
        border: 1px solid #313244;
    }
    
    #titleLabel {
        color: #cdd6f4;
        font-size: 18px;
        font-weight: bold;
        padding: 5px;
    }
    
    #minimizeBtn, #closeBtn {
        background-color: transparent;
        border: none;
        border-radius: 16px;
        color: #6c7086;
        font-size: 16px;
        font-weight: bold;
    }
    
    #minimizeBtn:hover { background-color: #45475a; color: #f9e2af; }
    #closeBtn:hover { background-color: #f38ba8; color: #1e1e2e; }
    
    QComboBox {
        background-color: #313244;
        border: 1px solid #45475a;
        border-radius: 8px;
        color: #cdd6f4;
        padding: 10px 14px;
        font-size: 15px;
        min-width: 140px;
    }
    
    QComboBox:hover { border-color: #89b4fa; }
    QComboBox::drop-down { border: none; width: 30px; }
    QComboBox::down-arrow { image: none; }
    
    QComboBox QAbstractItemView {
        background-color: #313244;
        border: 1px solid #45475a;
        border-radius: 8px;
        color: #cdd6f4;
        font-size: 15px;
        selection-background-color: #45475a;
    }
    
    #swapBtn {
        background-color: #45475a;
        border: none;
        border-radius: 8px;
        color: #89b4fa;
        font-size: 20px;
        font-weight: bold;
    }
    #swapBtn:hover { background-color: #585b70; }
    
    QTextEdit {
        background-color: #313244;
        border: 1px solid #45475a;
        border-radius: 10px;
        color: #cdd6f4;
        font-size: 16px;
        padding: 12px;
    }
    QTextEdit:focus { border-color: #89b4fa; }
    
    #inputText { min-height: 90px; }
    #outputText { min-height: 90px; background-color: #181825; }
    
    #actionBtn {
        background-color: #45475a;
        border: none;
        border-radius: 8px;
        color: #cdd6f4;
        font-size: 14px;
        padding: 10px 16px;
    }
    #actionBtn:hover { background-color: #585b70; }
    
    #translateBtn {
        background-color: #89b4fa;
        border: none;
        border-radius: 8px;
        color: #1e1e2e;
        font-size: 15px;
        font-weight: bold;
        padding: 10px 24px;
    }
    #translateBtn:hover { background-color: #b4befe; }
    #translateBtn:disabled { background-color: #45475a; color: #6c7086; }
    
    #statusLabel { color: #6c7086; font-size: 13px; }
    
    QScrollBar:vertical {
        background-color: #313244;
        width: 10px;
        border-radius: 5px;
    }
    QScrollBar::handle:vertical {
        background-color: #45475a;
        border-radius: 5px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
    """