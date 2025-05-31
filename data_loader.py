import os
import json
from typing import List, Dict
from models.plan_stack import PlanStack

DATA_DIR = "data"

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def load_users() -> Dict[str, Dict]:
    try:
        with open(os.path.join(DATA_DIR, "users.json"), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "admin": {
                "password": "admin123",
                "is_admin": True
            }
        }

def save_users(users: Dict[str, Dict]) -> None:
    with open(os.path.join(DATA_DIR, "users.json"), "w") as f:
        json.dump(users, f, indent=4)

def load_schedules() -> List[Dict]:
    try:
        with open(os.path.join(DATA_DIR, "schedules.json"), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_schedules(schedules: List[Dict]) -> None:
    with open(os.path.join(DATA_DIR, "schedules.json"), "w") as f:
        json.dump(schedules, f, indent=4)

def load_user_plans() -> Dict[str, int]:
    try:
        with open(os.path.join(DATA_DIR, "user_plans.json"), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_user_plans(user_plans: Dict[str, int]) -> None:
    with open(os.path.join(DATA_DIR, "user_plans.json"), "w") as f:
        json.dump(user_plans, f, indent=4)

def load_user_plan_history() -> Dict[str, PlanStack]:
    history = {}
    try:
        with open(os.path.join(DATA_DIR, "user_plan_history.json"), "r") as f:
            data = json.load(f)
            for username, plans in data.items():
                stack = PlanStack()
                for plan in plans:
                    stack.push(plan)
                history[username] = stack
    except FileNotFoundError:
        pass
    return history

def save_user_plan_history(plan_history: Dict[str, PlanStack]) -> None:
    data = {username: stack.get_all() for username, stack in plan_history.items()}
    with open(os.path.join(DATA_DIR, "user_plan_history.json"), "w") as f:
        json.dump(data, f, indent=4)
