from dataclasses import dataclass
import os
from random import shuffle
from collections import deque

class System():
    def __init__(self, review_frequency, vocabulary):
        self.session = SessionCounter()
        self.terminal_viewer = TerminalViewer()
        self.sessionBox = SessionBox()
        self.boxes = []
        
        self.box_count = len(review_frequency)
        self.review_frequency = review_frequency
        self.vocabulary = vocabulary
        
    def __str__(self):
        header = f"System: boxes_count:{self.box_count}\n"
        
        if not self.boxes:
            return header
        
        boxes_string = [str(box) for box in self.boxes]
        
        for box in boxes_string:
            print("string:", box)
        response = header + "\n".join(boxes_string)
        
        return response
    
    def setup(self):
        self.setup_boxes()
        self.session.add_subscribers(self.boxes)
        self.setup_cards()
        
    def setup_boxes(self):
        for i in self.review_frequency:
            box = Box(i)
            self.boxes.append(box)
    
    def setup_cards(self):
        if not self.boxes:
            return KeyError("error, need boxes to place cards in first")
        
        for vocab in self.vocabulary:
            card = Card(vocab["front"], vocab["back"], 0)
            self.boxes[0].add_card(card)
            
    def promote_card(self, card):
        card.level += 1
        
        # destroy card when its been reviewed enough
        if card.level > len(self.boxes):
            return
        
        # move card to next box
        self.boxes[card.level].add_card(card)
    
    def demote_card(self, card):
        if card.level > 1:
            card.level -= 1
        
        self.sessionBox.add_card(card)
    
    def get_session_cards(self):
        for box in self.boxes:
            session_cards = box.load_session_cards(self.session)
            
            self.sessionBox.add_card(session_cards)
    
    def return_cards(self):
        for card in self.sessionBox.cards:
            self.boxes[card.level].add_card(card)
    
    def load_session_box(self):
        for box in self.boxes:
            if box.is_due:
                while box.length > 0:
                    card = box.cards.popleft()
                    self.sessionBox.add_card(card)
        
        self.sessionBox.shuffle()

    def run(self):
        self.session.increment()
        self.load_session_box()
        
        try:
            while self.sessionBox.length > 0:
                card = self.sessionBox.next_card()
                
                response = self.terminal_viewer.get_user_input(card)
                if response is None:    
                    raise KeyboardInterrupt()
                
                # move the card to the next box
                if response is True:
                    self.promote_card(card)
                else:
                    self.demote_card(card)
        except:
            print()
            self.terminal_viewer.display_message("Exiting program ...")
            self.return_cards()
        
        # clear session cards for next session   
        self.sessionBox.clear()
            
class TerminalViewer():
    def __init__(self):
        self.padding = 15
        self.success = "y"
        self.fail = "n"
    
    def display_card(self, card):
        self.clear_screen()
        
        print("=" * self.padding)
        print(f" CARD FRONT: {card.front}")
        print("=" * self.padding)
        input("\nPress [Enter] to see the answer")
        print(f"\n CARD BACK: {card.back}")
        print("=" * self.padding)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_user_input(self, card):
        self.display_card(card)
        try:
            user_input = input("Did you get it right? (y/n)")
            
            if user_input is self.success:
                return True
            elif user_input is self.fail:
                return False
        except KeyboardInterrupt:
            return None
        
        return None
        

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


class Box():
    def __init__(self, level):
        self.count = 0
        self.level = level
        self.cards = deque()
    
    @property
    def length(self):
        return len(self.cards)
    
    @property
    def is_due(self):
        if self.count % self.level == 0:
            return True

        return False

    def increment_count(self):
        self.count +=1
    
    def add_card(self, card):
        self.cards.append(card)
    
    def next_card(self):
        if not self.cards:
            return KeyError
        
        return self.cards.popleft()
    
    def __str__(self) -> str:
        header = f"Box {self.level}: cards_count: {len(self.cards)}"
        
        if not self.cards:
            return header
        
        cards_string = [str(card) for card in self.cards]
        response = header +"\n".join(cards_string)
        
        return response


class SessionBox(Box):
    def __init__(self):
        super().__init__(0)
    
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
      
        
def main():
    vocabulary = [{"front":"ciao", "back":"hallo"}, {"front":"halla balla", "back": "camma fa fra"}]
    
    review_frequency = [1, 3, 7]
    system = System(review_frequency, vocabulary)
    system.setup()
    system.run()

if __name__ == "__main__":
    main()
    