import json
import os
from typing import List
from models.quiz_session import QuizSession

HISTORY_FILE = "data/history.json"
MAX_HISTORY_ITEMS = 10

class HistoryManager:
    @staticmethod
    def load_history() -> List[QuizSession]:
        if not os.path.exists(HISTORY_FILE):
            return []
            
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [QuizSession.from_dict(item) for item in data]
        except Exception as e:
            print(f"Failed to load history: {e}")
            return []
            
    @staticmethod
    def save_session(session: QuizSession):
        history = HistoryManager.load_history()
        
        # Add new session to the front
        history.insert(0, session)
        
        # Keep only the latest MAX_HISTORY_ITEMS
        history = history[:MAX_HISTORY_ITEMS]
        
        # Save to file
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        try:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump([h.to_dict() for h in history], f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Failed to save history: {e}")
