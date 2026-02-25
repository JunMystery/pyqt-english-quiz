import sys
from PyQt6.QtWidgets import QApplication

from views.main_window import MainWindow
from views.home_view import HomeView
from views.setup_available_view import SetupAvailableView
from views.history_view import HistoryView
from views.quiz_view import QuizView
from views.result_view import ResultView

from controllers.home_controller import HomeController
from controllers.setup_controller import SetupController
from controllers.quiz_controller import QuizController
from controllers.result_controller import ResultController

from models.quiz_session import QuizSession
from styles.loader import load_theme

class MainController:
    """Orchestrates the flow between Home -> Setup -> Quiz -> Result screens."""
    
    def __init__(self, main_window: MainWindow):
        self.main_window = main_window
        
        # Instantiate Views
        self.home_view = HomeView()
        self.setup_available_view = SetupAvailableView()
        self.history_view = HistoryView()
        self.quiz_view = QuizView()
        self.result_view = ResultView()
        
        # Add to stack and map indices
        self.home_idx = self.main_window.add_view(self.home_view)
        self.setup_available_idx = self.main_window.add_view(self.setup_available_view)
        self.history_idx = self.main_window.add_view(self.history_view)
        self.quiz_idx = self.main_window.add_view(self.quiz_view)
        self.result_idx = self.main_window.add_view(self.result_view)
        
        # Initialize Controllers
        self.home_controller = HomeController(self.home_view, self)
        self.setup_controller = SetupController(self.setup_available_view, self)
        self.quiz_controller = None
        self.result_controller = None
        
        # Start at home
        self.show_home()
        
    def _cleanup_old_quiz(self):
        if self.quiz_controller and self.quiz_controller.timer:
            self.quiz_controller.timer.stop()

    def show_home(self):
        """Switches to Home View."""
        self._cleanup_old_quiz()
        self.main_window.show_view(self.home_idx)

    def show_available_setup(self):
        """Switches to Setup Available View."""
        from utils.file_scanner import scan_available_quizzes
        quizzes = scan_available_quizzes()
        self.setup_available_view.populate(quizzes)
        self.main_window.show_view(self.setup_available_idx)
        
    def show_history(self):
        """Switches to History View."""
        from models.history_manager import HistoryManager
        history_list = HistoryManager.load_history()
        self.history_view.populate(history_list)
        # Only connected here to inject self without breaking structure
        try:
            self.history_view.view_history_signal.disconnect()
        except TypeError:
            pass
        self.history_view.view_history_signal.connect(self.show_results)
        self.history_view.back_signal.connect(self.show_home)
        self.main_window.show_view(self.history_idx)
        
    def start_quiz(self, session: QuizSession):
        """Switches to Quiz View and starts the session."""
        self._cleanup_old_quiz()
        self.quiz_controller = QuizController(self.quiz_view, session, self)
        self.quiz_controller.start()
        self.main_window.show_view(self.quiz_idx)
        
    def show_results(self, session: QuizSession):
        """Switches to Results View and displays scores."""
        self._cleanup_old_quiz()
        self.result_controller = ResultController(self.result_view, session, self)
        self.result_controller.start()
        self.main_window.show_view(self.result_idx)


def main():
    app = QApplication(sys.argv)
    
    # Load Global QSS Theme
    load_theme(app)
    
    main_window = MainWindow()
    controller = MainController(main_window)
    
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
