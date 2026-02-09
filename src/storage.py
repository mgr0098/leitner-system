import json
import os
from dataclasses import asdict
from src.errors import StorageManagerError


"""
Example json string to store system state

{
    "current_session": 0, 
    "cards": 
        [{"front": "Gatto", "back": "Cat", "level": 0}, 
        {"front": "Cane", "back": "Dog", "level": 0}, 
        {"front": "Mela", "back": "Apple", "level":0}]
}
"""

"""Manages disk read and write"""
class StorageManager():
    def __init__(self, file_path):
        self.file_path = file_path
    
    """imports json file and returns is a dict """
    def import_json_file(self):
        if not os.path.exists(self.file_path):
            raise StorageManagerError(f"Cannot Find File Path {self.file_path}")
        
        try:
            # read json string from the file path
            with open(self.file_path) as fp:
                data = json.load(fp)
                return data
        except:
            raise StorageManagerError("Unable to import data")
    
    """Writes boxes into json on filepath"""
    def write_to_json(self, data):
        if not os.path.exists(self.file_path):
            raise StorageManagerError(f"Cannot Find Filepath {self.file_path}")

        try:
            # write dictionaries to file
            with open(self.file_path, "w", encoding="utf-8") as fp:
                json.dump(data, fp, indent=4) #writes it cleanly to the file
        except:
            raise StorageManagerError("Unable to write data")
    
    """Returns json serialized boxes """
    def serialize_boxes(self, boxes):
        try:
            data = []
            
            for box in boxes:
                if box.length > 0:                
                    # create dict from dataclass
                    seralized_box = [asdict(card) for card in box.cards]
                    data.extend(seralized_box) # keep list flat
            
            return data
        except:
            raise StorageManagerError("Unable to serialize boxes")
    
            
