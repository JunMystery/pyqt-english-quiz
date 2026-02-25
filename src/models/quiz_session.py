from typing import List
from datetime import datetime
from models.question_model import Question

class QuizSession:
    def __init__(self, questions: List[Question], time_limit_minutes: int = 0, difficulty: str = "Tự do", quiz_id: str = "Custom"):
        self.questions = questions
        self.time_limit_minutes = time_limit_minutes
        self.current_index = 0
        self.is_submitted = False
        
        # History metadata
        self.difficulty = difficulty
        self.quiz_id = quiz_id
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def get_current_question(self) -> Question:
        if 0 <= self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None
        
    def next_question(self) -> bool:
        if self.current_index < len(self.questions) - 1:
            self.current_index += 1
            return True
        return False
        
    def prev_question(self) -> bool:
        if self.current_index > 0:
            self.current_index -= 1
            return True
        return False
        
    def set_answer(self, answer: str):
        q = self.get_current_question()
        if q and not self.is_submitted:
            q.user_answer = answer
            
    def get_score(self) -> int:
        return sum(1 for q in self.questions if q.is_correct())
        
    def submit(self):
        self.is_submitted = True
        
    def reset(self):
        self.current_index = 0
        self.is_submitted = False
        for q in self.questions:
            q.user_answer = None

    def to_dict(self) -> dict:
        return {
            "questions": [q.to_dict() for q in self.questions],
            "time_limit_minutes": self.time_limit_minutes,
            "difficulty": self.difficulty,
            "quiz_id": self.quiz_id,
            "timestamp": self.timestamp,
        }
        
    @classmethod
    def from_dict(cls, data: dict):
        questions = [Question.from_dict(q_data) for q_data in data.get("questions", [])]
        session = cls(
            questions=questions, 
            time_limit_minutes=data.get("time_limit_minutes", 0),
            difficulty=data.get("difficulty", "Tự do"),
            quiz_id=data.get("quiz_id", "Custom")
        )
        session.timestamp = data.get("timestamp", session.timestamp)
        # Note: If loaded from history it's usually already submitted, but we reset state for "Xem lại"
        # The history manager might just load it. 
        # Actually user_answers are restored by Question.from_dict, so we want it to stay submitted
        session.is_submitted = True
        return session
