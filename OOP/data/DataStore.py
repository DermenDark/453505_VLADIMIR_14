from typing import List, Optional, Dict, Any
import uuid
import datetime
import json

def gen_id(prefix: str = "") -> str:
    return prefix + str(uuid.uuid4())[:8]

def now_iso() -> str:
    return datetime.datetime.utcnow().isoformat()

# Domain models
class LogEntry:
    def __init__(self, actor_id: str, action: str, payload: dict, timestamp: Optional[str] = None):
        self.id = gen_id("log_")
        self.actor_id = actor_id
        self.action = action
        self.payload = payload
        self.timestamp = timestamp or now_iso()

    def to_dict(self):
        return {"id": self.id, "actor_id": self.actor_id, "action": self.action, "payload": self.payload, "timestamp": self.timestamp}

class Transaction:
    def __init__(self, src_type: str, src_id: str, dst_type: str, 
                 dst_id: str, amount: float, actor_id: str):
        self.id = gen_id("tx_")
        self.src_type = src_type  
        self.src_id = src_id
        self.dst_type = dst_type
        self.dst_id = dst_id
        self.amount = amount
        self.timestamp = now_iso()
        self.actor_id = actor_id

    def to_dict(self):
        return {
            "id": self.id,
            "src_type": self.src_type,
            "src_id": self.src_id,
            "dst_type": self.dst_type,
            "dst_id": self.dst_id,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "actor_id": self.actor_id,
        }

class Account:
    def __init__(self, bank_id: str, owner_id: str, 
                 balance: float = 0.0, blocked: bool = False):
        self.id = gen_id("acc_")
        self.bank_id = bank_id
        self.owner_id = owner_id
        self.balance = float(balance)
        self.blocked = blocked
        self.history: List[Transaction] = []

    def deposit(self, amount: float, tx: Transaction):
        if self.blocked:
            raise ValueError("Счет заблокирован.")
        if amount <= 0:
            raise ValueError("Сумма должна быть > 0.")
        self.balance += amount
        self.history.append(tx)

    def withdraw(self, amount: float, tx: Transaction):
        if self.blocked:
            raise ValueError("Счет заблокирован.")
        if amount <= 0:
            raise ValueError("Сумма должна быть > 0.")
        if self.balance < amount:
            raise ValueError("Недостаточно средств.")
        self.balance -= amount
        self.history.append(tx)

    def to_dict(self):
        return {"id": self.id, "bank_id": self.bank_id, 
                "owner_id": self.owner_id, "balance": self.balance, 
                "blocked": self.blocked}

class Deposit:
    def __init__(self, bank_id: str, owner_id: str, principal: float, 
                 rate_pct: float, term_months: int, blocked: bool = False):
        self.id = gen_id("dep_")
        self.bank_id = bank_id
        self.owner_id = owner_id
        self.principal = float(principal)
        self.rate_pct = float(rate_pct)
        self.term_months = int(term_months)
        self.blocked = blocked
        self.created_at = now_iso()
        self.history: List[Transaction] = []

    def accrue_month(self):
        # простая месячная капитализация
        monthly_rate = self.rate_pct / 100.0 / 12.0
        self.principal += self.principal * monthly_rate

    def to_dict(self):
        return {"id": self.id, "bank_id": self.bank_id,
                "owner_id": self.owner_id, "principal": self.principal, 
                "rate_pct": self.rate_pct, "term_months": self.term_months, "blocked": self.blocked}

class Bank:
    def __init__(self, name: str):
        self.id = gen_id("bank_")
        self.name = name
        self.accounts: Dict[str, Account] = {}
        self.deposits: Dict[str, Deposit] = {}

    def to_dict(self):
        return {"id": self.id, "name": self.name}

class Enterprise:
    def __init__(self, name: str, manager_id: Optional[str] = None, funds: float = 0.0):
        self.id = gen_id("ent_")
        self.name = name
        self.manager_id = manager_id 
        self.employees: List[str] = [] 
        self.funds = float(funds)
        self.payroll_requests: Dict[str, Dict[str, Any]] = {}  
    def to_dict(self):
        return {"id": self.id, "name": self.name, "funds": self.funds}

class User:
    def __init__(self, login: str, full_name: str, role: str, password: str):
        self.id = gen_id("usr_")
        self.login = login
        self.full_name = full_name
        self.role = role 
        self.password = password
        self.confirmed = role != "client"  

    def to_dict(self):
        return {"id": self.id, "login": self.login, "full_name": self.full_name, 
                "role": self.role, "confirmed": self.confirmed}

# Repositories / Managers (Single Responsibility)
class DataStore:
    """Хранит все сущности в памяти (для demo). Можно добавить сериализацию."""
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.banks: Dict[str, Bank] = {}
        self.enterprises: Dict[str, Enterprise] = {}
        self.logs: List[LogEntry] = []
        self.transactions: Dict[str, Transaction] = {}

        self.accounts_index: Dict[str, Account] = {}
        self.deposits_index: Dict[str, Deposit] = {}

    def save_log(self, entry: LogEntry):
        self.logs.append(entry)

    def save_tx(self, tx: Transaction):
        self.transactions[tx.id] = tx

    def dump_to_file(self, path="demo_state.json"):
        obj = {
            "users": {u_id: u.to_dict() for u_id, u in self.users.items()},
            "banks": {b_id: {"meta": bank.to_dict(),
                             "accounts": {acc.id: acc.to_dict() for acc in bank.accounts.values()},
                             "deposits": {dep.id: dep.to_dict() for dep in bank.deposits.values()}} 
                             for b_id, bank in self.banks.items()},
            "enterprises": {e_id: ent.to_dict() for e_id, ent in self.enterprises.items()},
            "logs": [l.to_dict() for l in self.logs],
            "transactions": {tx_id: tx.to_dict() for tx_id, tx in self.transactions.items()}
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        print(f"State dumped to {path}")