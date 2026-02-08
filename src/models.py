from dataclasses import dataclass
from collections import deque

class Box():
    def __init__(self, frequency, name):
        self.name = name
        self.frequency = frequency
        self.count = 0
        self.cards = deque()
    
    @property
    def length(self):
        return len(self.cards)
    
    @property
    def is_due(self):
        if self.count % self.frequency == 0:
            return True

        return False

    def increment_count(self):
        self.count +=1
    
    def add_card(self, card):
        self.cards.append(card)
    
    def next_card(self):
        if not self.cards:
            return IndexError("Empty box")
        
        return self.cards.popleft()
    
    def __str__(self) -> str:
        header = f"Box {self.frequency}: cards_count: {len(self.cards)}"
        
        if not self.cards:
            return header
        
        cards_string = [str(card) for card in self.cards]
        response = header +"\n".join(cards_string)
        
        return response


class SessionBox(Box):
    def __init__(self):
        super().__init__(0, "session_box")
    
    # add shuffling
    def add_card(self, card):
        super().add_card(card)
        return
    
    def clear(self):
        self.cards.clear()
    
    def shuffle(self):
        shuffle(self.cards)
        

@dataclass
class Card():
    front: str
    back: str
    level: int
    
    def __str__(self) -> str:
        return f"Card: {self.front}, {self.back}, lvl {self.level}"

class SessionCounter():
    def __init__(self):
        self.count = 0
        self.subscribers = []
    
    def add_subscribers(self, subscribers):
        for subscriber in subscribers:
            self.subscribers.append(subscriber)
    
    def increment(self):
        self.count += 1
        for subscriber in self.subscribers:
            subscriber.increment_count()
