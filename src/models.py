from dataclasses import dataclass
from collections import deque

"""Box holds the cards and tracks whether its due for a session"""
class Box():
    def __init__(self, level, name):
        self.name = name
        self.level = level
        self.count = 0
        
        # O(1) when popping cards from front
        # instead of O(N) with python list
        # useful for retrieving the first card of the list
        self.cards = deque() 
    
    @property
    def length(self):
        return len(self.cards)
    
    @property
    def is_due(self):
        if self.count % self.level == 0:
            return True

        return False

    def increment_session_count(self):
        self.count +=1
    
    def add_card(self, card):
        self.cards.append(card)
    
    def next_card(self):
        if not self.cards:
            return IndexError("Empty box")
        
        return self.cards.popleft()
    
    """Pretty printer for debugging, retrieves cards in box aswell"""
    def __str__(self) -> str:
        header = f"Box {self.level}: cards_count: {len(self.cards)}"
        
        if not self.cards:
            return header
        
        cards_string = [str(card) for card in self.cards]
        response = header +"\n".join(cards_string)
        
        return response

"""Holds the cards in the current session"""
class SessionBox(Box):
    def __init__(self):
        super().__init__(0, "session_box")
    
    def add_card(self, card):
        super().add_card(card)
        return
    
    def clear(self):
        self.cards.clear()
        
    def shuffle(self):
        pass

"""Holds card information"""
@dataclass
class Card():
    front: str
    back: str
    level: int
    
    """Pretty printer for the card"""
    def __str__(self) -> str:
        return f"Card: {self.front}, {self.back}, lvl {self.level}"

"""Keeps track of the session number"""
class SessionCounter():
    def __init__(self):
        self.count = 0
        self.subscribers = []
    
    def add_subscribers(self, subscribers):
        for subscriber in subscribers:
            self.subscribers.append(subscriber)
    
    """Tell the subscribers to increase the count"""
    def increment(self):
        self.count += 1
        for subscriber in self.subscribers:
            subscriber.increment_session_count()
