from PyQt6.QtCore import QTimer
from models.quiz_session import QuizSession

class QuizController:
    def __init__(self, quiz_view, session: QuizSession, main_controller):
        self.view = quiz_view
        self.session = session
        self.main_controller = main_controller
        
        # Setup Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.time_left_seconds = session.time_limit_minutes * 60
        
        # Connect View Signals
        self.view.next_question_signal.connect(self.go_next)
        self.view.prev_question_signal.connect(self.go_prev)
        self.view.goto_question_signal.connect(self.go_to)
        self.view.answer_selected_signal.connect(self.handle_answer)
        self.view.submit_quiz_signal.connect(self.submit)
        
    def start(self):
        """Initializes the quiz UI and starts the timer."""
        # Setup Grid
        total_q = len(self.session.questions)
        self.view.setup_navigation_grid(total_q)
        
        # Show first question
        self.refresh_view()
        
        # Start Timer if time limit > 0
        if self.time_left_seconds > 0:
            self.update_timer_display()
            self.timer.start(1000) # Tick every 1 second
        else:
            self.view.update_timer("Không giới hạn\n")
            
    def update_timer(self):
        if self.time_left_seconds <= 0:
            self.timer.stop()
            self.submit(auto=True)
            return
            
        self.time_left_seconds -= 1
        self.update_timer_display()
        
    def update_timer_display(self):
        mins = self.time_left_seconds // 60
        secs = self.time_left_seconds % 60
        self.view.update_timer(f"{mins:02d}:{secs:02d}")
        
    def go_next(self):
        if self.session.next_question():
            self.refresh_view()
            
    def go_prev(self):
        if self.session.prev_question():
            self.refresh_view()
            
    def go_to(self, index: int):
        if 0 <= index < len(self.session.questions):
            self.session.current_index = index
            self.refresh_view()
            
    def handle_answer(self, letter: str):
        # Save the answer to session model
        self.session.set_answer(letter)
        # Refresh sidebar colors
        self.update_sidebar()
        
    def refresh_view(self):
        q = self.session.get_current_question()
        if q:
            self.view.display_question(
                index=self.session.current_index,
                total=len(self.session.questions),
                text=q.text,
                options=q.options,
                selected_ans=q.user_answer,
                group_instruction=q.group_instruction,
                passage=q.passage_text,
                media_url=getattr(q, 'media_url', None)
            )
            
            # Update buttons state
            self.view.prev_btn.setEnabled(self.session.current_index > 0)
            self.view.next_btn.setEnabled(self.session.current_index < len(self.session.questions) - 1)
            
            self.update_sidebar()
            
    def update_sidebar(self):
        # Find which questions have been answered
        answered = [i for i, q in enumerate(self.session.questions) if q.user_answer is not None]
        self.view.update_sidebar_state(self.session.current_index, answered)
        
    def submit(self, auto=False):
        # Note: If not auto, we could show a confirmation dialog here
        from PyQt6.QtWidgets import QMessageBox
        
        if not auto:
            reply = QMessageBox.question(
                self.view, 'Xác nhận nộp bài', 
                "Bạn có chắc chắn muốn nộp bài?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
                
        self.timer.stop()
        self.session.submit()
        
        from models.history_manager import HistoryManager
        HistoryManager.save_session(self.session)
        
        self.main_controller.show_results(self.session)
