from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame, QGridLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from models.quiz_session import QuizSession

class HistoryView(QWidget):
    back_signal = pyqtSignal()
    view_history_signal = pyqtSignal(QuizSession)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        self.btn_back = QPushButton("⬅ Quay lại")
        self.btn_back.setProperty("class", "secondary")
        self.btn_back.clicked.connect(lambda: self.back_signal.emit())
        header_layout.addWidget(self.btn_back)
        
        header = QLabel("Lịch sử làm bài (10 lần gần nhất)")
        header.setObjectName("headerTitle")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(header, stretch=1)
        
        # Spacer to balance the header since the back button is on the left
        spacer = QWidget()
        spacer.setFixedWidth(self.btn_back.sizeHint().width())
        header_layout.addWidget(spacer)
        
        main_layout.addLayout(header_layout)
        
        # Scroll Area for history cards
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        self.content_widget = QWidget()
        self.content_widget.setObjectName("q_container")
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.content_layout.setSpacing(15)
        
        self.scroll_area.setWidget(self.content_widget)
        main_layout.addWidget(self.scroll_area)
        
    def populate(self, history: list[QuizSession]):
        # Clear existing
        for i in reversed(range(self.content_layout.count())): 
            item = self.content_layout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                
        if not history:
            empty_label = QLabel("Chưa có lịch sử làm bài nào.")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet("color: #718096; font-size: 16px; margin-top: 50px;")
            self.content_layout.addWidget(empty_label)
            return
            
        for session in history:
            card = QFrame()
            card.setObjectName("card")
            card_layout = QHBoxLayout(card)
            
            # Info side
            info_layout = QVBoxLayout()
            title = QLabel(f"Đề: {session.quiz_id} (Độ khó: {session.difficulty})")
            title.setStyleSheet("font-weight: bold; font-size: 16px;")
            
            score = session.get_score()
            total = len(session.questions)
            score_lbl = QLabel(f"Điểm: {score}/{total}")
            score_lbl.setStyleSheet("color: #E53E3E; font-weight: bold;")
            
            time_lbl = QLabel(f"Thời gian làm: {session.timestamp}")
            time_lbl.setStyleSheet("color: #718096; font-size: 13px;")
            
            info_layout.addWidget(title)
            info_layout.addWidget(score_lbl)
            info_layout.addWidget(time_lbl)
            
            # Action side
            btn_view = QPushButton("Xem Lại")
            # Bind the specific session using default argument in lambda
            btn_view.clicked.connect(lambda checked, s=session: self.view_history_signal.emit(s))
            btn_view.setFixedWidth(120)
            
            card_layout.addLayout(info_layout)
            card_layout.addStretch()
            card_layout.addWidget(btn_view)
            
            self.content_layout.addWidget(card)
