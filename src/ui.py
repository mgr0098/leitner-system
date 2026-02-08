import os

"""Speaks to the terminal, retrives response from user"""
class TerminalViewer():
    def __init__(self):
        self.padding = 15
        self.success = "y"
        self.fail = "n"
    
    """Displays the card in a clean manner to the terminal""" 
    def display_card(self, card):
        self.clear_screen()
        
        print("=" * self.padding)
        print(f" CARD FRONT: {card.front}")
        print("=" * self.padding)
        input("\nPress [Enter] to see the answer")
        print(f"\n CARD BACK: {card.back}")
        print("=" * self.padding)

    """Clears terminal screen for windows, mac, and linux """
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    """Keep prints to terminal limited to this class"""
    def display_message(self, message):
        print(message)
    
    """
    Displays card to the terminal and retrieves the response
    returns None if something went wrong
    """
    def get_user_input(self, card):
        while True:
            self.display_card(card)
            try:
                user_input = input("Did you get it right? (y/n)")
                
                if user_input == self.success:
                    return True
                elif user_input == self.fail:
                    return False
            except KeyboardInterrupt:
                return None
            return None
