# Leitner System Implementation

This project implements a very simple [Leitner System](https://subjectguides.york.ac.uk/study-revision/leitner-system) in the terminal, which is a spaced repetition technique for learning flashcards. 

## Prerequisites ✔

* [Python 3](https://www.python.org/downloads/)

## Folder content 🗃️
```
/src
    ├── errors.py  # Custom error objects
    ├── storage.py # Reads and writes system state to disk
    ├── models.py  # Holds box, card, session_counter models
    ├── system.py  # Manages and runs the system       
    └── ui.py      # Displays and retrieves user input in the terminal
```

## Setup and Run ⚙️

Clone the repository
```
git clone https://github.com/mgr0098/leitner-system
```

Run in your terminal

```
python3 main.py
```

The system will display in the terminal a front card which you must answer either Yes (Y) or No (No) if you know the answer. The system is configured with a review on every 1st, 3rd, and 7nd session. If you answer wrong, the card gets moved to the first "box", if you answer correctly it gets promoted. Cards are mastered and removed from the list when they pass the final box.

Note! This means that if you pass a card on the first attempt, youre not going to see it until the 3rd session.


