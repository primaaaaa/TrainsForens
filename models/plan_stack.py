from typing import Dict, List, Optional

class PlanStack:
    def __init__(self):
        self.items = []

    def push(self, item: Dict) -> None:
        self.items.append(item)

    def pop(self) -> Optional[Dict]:
        if not self.is_empty():
            return self.items.pop()
        return None

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def peek(self) -> Optional[Dict]:
        if not self.is_empty():
            return self.items[-1]
        return None

    def get_all(self) -> List[Dict]:
        return self.items.copy()
