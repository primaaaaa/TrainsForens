from typing import Dict, List, Optional

class BSTNode:
    def __init__(self, data: Dict):
        self.data = data
        self.left = None
        self.right = None

class ScheduleBST:
    def __init__(self):
        self.root = None

    def insert(self, data: Dict) -> None:
        if not self.root:
            self.root = BSTNode(data)
            return
        self._insert_recursive(self.root, data)

    def _insert_recursive(self, node: BSTNode, data: Dict) -> None:
        if data["schedule_id"] < node.data["schedule_id"]:
            if node.left is None:
                node.left = BSTNode(data)
            else:
                self._insert_recursive(node.left, data)
        else:
            if node.right is None:
                node.right = BSTNode(data)
            else:
                self._insert_recursive(node.right, data)

    def search(self, schedule_id: str) -> Optional[Dict]:
        return self._search_recursive(self.root, schedule_id)

    def _search_recursive(self, node: BSTNode, schedule_id: str) -> Optional[Dict]:
        if not node:
            return None
        if node.data["schedule_id"] == schedule_id:
            return node.data
        if schedule_id < node.data["schedule_id"]:
            return self._search_recursive(node.left, schedule_id)
        return self._search_recursive(node.right, schedule_id)

    def inorder_traversal(self) -> List[Dict]:
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node: BSTNode, result: List) -> None:
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.data)
            self._inorder_recursive(node.right, result)

    def search_by_departure(self, departure: str) -> List[Dict]:
        result = []
        self._search_by_attribute(self.root, "departure", departure, result)
        return result

    def search_by_destination(self, destination: str) -> List[Dict]:
        result = []
        self._search_by_attribute(self.root, "destination", destination, result)
        return result

    def search_by_train_name(self, train_name: str) -> List[Dict]:
        result = []
        self._search_by_attribute(self.root, "train_name", train_name, result)
        return result

    def _search_by_attribute(self, node: BSTNode, attr: str, value: str, result: List) -> None:
        if node:
            self._search_by_attribute(node.left, attr, value, result)
            if node.data.get(attr, "").lower() == value.lower():
                result.append(node.data)
            self._search_by_attribute(node.right, attr, value, result)

    def clear(self) -> None:
        self.root = None

    def build_from_list(self, schedules: List[Dict]) -> None:
        self.clear()
        for schedule in schedules:
            self.insert(schedule)
