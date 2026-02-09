from src.storage import StorageManager
from src.models import SessionCounter
from src.ui import TerminalViewer
from src.system import System
from src.errors import CardSystemError, StorageManagerError

VOCABULARY_PATH = "data/vocabulary.json"
box_config = [{"name": "daily", "level": 1}, {"name": "every_3rd_day", "level": 3},{"name": "weekly", "level": 7}]

"""
Main loop, initalize the system and run them, 
all errors are propogated up here
"""
def main():
        storage_manager = StorageManager(VOCABULARY_PATH)
        session_counter = SessionCounter()
        terminal_viewer = TerminalViewer()
            
        system = System(box_config, session_counter, terminal_viewer, storage_manager)
        try: 
            system.run_session()
        except StorageManagerError:
            print("Error in storage manager")
        except KeyboardInterrupt:
            print("Progress Saved ...")
        except CardSystemError as cse:
            print(cse)

if __name__ == "__main__":
    main()
    