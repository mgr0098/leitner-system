from collections import deque
from src.models import Card

class CardImporter():
    def __init__(self, file_name):
        self.file_name = file_name
        self.cards = deque()
        self.import_file()
    
    def import_file(self):
        for vocab in self.file_name:
            card = Card(**vocab, level=0)
            self.cards.appendleft(card)
