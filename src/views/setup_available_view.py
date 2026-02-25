from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QComboBox, QSpinBox, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal

class SetupAvailableView(QWidget):
    back_signal = pyqtSignal()
    start_signal = pyqtSignal(str, str, int) # difficulty, quiz_id, time_limit
    
    def __init__(self):
        super().__init__()
        self.available_data = {}
        self.selected_diff = None
        self.diff_buttons = []
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        self.btn_back = QPushButton("⬅ Quay lại")
        self.btn_back.setProperty("class", "secondary")
        self.btn_back.clicked.connect(lambda: self.back_signal.emit())
        header_layout.addWidget(self.btn_back)
        
        header = QLabel("Chọn Đề Có Sẵn")
        header.setObjectName("headerTitle")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(header, stretch=1)
        
        spacer = QWidget()
        spacer.setFixedWidth(self.btn_back.sizeHint().width())
        header_layout.addWidget(spacer)
        layout.addLayout(header_layout)
        
        # Selection Card
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(25)
        
        # Difficulty Label
        diff_lbl = QLabel("Chọn độ khó:")
        diff_lbl.setStyleSheet("font-weight: bold; font-size: 14pt;")
        card_layout.addWidget(diff_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 5 Difficulty Buttons Layout
        diff_buttons_layout = QHBoxLayout()
        diff_buttons_layout.setSpacing(15)
        
        colors = [
            "#48BB78", # Green (Level 1)
            "#38B2AC", # Teal (Level 2)
            "#ECC94B", # Yellow (Level 3)
            "#ED8936", # Orange (Level 4)
            "#E53E3E"  # Red (Level 5)
        ]
        
        for i in range(1, 6):
            btn = QPushButton(f"Cấp độ {i:02d}")
            # Base style with disabled color fallback
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {colors[i-1]};
                    color: white;
                    border-radius: 8px;
                    font-size: 13pt;
                    padding: 15px 10px;
                }}
                QPushButton:disabled {{
                    background-color: #E2E8F0;
                    color: #A0AEC0;
                }}
            """)
            btn.setCheckable(True)
            # Create a localized closure scope for i
            btn.clicked.connect(lambda checked, level=f"{i:02d}": self.on_difficulty_selected(level))
            self.diff_buttons.append(btn)
            diff_buttons_layout.addWidget(btn)
            
        card_layout.addLayout(diff_buttons_layout)
        
        # Quiz Info Label (To replace the manual drop down)
        self.info_lbl = QLabel("Hệ thống sẽ bốc ngẫu nhiên 1 đề thi từ kho dữ liệu.")
        self.info_lbl.setStyleSheet("color: #718096; font-size: 11pt; font-style: italic;")
        card_layout.addWidget(self.info_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(card, stretch=1)
        
        # Bottom controls
        bottom_layout = QHBoxLayout()
        time_label = QLabel("Giới hạn thời gian (phút):")
        self.time_spin = QSpinBox()
        self.time_spin.setRange(0, 180)
        self.time_spin.setValue(45)
        self.time_spin.setSpecialValueText("Không G.hạn")
        
        self.btn_start = QPushButton("Bắt Đầu Làm Bài")
        self.btn_start.clicked.connect(self.on_start_clicked)
        
        bottom_layout.addWidget(time_label)
        bottom_layout.addWidget(self.time_spin)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.btn_start)
        
        layout.addLayout(bottom_layout)
        
    def populate(self, available_quizzes: dict):
        self.available_data = available_quizzes
        self.selected_diff = None
        self.btn_start.setEnabled(False)
        
        # Reset and verify availability
        for i, btn in enumerate(self.diff_buttons):
            level_str = f"{int(i)+1:02d}"
            btn.setChecked(False)
            
            if level_str in available_quizzes and len(available_quizzes[level_str]) > 0:
                btn.setEnabled(True)
            else:
                btn.setEnabled(False)
                
    def on_difficulty_selected(self, level: str):
        self.selected_diff = level
        
        # Enforce exact one checked, Qt's auto-exclusive behavior sometimes struggles with dynamic color sheets
        for i, btn in enumerate(self.diff_buttons):
            if f"{i+1:02d}" == level:
                btn.setChecked(True)
                btn.setStyleSheet(btn.styleSheet() + "QPushButton { border: 3px solid #2D3748; }")
            else:
                btn.setChecked(False)
                # Remove outline hackily by reapplying original embedded style
                sheet = btn.styleSheet().replace("QPushButton { border: 3px solid #2D3748; }", "")
                btn.setStyleSheet(sheet)
                
        # Validate count for UI display
        count = len(self.available_data.get(level, []))
        self.info_lbl.setText(f"Có sẵn {count} đề thuộc Cấp độ {level}. Hệ thống sẽ bốc ngẫu nhiên 1 đề.")
        self.btn_start.setEnabled(True)
                
    def on_start_clicked(self):
        import random
        from models.history_manager import HistoryManager

        available_ids = self.available_data.get(self.selected_diff, [])
        if not available_ids:
            QMessageBox.warning(self, "Lỗi", "Không có mã đề nào tồn tại cho cấp độ này!")
            return
            
        # Optimization: Prevent sequential repetitions (Constraint 3)
        history = HistoryManager.load_history()
        recent_ids = []
        for session in history:
            if session.difficulty == self.selected_diff:
                recent_ids.append(session.quiz_id)
            if len(recent_ids) >= 3:
                break
                
        # Filter pool
        filtered_ids = [qid for qid in available_ids if qid not in recent_ids]
        
        # Fallback if filtered pool evaluates to zero (Too few quizzes available overall)
        if not filtered_ids:
            filtered_ids = available_ids
            
        q_id = random.choice(filtered_ids)
        time_limit = self.time_spin.value()
        
        self.start_signal.emit(self.selected_diff, q_id, time_limit)
