from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QGridLayout, QScrollArea, QFrame,
    QSizePolicy, QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal

class ResultView(QWidget):
    # Signals
    next_question_signal = pyqtSignal()
    prev_question_signal = pyqtSignal()
    goto_question_signal = pyqtSignal(int)
    restart_signal = pyqtSignal() # Làm bài mới
    retry_signal = pyqtSignal()   # Làm lại
    
    def __init__(self):
        super().__init__()
        self.nav_buttons = []
        self.init_ui()
        
    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Left Side: Result Content Area
        left_layout = QVBoxLayout()
        left_frame = QFrame()
        left_frame.setObjectName("card")
        left_frame.setLayout(left_layout)
        
        # Top Header (Score and Section)
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 10)
        
        top_row = QHBoxLayout()
        self.section_text = QLabel("")
        self.section_text.setWordWrap(True)
        self.section_text.setStyleSheet("font-size: 17px; font-weight: bold; font-style: italic; color: #2D3748;")
        self.section_text.hide()
        
        self.score_label = QLabel("Kết quả: 0 / 40 điểm")
        self.score_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #E53E3E;")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        top_row.addWidget(self.section_text, stretch=1)
        top_row.addWidget(self.score_label)
        
        self.progress_label = QLabel("Câu hỏi 1 / 40")
        self.progress_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #718096;")
        
        header_layout.addLayout(top_row)
        header_layout.addWidget(self.progress_label)
        left_layout.addLayout(header_layout)
        
        # Question Container
        q_container = QWidget()
        q_container.setObjectName("q_container")
        q_layout = QVBoxLayout(q_container)
        q_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Interactive Audio Mount Point
        self.media_layout = QVBoxLayout()
        q_layout.addLayout(self.media_layout)
        
        # Passage Text
        self.passage_text = QLabel("")
        self.passage_text.setWordWrap(True)
        self.passage_text.setStyleSheet("""
            font-size: 15px; 
            color: #4A5568; 
            background-color: #EDF2F7; 
            padding: 15px; 
            border-left: 4px solid #4A90E2;
            border-radius: 4px;
            margin-bottom: 15px;
        """)
        self.passage_text.setTextFormat(Qt.TextFormat.MarkdownText)
        self.passage_text.hide()
        
        # Question Text
        self.question_text = QLabel("Nội dung câu hỏi sẽ hiển thị ở đây...")
        self.question_text.setTextFormat(Qt.TextFormat.MarkdownText)
        self.question_text.setWordWrap(True)
        self.question_text.setStyleSheet("font-size: 16px; margin-top: 5px; margin-bottom: 20px; font-weight: bold;")
        
        q_layout.addWidget(self.passage_text)
        q_layout.addWidget(self.question_text)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(q_container)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        left_layout.addWidget(scroll_area, stretch=1)
        
        # Options Area
        self.options_layout = QVBoxLayout()
        self.options_layout.setSpacing(10)
        q_layout.addLayout(self.options_layout)
        
        # Explanation Area
        self.explanation_text = QLabel("")
        self.explanation_text.setWordWrap(True)
        self.explanation_text.setStyleSheet("""
            background-color: #EBF8FF;
            border-left: 4px solid #4299E1;
            padding: 10px;
            margin-top: 15px;
            color: #2B6CB0;
        """)
        self.explanation_text.hide()
        q_layout.addWidget(self.explanation_text)
        
        q_layout.addStretch()
        
        # Bottom Navigation
        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton("Câu Trước")
        self.prev_btn.setProperty("class", "secondary")
        self.prev_btn.clicked.connect(lambda: self.prev_question_signal.emit())
        
        self.next_btn = QPushButton("Câu Tiếp")
        self.next_btn.clicked.connect(lambda: self.next_question_signal.emit())
        
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(self.next_btn)
        left_layout.addLayout(nav_layout)
        
        # Right Side: Sidebar Navigation
        right_layout = QVBoxLayout()
        right_frame = QFrame()
        right_frame.setObjectName("card")
        right_frame.setFixedWidth(250)
        right_frame.setLayout(right_layout)
        
        right_header = QLabel("Danh sách câu hỏi")
        right_header.setObjectName("subTitle")
        right_layout.addWidget(right_header)
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(5)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        
        grid_widget = QWidget()
        grid_widget.setObjectName("grid_widget")
        grid_widget.setLayout(self.grid_layout)
        
        grid_scroll = QScrollArea()
        grid_scroll.setWidgetResizable(True)
        grid_scroll.setWidget(grid_widget)
        grid_scroll.setFrameShape(QFrame.Shape.NoFrame)
        grid_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        right_layout.addWidget(grid_scroll, stretch=1)
        
        # Bottom Right Action Buttons
        self.retry_btn = QPushButton("Làm Lại Bài Này")
        self.retry_btn.setStyleSheet("background-color: #48BB78; margin-bottom: 10px;") # Green
        self.retry_btn.clicked.connect(lambda: self.retry_signal.emit())
        right_layout.addWidget(self.retry_btn)
        
        self.restart_btn = QPushButton("Quay lại Main Menu")
        self.restart_btn.setStyleSheet("background-color: #E53E3E;") # Red
        self.restart_btn.clicked.connect(lambda: self.restart_signal.emit())
        right_layout.addWidget(self.restart_btn)
        
        main_layout.addWidget(left_frame, stretch=3)
        main_layout.addWidget(right_frame, stretch=1)
        
    def setup_navigation_grid(self, total_questions: int):
        # Clear existing
        for i in reversed(range(self.grid_layout.count())): 
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
        
        self.nav_buttons.clear()
        
        cols = 5
        for i in range(total_questions):
            btn = QPushButton(str(i + 1))
            btn.setProperty("class", "nav_button")
            btn.clicked.connect(lambda checked, idx=i: self.goto_question_signal.emit(idx))
            
            row = i // cols
            col = i % cols
            self.grid_layout.addWidget(btn, row, col)
            self.nav_buttons.append(btn)
            
    def update_score(self, correct: int, total: int):
        self.score_label.setText(f"Kết quả: {correct} / {total} điểm")
        if total > 0 and correct / total >= 0.8:
            self.score_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #48BB78;") # Green for good score
        elif total > 0 and correct / total <= 0.4:
            self.score_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #E53E3E;") # Red for bad score
        else:
            self.score_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2C3E50;") # Default
            
    def display_question(self, index: int, total: int, q):
        self.progress_label.setText(f"Câu hỏi {index + 1} / {total}")
        self.question_text.setText(q.text)
        
        if q.group_instruction:
            self.section_text.setText(q.group_instruction)
            self.section_text.show()
        else:
            self.section_text.hide()
            
        if getattr(q, 'passage_text', None):
            self.passage_text.setText(q.passage_text)
            self.passage_text.show()
        else:
            self.passage_text.hide()
            
        # Clean up existing audio mounts
        for i in reversed(range(self.media_layout.count())): 
            widget = self.media_layout.itemAt(i).widget()
            if widget:
                if hasattr(widget, 'stop_and_release'):
                    widget.stop_and_release()
                widget.setParent(None)
                widget.deleteLater()
                
        # Inject custom player if media exists
        if getattr(q, 'media_url', None):
            from views.components.audio_player import AudioPlayerWidget
            player = AudioPlayerWidget(q.media_url)
            self.media_layout.addWidget(player)
            
        # Explanations
        if q.explanation:
            self.explanation_text.setText(f"**Giải thích:**\n\n{q.explanation}")
            self.explanation_text.setTextFormat(Qt.TextFormat.MarkdownText)
            self.explanation_text.show()
        else:
            self.explanation_text.hide()
        
        # Clear existing options layout
        for i in reversed(range(self.options_layout.count())): 
            widget = self.options_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
            
        if not q.options:
            user_ans = q.user_answer or ""
            is_correct = q.is_correct()
            
            bg_color = "#C6F6D5" if is_correct else "#FED7D7"
            border = "1px solid #48BB78" if is_correct else "1px solid #F56565"
            color = "#22543D" if is_correct else "#742A2A"
            
            text_display = QLineEdit()
            text_display.setReadOnly(True)
            text_display.setText(user_ans if user_ans else "(Không trả lời)")
            text_display.setStyleSheet(f"""
                QLineEdit {{
                    padding: 10px;
                    font-size: 15px;
                    background-color: {bg_color};
                    border: {border};
                    border-radius: 6px;
                    color: {color};
                    font-weight: bold;
                }}
            """)
            self.options_layout.addWidget(text_display)
            
            if not is_correct:
                correct_label = QLabel(f"Đáp án đúng: **{q.correct_answer}**")
                correct_label.setTextFormat(Qt.TextFormat.MarkdownText)
                correct_label.setStyleSheet("color: #48BB78; font-weight: bold; margin-top: 5px; font-size: 15px;")
                self.options_layout.addWidget(correct_label)
                
        else:
            # Add static colored labels for options
            for raw_letter, opt_text in q.options.items():
                # Reconstruct "**A.** Slum" layout for clean visual delivery
                content = f"**{raw_letter}.** {opt_text}"
                
                label = QLabel(content)
                label.setTextFormat(Qt.TextFormat.MarkdownText)
                label.setWordWrap(True)
                
                bg_color = "transparent"
                border = "1px solid #E2E8F0"
                color = "#333333"
                
                if raw_letter == q.correct_answer:
                    bg_color = "#C6F6D5" # Light Green
                    border = "1px solid #48BB78"
                    color = "#22543D"
                elif q.user_answer and raw_letter == q.user_answer and q.user_answer != q.correct_answer:
                    bg_color = "#FED7D7" # Light Red
                    border = "1px solid #F56565"
                    color = "#742A2A"
                    
                label.setStyleSheet(f"""
                    QLabel {{
                        background-color: {bg_color};
                        border: {border};
                        color: {color};
                        padding: 8px;
                        border-radius: 4px;
                        font-size: 15px;
                    }}
                """)
                self.options_layout.addWidget(label)
            
    def update_sidebar_state(self, current_index: int, questions: list):
        for idx, btn in enumerate(self.nav_buttons):
            q = questions[idx]
            
            old_class = btn.property("class")
            new_class = "nav_button"
            
            # Color coding map
            if q.is_correct():
                new_class = "nav_button nav_button_correct"
            else:
                new_class = "nav_button nav_button_incorrect"
                
            if idx == current_index:
                new_class = f"{new_class} nav_button_current"
                
            # Render Optimization
            if old_class != new_class:
                btn.setProperty("class", new_class)
                btn.style().unpolish(btn)
                btn.style().polish(btn)
