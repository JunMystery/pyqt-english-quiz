from models.quiz_session import QuizSession

class ResultController:
    def __init__(self, result_view, session: QuizSession, main_controller):
        self.view = result_view
        self.session = session
        self.main_controller = main_controller
        
        # Disconnect any previously connected signals to prevent multiple triggers
        try:
            self.view.restart_signal.disconnect()
            self.view.retry_signal.disconnect()
            self.view.next_question_signal.disconnect()
            self.view.prev_question_signal.disconnect()
            self.view.goto_question_signal.disconnect()
        except TypeError:
            pass # No connections yet
            
        # Connect Signals
        self.view.restart_signal.connect(self.restart)
        self.view.retry_signal.connect(self.retry)
        self.view.next_question_signal.connect(self.go_next)
        self.view.prev_question_signal.connect(self.go_prev)
        self.view.goto_question_signal.connect(self.go_to)
        
    def start(self):
        """Prepares results logic and displays them."""
        # Initialize Navigation Grid
        self.view.setup_navigation_grid(len(self.session.questions))
        
        score = self.session.get_score()
        total = len(self.session.questions)
        self.view.update_score(score, total)
        
        # Reset current index to 0 to review from the start
        self.session.current_index = 0
        self.refresh_view()
        
    def refresh_view(self):
        q = self.session.get_current_question()
        if q:
            self.view.display_question(
                index=self.session.current_index,
                total=len(self.session.questions),
                q=q
            )
            
            # Update buttons state
            self.view.prev_btn.setEnabled(self.session.current_index > 0)
            self.view.next_btn.setEnabled(self.session.current_index < len(self.session.questions) - 1)
            
            self.view.update_sidebar_state(self.session.current_index, self.session.questions)
            
    def go_next(self):
        if self.session.current_index < len(self.session.questions) - 1:
            self.session.current_index += 1
            self.refresh_view()
            
    def go_prev(self):
        if self.session.current_index > 0:
            self.session.current_index -= 1
            self.refresh_view()
            
    def go_to(self, index: int):
        if 0 <= index < len(self.session.questions):
            self.session.current_index = index
            self.refresh_view()
        
    def restart(self):
        self.main_controller.show_home()
        
    def retry(self):
        # Resets the current questions and moves back to quiz view
        self.session.reset()
        self.main_controller.start_quiz(self.session)
