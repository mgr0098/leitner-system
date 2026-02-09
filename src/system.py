from src.models import Box, SessionBox, Card
from src.errors import CardSystemError

"""Manages the leitner system state"""
class System():
    def __init__(self, box_config, session_counter, terminal_viewer, storage_manager):
        self.session_counter = session_counter
        self.terminal_viewer = terminal_viewer
        self.box_config = box_config
        self.storage_manager = storage_manager        
        self.boxes = [] # use list to get O(1) lookup instead of queue
        self.session_box = SessionBox()
        self.setup()
        
    """restores the state of the system"""
    def save_session(self):
        
        session_data = {
            "current_session": self.session_counter.count,
            "cards": self.storage_manager.serialize_boxes(self.boxes)
        }
        
        self.storage_manager.write_to_json(session_data)
        
    """reads from disk and sets the system into the state"""
    def load_session(self):
        
        data = self.storage_manager.import_json_file()
        
        # set to current session
        self.session_counter.count = data.get("current_session")
        cards = data.get("cards")
        
        for box in self.boxes:
            box.clear()
        
        for card in cards:
            new_card = Card(**card)
            idx = int(new_card.level)
            self.boxes[idx].add_card(new_card)
        
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
        self.session_counter.add_subscribers(self.boxes)
        self.load_session()
    
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
        
        next_level = card.level + 1
        
        # destroy card when its been reviewed enough
        if next_level >= len(self.boxes):
            return
        
        card.level = next_level
        
        # move card to next box
        self.boxes[next_level].add_card(card)
    
    """Demote the card to the first box, and return it to the session"""
    def demote_card(self, card):
        card.level = 0
        self.boxes[0].add_card(card)
    
    """Returns the cards back into the boxes they belong"""
    def return_cards(self):
        for card in self.session_box.cards:
            self.boxes[int(card.level)].add_card(card)
    
    """Transfer cards from source to target box"""
    def transfer_cards(self, source, target):
        while len(source) > 0:
            card = source.popleft()
            target.add_card(card)
    
    """Retrieves cards from due boxes"""
    def load_session_box(self):
        for idx, box in enumerate(self.boxes):
            
            # get the current interval, bad name: should probs be called interval
            level = self.box_config[idx]["level"]
            
            if self.session_counter.count % level == 0:
                self.transfer_cards(box.cards, self.session_box)

    """Runs the session, retrieves session card"""
    def run_session(self):
        
        self.session_counter.increment()
        self.load_session_box()
        
        self.terminal_viewer.display_message(f"Session Number: {self.session_counter.count}")
        
        # just increasing it so that you can eventually start a session
        if not self.session_box.length > 0:
            self.save_session()
            self.terminal_viewer.display_message("No cards to review, session Saved...")
            return
        
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
        finally:
            # in case there is another error
            if self.session_box.length > 0:
                self.return_cards()
            
            # writes all cards down to disk
            self.save_session()
            
            # clear session cards for next session   
            self.session_box.clear()
            
            self.terminal_viewer.display_message("Session Saved...")
    