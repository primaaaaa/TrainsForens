from typing import Dict, List, Optional

class ScheduleNode:
    def __init__(self, schedule_id: str, departure: str, destination: str, 
                 train_name: str, date:str ,departure_time: str, arrival_time: str, 
                 price: float, available_seats: int):
        self.schedule_id = schedule_id
        self.departure = departure
        self.destination = destination
        self.train_name = train_name
        self.date = date
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.price = price
        self.available_seats = available_seats
        self.next = None

    def to_dict(self) -> Dict:
        return {
            "schedule_id": self.schedule_id,
            "departure": self.departure,
            "destination": self.destination,
            "train_name": self.train_name,
            "date": self.date,
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
            "price": self.price,
            "available_seats": self.available_seats
        }

class ScheduleLinkedList:
    def __init__(self):
        self.head = None

    def add_schedule(self, schedule: ScheduleNode) -> None:
        if not self.head:
            self.head = schedule
            return

        current = self.head
        while current.next:
            current = current.next
        current.next = schedule

    def find_schedule_by_id(self, schedule_id: str) -> Optional[ScheduleNode]:
        current = self.head
        while current:
            if current.schedule_id == schedule_id:
                return current
            current = current.next
        return None

    def update_schedule(self, schedule_id: str, updated_data: Dict) -> bool:
        schedule = self.find_schedule_by_id(schedule_id)
        if not schedule:
            return False

        for key, value in updated_data.items():
            if hasattr(schedule, key):
                setattr(schedule, key, value)

        return True

    def delete_schedule(self, schedule_id: str) -> bool:
        if not self.head:
            return False

        if self.head.schedule_id == schedule_id:
            self.head = self.head.next
            return True

        current = self.head
        while current.next:
            if current.next.schedule_id == schedule_id:
                current.next = current.next.next
                return True
            current = current.next

        return False

    def get_all_schedules(self) -> List[Dict]:
        schedules = []
        current = self.head
        while current:
            schedules.append(current.to_dict())
            current = current.next
        return schedules
