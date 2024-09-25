from pydantic import BaseModel, RootModel, Field
from typing import List
import os
from datetime import datetime

class History(BaseModel):
    timestamp: str = Field(..., default_factory=lambda: datetime.now().isoformat())
    input: str
    result: str

class HistoryList(RootModel):
    root: List[History] = []

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
    
    def __len__(self):
        return len(self.root)
    
    def append(self, history: History):
        self.root.append(history)

class Memory():
    """
    Memory class to store the history of all previously executed inputs and results.
    History is stored in a list of History objects.
    The history list is saved to a file on disk, and loaded from the file when the program starts.
    """
    MAX_MEMORY = 10

    def __init__(self, filename: str):
        self.filename = filename
        self.history = self.load()

    def load(self):
        try:
            with open(self.filename, "r") as file:
                b_history = file.read()
                if b_history != "":
                    history = HistoryList.model_validate_json(b_history)
                else:
                    history = HistoryList()

        except FileNotFoundError:
            # If the file doesn't exist, create an empty history list and save it to disk            
            history = HistoryList()
            self.init_file()

        return history

    def init_file(self):
        if not os.path.exists(os.path.dirname(self.filename)):
            os.makedirs(os.path.dirname(self.filename))
        self._save(HistoryList())
    
    def save(self):
        self._save(self.history)

    def _save(self, history: HistoryList):
        with open(self.filename, "w") as file:
            file.write(history.model_dump_json())    

    def add(self, input: str, result: str):
        history_obj = History(input=input, result=result)
        self.history.append(history_obj)
        # purge old history
        if len(self.history) > self.MAX_MEMORY:
            self.history.root = self.history.root[-self.MAX_MEMORY:]
        self.save()
    
    def get_last(self, x:int)->History:
        return self.history[-x:] if len(self.history) > x else self.history.root