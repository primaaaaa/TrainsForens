import datetime
from typing import Dict, List, Optional

from models.schedule_linked_list import ScheduleNode, ScheduleLinkedList
from models.schedule_bst import ScheduleBST
from models.plan_stack import PlanStack
from data_loader import (
    ensure_data_dir,
    load_users, save_users,
    load_schedules, save_schedules,
    load_user_plans, save_user_plans,
    load_user_plan_history, save_user_plan_history
)

class TrainTicketSystem:
    def __init__(self):
        ensure_data_dir()

        self.users = load_users()
        self.schedules = ScheduleLinkedList()
        self.schedule_bst = ScheduleBST()
        self.user_plans = load_user_plans()
        self.user_plan_history = load_user_plan_history()
        self.current_user = None
        self.is_admin = False

        for data in load_schedules():
            node = ScheduleNode(**data)
            self.schedules.add_schedule(node)

        self.update_schedule_bst()

    def save_all(self):
        save_users(self.users)
        save_schedules(self.schedules.get_all_schedules())
        save_user_plans(self.user_plans)
        save_user_plan_history(self.user_plan_history)

    def update_schedule_bst(self):
        self.schedule_bst.build_from_list(self.schedules.get_all_schedules())

    def register(self, username: str, password: str, is_admin: bool = False) -> bool:
        if username in self.users:
            return False
        self.users[username] = {"password": password, "is_admin": is_admin}
        save_users(self.users)
        return True

    def login(self, username: str, password: str) -> bool:
        if username in self.users and self.users[username]["password"] == password:
            self.current_user = username
            self.is_admin = self.users[username]["is_admin"]
            return True
        return False

    def logout(self):
        self.current_user = None
        self.is_admin = False

    def get_current_user(self):
        return self.current_user

    def add_schedule(self, departure, destination, train_name, date,
                     departure_time, arrival_time, price, available_seats) -> bool:
        if not self.is_admin:
            return False
        schedule_id = f"SCH{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        schedule = ScheduleNode(schedule_id, departure, destination, train_name,
                                 date, departure_time, arrival_time, price, available_seats)
        self.schedules.add_schedule(schedule)
        self.update_schedule_bst()
        save_schedules(self.schedules.get_all_schedules())
        return True

    def update_schedule(self, schedule_id: str, updated_data: Dict) -> bool:
        if not self.is_admin:
            return False
        if self.schedules.update_schedule(schedule_id, updated_data):
            self.update_schedule_bst()
            save_schedules(self.schedules.get_all_schedules())
            return True
        return False

    def delete_schedule(self, schedule_id: str) -> bool:
        if not self.is_admin:
            return False
        if self.schedules.delete_schedule(schedule_id):
            self.update_schedule_bst()
            save_schedules(self.schedules.get_all_schedules())
            self.user_plans[schedule_id] = 0
            if self.user_plans[schedule_id] <= 0:
                del self.user_plans[schedule_id]
            return True
        return False

    def get_all_schedules(self) -> List[Dict]:
        return self.schedules.get_all_schedules()

    def search_schedules(self, category: str, value: str) -> List[Dict]:
        if category == "departure":
            return self.schedule_bst.search_by_departure(value)
        elif category == "destination":
            return self.schedule_bst.search_by_destination(value)
        elif category == "train_name":
            return self.schedule_bst.search_by_train_name(value)
        return self.schedule_bst.inorder_traversal()

    def sort_schedules(self, category: str) -> List[Dict]:
        schedules = self.schedule_bst.inorder_traversal()
        return sorted(schedules, key=lambda x: x.get(category, x["schedule_id"]))

    def create_plan(self, schedule_id: str, date: str) -> bool:
        if not self.current_user or self.is_admin:
            return False
        schedule = self.schedules.find_schedule_by_id(schedule_id)
        if not schedule:
            return False
        
        if self.current_user in self.user_plan_history:
            for plan in self.user_plan_history[self.current_user].get_all():
                if plan["schedule"]["schedule_id"] == schedule_id:
                    print("Anda sudah membuat rencana perjalanan ini")
                    return False  # Sudah ada rencana dengan schedule_id yang sama
        plan_data = {
            "plan_id": f"PLAN{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            "schedule": schedule.to_dict(),
            "date": date,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        if self.current_user not in self.user_plan_history:
            self.user_plan_history[self.current_user] = PlanStack()
        self.user_plan_history[self.current_user].push(plan_data)
        self.user_plans[schedule_id] = self.user_plans.get(schedule_id, 0) + 1
        self.save_all()
        return True

    def get_user_plan_history(self) -> List[Dict]:
        if not self.current_user or self.is_admin:
            return []
        if self.current_user not in self.user_plan_history:
            return []
        return self.user_plan_history[self.current_user].get_all()

    def get_users_plan_count(self) -> Dict[str, int]:
        return self.user_plans
                
    def clear_user_plan_history(self, username: str):
        if username in self.user_plan_history:
            # Ambil semua plan yang dimiliki user sebelum dihapus
            plans = self.user_plan_history[username].get_all()
            
            # Kurangi count pada user_plans berdasarkan schedule_id dari tiap plan
            for plan in plans:
                schedule_id = plan['schedule']['schedule_id']
                if schedule_id in self.user_plans:
                    self.user_plans[schedule_id] -= 1
                    if self.user_plans[schedule_id] <= 0:
                        del self.user_plans[schedule_id]

            # Hapus histori rencana user
            self.user_plan_history[username] = PlanStack()
            self.save_all()
