import os
import json
from PyQt6.QtWidgets import QMessageBox
from models.question_model import Question
from models.quiz_session import QuizSession

class SetupController:
    """Handles Setup views for JSON-driven quiz payload"""
    def __init__(self, setup_available_view, main_controller):
        self.available_view = setup_available_view
        self.main_controller = main_controller
        
        # Connect Available View Signals
        self.available_view.start_signal.connect(self.handle_available_quiz)
        self.available_view.back_signal.connect(self.main_controller.show_home)

    def handle_available_quiz(self, difficulty: str, quiz_id: str, time_limit: int):
        try:
            # Construct the path to the folder
            quiz_folder = os.path.join("data", "quizzes", f"{difficulty}-{quiz_id}")
            data_file = os.path.join(quiz_folder, "data.json")
            
            if not os.path.exists(data_file):
                raise ValueError(f"Không tìm thấy file dữ liệu `data.json` cho đề thi {difficulty}-{quiz_id}.")
                
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Build passage map
            passage_map = {}
            for p in data.get("passages", []):
                p_media = p.get("media_url")
                if p_media:
                    p["media_url"] = os.path.join(quiz_folder, p_media)
                passage_map[p.get("id")] = p
                
            # Render questions
            questions = []
            for q_data in data.get("questions", []):
                q = Question.from_dict(q_data)
                
                # Hydrate passage into the dynamic Question model at runtime
                if q.passage_id and q.passage_id in passage_map:
                    p = passage_map[q.passage_id]
                    q.passage_text = p.get("content")
                    q.passage_type = p.get("type")
                    q.media_url = p.get("media_url")
                    
                questions.append(q)
            
            if not questions:
                 raise ValueError("Không thể trích xuất câu hỏi nào từ file JSON này. Vui lòng kiểm tra cấu trúc file.")

            session = QuizSession(questions, time_limit, difficulty=difficulty, quiz_id=quiz_id)
            self.main_controller.start_quiz(session)
            
        except Exception as e:
            self._show_error(self.available_view, e)

    def _show_error(self, parent_widget, exception):
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.critical(parent_widget, "Lỗi Phân Tích", f"Đã xảy ra lỗi:\n{str(exception)}")
