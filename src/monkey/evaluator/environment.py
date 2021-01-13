"""implements Environments for Monkey language"""

from typing import Optional
from monkey.evaluator import mobjects

class Environment():
    def __init__(self, outer = None):
        self.store = dict()
        self.outer = outer
    
    def get(self, name: str) -> Optional[mobjects.Object]:
        value = self.store.get(name, None)
        if value is None and self.outer is not None:
            return self.outer.get(name)
        return value

    def set(self, name: str, value: mobjects.Object) -> mobjects.Object:
        self.store[name] = value
        return value
    
    def __str__(self):
        return str(self.store)
    
    def __repr__(self):
        return self.__str__()
