from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
import os

class MenuButton(QPushButton):
    def __init__(self, title: str, subtitle: str, color_hex: str, parent=None):
        super().__init__(parent)
        self.setFixedSize(320, 90)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color_hex};
                color: #FFFFFF;
                border-radius: 12px;
            }}
            QPushButton:hover {{
                border: 2px solid #2D3748;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 15, 10, 15)
        layout.setSpacing(4)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 15pt; font-weight: bold; background: transparent; color: white;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        sub_lbl = QLabel(subtitle)
        sub_lbl.setStyleSheet("font-size: 11pt; font-weight: normal; background: transparent; color: rgba(255, 255, 255, 0.8);")
        sub_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        layout.addWidget(title_lbl)
        layout.addWidget(sub_lbl)

class HomeView(QWidget):
    # Signals
    on_available = pyqtSignal()
    on_history = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)

        # Title
        title = QLabel("Hệ Thống Thi Trắc Nghiệm")
        title.setObjectName("headerTitle")
        title.setStyleSheet("font-size: 32px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Chọn phương thức tạo bài thi:")
        subtitle.setObjectName("subTitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        # Buttons Layout (Vertical)
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(20)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_available = MenuButton("📂 Bắt đầu làm ", "Lựa chọn độ khó bài làm", "#319795") # Teal
        self.btn_available.clicked.connect(lambda: self.on_available.emit())
        
        self.btn_history = MenuButton("🕒 Lịch Sử Làm Bài", "Xem lại biên bản 10 bài vừa thi", "#DD6B20") # Orange
        self.btn_history.clicked.connect(lambda: self.on_history.emit())
        
        btn_layout.addWidget(self.btn_available)
        btn_layout.addWidget(self.btn_history)
        
        layout.addLayout(btn_layout)
