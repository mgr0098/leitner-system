from src.models import Box, SessionBox
from src.errors import CardSystemError

"""Manages the leitner system state"""
class System():
    def __init__(self, deck, box_config, session_counter, terminal_viewer):
        self.session = session_counter
        self.terminal_viewer = terminal_viewer
        self.box_config = box_config
        self.deck = deck
        
        self.boxes = [] # use list to get O(1) lookup instead of queue
        self.session_box = SessionBox()
        self.setup()
        
    """Pretty printer for easier debugging"""
    def __str__(self):
        header = f"System: boxes_count:{len(self.boxes)}\n"
        
        if not self.boxes:
            return header

        body = "\n".join(str(box) for box in self.boxes)
        
        return f"{header}\n{body}"
    
    """Setup the boxes, and put cards into the first box """
    def setup(self):
        self.setup_boxes()
        self.session.add_subscribers(self.boxes)
        self.setup_cards()
    
    """Setup the boxes based on box config"""
    def setup_boxes(self):
        if not len(self.box_config) > 0:
           raise CardSystemError("Unable to setup boxes, Box config is empty") 
        
        for i in self.box_config:
            box = Box(**i)
            self.boxes.append(box)
    
    """Insert the cards into the first box"""
    def setup_cards(self):
        if not self.boxes:
            raise CardSystemError("No boxes to put cards in")
        
        self.transfer_cards(self.deck, self.boxes[0])
    
    """Promotes card to the next box"""
    def promote_card(self, card):
        
        card.level += 1
        # destroy card when its been reviewed enough
        if card.level > len(self.boxes) - 1:
            return
        
        # move card to next box
        self.boxes[card.level].add_card(card)
    
    """Demote the card to the first box, and return it to the session"""
    def demote_card(self, card):
        card.level = 0
        self.session_box.add_card(card)
    
    """Retrieves all the session cards from due boxes"""
    def get_session_cards(self):
        for box in self.boxes:
            session_cards = box.load_session_cards(self.session)
        
            self.session_box.add_card(session_cards)
    
    """Returns the cards back into the boxes they belong"""
    def return_cards(self):
        for card in self.session_box.cards:
            self.boxes[card.level].add_card(card)
    
    """Transfer cards from source to target box"""
    def transfer_cards(self, source, target):
        while len(source) > 0:
            card = source.popleft()
            target.add_card(card)
    
    """Retrieves cards from due boxes"""
    def load_session_box(self):
        for box in self.boxes:
            if box.is_due:
                self.transfer_cards(box.cards, self.session_box)

    """Runs the session, retrieves session card"""
    def run_session(self):
        
        self.session.increment()
        self.load_session_box()
        
        if not self.session_box.length > 0:
            raise CardSystemError("No cards in deck")
        
        try:
            while self.session_box.length > 0:
                card = self.session_box.next_card()
                
                response = self.terminal_viewer.get_user_input(card)
                if response is None:    
                    raise KeyboardInterrupt()
                
                # move the card to the next box
                if response is True:
                    self.promote_card(card)
                else:
                    # put it back into the session and demote it to first box
                    self.demote_card(card)
        except KeyboardInterrupt:
            # returns the cards back into the corresponding box
            self.terminal_viewer.display_message("Exiting program ...")
            self.return_cards()
        finally:
            # in case there is another error
            if self.session_box.length > 0:
                self.return_cards()
            
            # clear session cards for next session   
            self.session_box.clear()
