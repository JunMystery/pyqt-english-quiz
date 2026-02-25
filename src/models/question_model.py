import re

class Question:
    def __init__(self, q_id: str, text: str, options: dict, correct_answer: str = "", explanation: str = "", group_instruction: str = "", passage_id: str = None):
        self.q_id = str(q_id)
        self.text = text
        self.options = options or {}
        self.correct_answer = correct_answer
        self.explanation = explanation
        self.user_answer = None
        self.group_instruction = group_instruction
        self.passage_id = passage_id
        
        # Passage injection runtime
        self.passage_text = None
        self.passage_type = None
        self.media_url = None

    def is_correct(self) -> bool:
        """Check if the user's answer matches the correct answer using normalization."""
        if not self.correct_answer or not self.user_answer:
            return False
            
        def normalize(text: str) -> str:
            # Uppercase
            t = text.upper()
            # Remove trailing period if present
            t = t.rstrip('.')
            # Compress multiple spaces into a single space
            t = re.sub(r'\s+', ' ', t)
            return t.strip()
            
        return normalize(self.user_answer) == normalize(self.correct_answer)

    def to_dict(self) -> dict:
        return {
            "id": self.q_id,
            "question": self.text,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "explanation": self.explanation,
            "user_answer": self.user_answer,
            "group_instruction": self.group_instruction,
            "passage_id": self.passage_id,
            "passage_text": self.passage_text,
            "passage_type": self.passage_type,
            "media_url": self.media_url
        }
        
    @classmethod
    def from_dict(cls, data: dict):
        q = cls(
            q_id=data.get("id", ""),
            text=data.get("question", ""),
            options=data.get("options") or {},
            correct_answer=data.get("correct_answer", ""),
            explanation=data.get("explanation", ""),
            group_instruction=data.get("group_instruction", ""),
            passage_id=data.get("passage_id")
        )
        # Restore fields
        q.user_answer = data.get("user_answer")
        q.passage_text = data.get("passage_text")
        q.passage_type = data.get("passage_type")
        q.media_url = data.get("media_url")
        return q

    def __repr__(self):
        return f"<Question '{self.text[:20]}...' Correct: {self.correct_answer}>"
