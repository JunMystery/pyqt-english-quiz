from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QRadioButton, QPushButton, QGridLayout, QScrollArea, QFrame,
    QSizePolicy, QButtonGroup, QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal

class QuizView(QWidget):
    # Signals
    next_question_signal = pyqtSignal()
    prev_question_signal = pyqtSignal()
    goto_question_signal = pyqtSignal(int)
    submit_quiz_signal = pyqtSignal()
    answer_selected_signal = pyqtSignal(str) # Emits selected option text
    
    def __init__(self):
        super().__init__()
        self.nav_buttons = []
        self.option_buttons = QButtonGroup(self)
        self.option_buttons.buttonClicked.connect(self.on_option_clicked)
        self.init_ui()
        
    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Left Side: Quiz Content Area
        left_layout = QVBoxLayout()
        left_frame = QFrame()
        left_frame.setObjectName("card")
        left_frame.setLayout(left_layout)
        
        # Top Header (Timer and Question progress)
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 10)
        
        top_row = QHBoxLayout()
        self.section_text = QLabel("")
        self.section_text.setWordWrap(True)
        self.section_text.setStyleSheet("font-size: 17px; font-weight: bold; font-style: italic; color: #2D3748;")
        self.section_text.hide()
        
        self.timer_label = QLabel("Thời gian: 15:00")
        self.timer_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #E53E3E;")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        top_row.addWidget(self.section_text, stretch=1)
        top_row.addWidget(self.timer_label)
        
        self.progress_label = QLabel("Câu hỏi 1 / 10")
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
        
        # Passage Text (For Reading sections)
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
        left_layout.addLayout(self.options_layout)
        
        left_layout.addStretch()
        
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
        
        self.submit_btn = QPushButton("Nộp Bài")
        self.submit_btn.setStyleSheet("background-color: #E53E3E;") # Red submit button
        self.submit_btn.clicked.connect(lambda: self.submit_quiz_signal.emit())
        right_layout.addWidget(self.submit_btn)
        
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
            
    def display_question(self, index: int, total: int, text: str, options: dict, selected_ans: str = None, group_instruction: str = "", passage: str = "", media_url: str = None):
        self.progress_label.setText(f"Câu hỏi {index + 1} / {total}")
        self.question_text.setText(text)
        
        if group_instruction:
            self.section_text.setText(group_instruction)
            self.section_text.show()
        else:
            self.section_text.hide()
            
        if passage:
            self.passage_text.setText(passage)
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
        if media_url:
            from views.components.audio_player import AudioPlayerWidget
            player = AudioPlayerWidget(media_url)
            self.media_layout.addWidget(player)
            
        for button in self.option_buttons.buttons():
            self.option_buttons.removeButton(button)
            
        for i in reversed(range(self.options_layout.count())): 
            widget = self.options_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
            
        if not options:
            self.text_input = QLineEdit()
            self.text_input.setPlaceholderText("Nhập câu trả lời của bạn vào đây...")
            self.text_input.setStyleSheet("""
                QLineEdit {
                    padding: 10px;
                    font-size: 15px;
                    background-color: white;
                    border: 2px solid #CBD5E0;
                    border-radius: 6px;
                    color: #2D3748;
                }
                QLineEdit:focus {
                    border: 2px solid #4C51BF;
                }
            """)
            if selected_ans:
                self.text_input.setText(selected_ans)
            
            def on_text_changed(text):
                self.answer_selected_signal.emit(text.strip())
                
            self.text_input.textChanged.connect(on_text_changed)
            self.options_layout.addWidget(self.text_input)
            
        else:
            # Add new options (Iterating dictionary keys A, B, C, D)
            for raw_letter, opt_text in options.items():
                opt_container = QWidget()
                opt_container.setCursor(Qt.CursorShape.PointingHandCursor)
                
                opt_layout = QHBoxLayout(opt_container)
                opt_layout.setContentsMargins(5, 5, 5, 5)
    
                rb = QRadioButton()
                rb.setProperty("letter", raw_letter)
                
                # Reconstruct legacy visual pattern "**A.** Slum" for rendering
                lbl = QLabel(f"**{raw_letter}.** {opt_text}")
                lbl.setTextFormat(Qt.TextFormat.MarkdownText)
                lbl.setWordWrap(True)
                lbl.setStyleSheet("font-size: 15px; background: transparent; margin: 0; padding: 0;")
                lbl.setCursor(Qt.CursorShape.PointingHandCursor)
                
                opt_layout.addWidget(rb)
                opt_layout.addWidget(lbl, stretch=1)
                
                self.option_buttons.addButton(rb)
                self.options_layout.addWidget(opt_container)
                
                if selected_ans and selected_ans == raw_letter:
                    rb.setChecked(True)
                    
                def make_handler(radio_btn):
                    def handler(event):
                        radio_btn.setChecked(True)
                        self.on_option_clicked(radio_btn)
                    return handler
                    
                opt_container.mousePressEvent = make_handler(rb)
                lbl.mousePressEvent = make_handler(rb)
                
    def on_option_clicked(self, button):
        letter = button.property("letter")
        if letter:
            self.answer_selected_signal.emit(letter)
            
    def update_sidebar_state(self, current_index: int, answered_indices: list[int]):
        for idx, btn in enumerate(self.nav_buttons):
            old_class = btn.property("class")
            new_class = "nav_button"
            
            if idx in answered_indices:
                new_class = "nav_button nav_button_answered"
                
            if idx == current_index:
                new_class = f"{new_class} nav_button_current"
                
            # Render Optimization: Only Repaint if the style logic implies a diff
            if old_class != new_class:
                btn.setProperty("class", new_class)
                btn.style().unpolish(btn)
                btn.style().polish(btn)

    def update_timer(self, time_str: str):
        self.timer_label.setText(f"Thời gian: {time_str}")
