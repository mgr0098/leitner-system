import logging

from src.importer import CardImporter
from src.models import SessionCounter
from src.ui import TerminalViewer
from src.system import System
from src.errors import CardSystemError

VOCABULARY_PATH = "data/vocabulary.json"

box_config = [{"name": "daily", "level": 1}, {"name": "every_3rd_day", "level": 3},{"name": "weekly", "level": 7}]
        
def main():
    try: 
        card_importer = CardImporter(VOCABULARY_PATH)
        session_counter = SessionCounter()
        terminal_viewer = TerminalViewer()
    
        system = System(card_importer.cards, box_config, session_counter, terminal_viewer)
        system.run_session()
    except KeyboardInterrupt:
        print("Progress Saved ...")
    except CardSystemError as cse:
        print(cse)
    except:
        print()

if __name__ == "__main__":
    main()
    