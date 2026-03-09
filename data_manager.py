import json, os
from datetime import datetime
from typing import List, Dict, Any

class DataManager:
    def __init__(self, data_file: str = "finance_data.json"):
        self.data_file = data_file
        self.transactions: List[Dict[str, Any]] = []
        self.investments: List[Dict[str, Any]] = []
        self.debts: List[Dict[str, Any]] = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.transactions = data.get("transactions", [])
                    self.investments = data.get("investments", [])
                    self.debts = data.get("debts", [])
            except Exception as e:
                print(f"Error loading data: {e}")

    def save_data(self):
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump({
                    "transactions": self.transactions,
                    "investments": self.investments,
                    "debts": self.debts
                }, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    # --- CRUD de Transacciones / Inversiones / Deudas ---
    def add_transaction(self, t_type: str, amount: float, category: str, description: str):
        self.transactions.append({
            "type": t_type, "amount": amount, "category": category,
            "description": description, "date": datetime.now().strftime("%Y-%m-%d")
        })
        self.save_data()

    def add_investment(self, inv_type: str, name: str, amount: float, purchase: float, current: float):
        self.investments.append({
            "type": inv_type, "name": name, "amount": amount,
            "purchase_price": purchase, "current_price": current
        })
        self.save_data()

    def add_debt(self, name: str, total: float, monthly: float, category: str):
        self.debts.append({
            "name": name, "total_amount": total, "monthly_payment": monthly,
            "category": category, "paid_amount": 0
        })
        self.save_data()

    def delete(self, data_list: list, index: int):
        if 0 <= index < len(data_list):
            data_list.pop(index)
            self.save_data()

    # --- Estadísticas ---
    def get_total_income(self) -> float:
        return sum(t["amount"] for t in self.transactions if t["type"] == "ingreso")

    def get_total_expenses(self) -> float:
        return sum(t["amount"] for t in self.transactions if t["type"] == "gasto")

    def get_balance(self) -> float:
        return self.get_total_income() - self.get_total_expenses()

    def get_expenses_by_category(self) -> Dict[str, float]:
        res = {}
        for t in self.transactions:
            if t["type"] == "gasto":
                res[t["category"]] = res.get(t["category"], 0) + t["amount"]
        return res
