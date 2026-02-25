import os
import re
from typing import Dict, List

def scan_available_quizzes(data_dir: str = "data/quizzes") -> Dict[str, List[str]]:
    """
    Scans the data directory for folders matching the pattern XX-YYY
    XX: Difficulty Level (e.g., 01)
    YYY: Quiz ID/Number (e.g., 001)
    Inside the folder, it expects a `data.json` file.
    
    Returns a dictionary mapping difficulty to a list of available Quiz IDs.
    Format:
    {
        "01": ["001", "002"],
        "12": ["002"]
    }
    """
    available_quizzes = {}
    
    if not os.path.exists(data_dir):
        return available_quizzes
        
    pattern_folder = re.compile(r'^(\d{2})-(\d{3})$', re.IGNORECASE)
    
    for item in os.listdir(data_dir):
        item_path = os.path.join(data_dir, item)
        if os.path.isdir(item_path):
            match = pattern_folder.match(item)
            if match:
                difficulty = match.group(1)
                quiz_id = match.group(2)
                
                # Check if data.json exists in this folder
                data_json_path = os.path.join(item_path, "data.json")
                if os.path.exists(data_json_path):
                    if difficulty not in available_quizzes:
                        available_quizzes[difficulty] = []
                    if quiz_id not in available_quizzes[difficulty]:
                        available_quizzes[difficulty].append(quiz_id)
                        
    # Sort for consistent display
    for diff in available_quizzes:
        available_quizzes[diff] = sorted(available_quizzes[diff])
        
    return dict(sorted(available_quizzes.items()))
