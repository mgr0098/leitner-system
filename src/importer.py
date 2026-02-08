import json
import os
from collections import deque
from src.models import Card
from src.errors import ImportError

"""Imports cards from a filepath"""
class CardImporter():
    def __init__(self, file_path):
        self.file_path = file_path
        self.cards = deque()
        self.import_json_file()
    
    """Adds Card(s) to the queue from a json file """
    def import_json_file(self):
        if not os.path.exists(self.file_path):
            raise ImportError(f"Cannot Find Filepath {self.file_path}")
        
        try:
            # read json string from the file path
            with open(self.file_path) as f:
                string = f.read()
            
            # deserialize json string into python object
            vocabulary_list = json.loads(string)
            
            # create cards from the object and add to the queue
            for vocabulary in vocabulary_list:
                card = Card(**vocabulary, level=0)
                self.cards.appendleft(card)
        
        except json.JSONDecodeError as e:
            raise ImportError(f"Error: {e} while importing cards")
            
