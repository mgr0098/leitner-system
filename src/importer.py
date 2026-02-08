import json
import os
from collections import deque
from src.models import Card
from src.errors import ImportError

class CardImporter():
    def __init__(self, file_path):
        self.file_path = file_path
        self.cards = deque()
        self.import_json_file()
    
    def import_json_file(self):
        if not os.path.exists(self.file_path):
            raise ImportError(f"Cannot Find Filepath {self.file_path}")
        
        try:
            with open(self.file_path) as f:
                string = f.read()
            
            vocabulary_list = json.loads(string)
            
            for vocabulary in vocabulary_list:
                card = Card(**vocabulary, level=0)
                self.cards.appendleft(card)
                
        except json.JSONDecodeError as e:
            raise ImportError(f"Error: {e} while importing cards")
            
