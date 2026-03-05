import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional

# Dialogs / helpers
class CreateDepositDialog(tk.Toplevel):
    def __init__(self, parent, bank_choices: dict):
        super().__init__(parent)
        self.title("Создать вклад")
        self.result: Optional[tuple] = None
        tk.Label(self, text="Выберите банк (id):").pack(anchor="w")
        self.bank_var = tk.StringVar(value=list(bank_choices.keys())[0] if bank_choices else "")
        banks_combo = ttk.Combobox(self, values=[f"{k} — {v}" for k, v in bank_choices.items()], state="readonly")
        banks_combo.pack(fill="x")
        if bank_choices:
            banks_combo.current(0)
        tk.Label(self, text="Сумма (principal):").pack(anchor="w")
        self.principal_entry = tk.Entry(self)
        self.principal_entry.pack(fill="x")
        tk.Label(self, text="Годовой процент (rate):").pack(anchor="w")
        self.rate_entry = tk.Entry(self)
        self.rate_entry.pack(fill="x")
        tk.Label(self, text="Срок в месяцах (term):").pack(anchor="w")
        self.term_entry = tk.Entry(self)
        self.term_entry.pack(fill="x")
        def on_ok():
            val = banks_combo.get()
            if not val:
                messagebox.showwarning("Ошибка", "Выберите банк.")
                return
            bank_id = val.split(" — ")[0]
            try:
                principal = float(self.principal_entry.get().strip())
                rate = float(self.rate_entry.get().strip())
                term = int(self.term_entry.get().strip())
            except Exception:
                messagebox.showwarning("Ошибка", "Неверные входные значения.")
                return
            self.result = (bank_id, principal, rate, term)
            self.destroy()
        tk.Button(self, text="Создать", command=on_ok).pack(pady=8)

class TransferDialog(tk.Toplevel):
    def __init__(self, parent, store, tx_service, user):
        super().__init__(parent)
        self.store = store
        self.tx_service = tx_service
        self.user = user
        self.title("Перевод средств")
        self.geometry("480x360")
        tk.Label(self, text="Источник (тип: account/deposit):").pack(anchor="w")
        self.src_type = tk.Entry(self); self.src_type.insert(0,"account"); self.src_type.pack(fill="x")
        tk.Label(self, text="Источник id:").pack(anchor="w")
        self.src_id = tk.Entry(self); self.src_id.pack(fill="x")
        tk.Label(self, text="Назначение (account/deposit/enterprise):").pack(anchor="w")
        self.dst_type = tk.Entry(self); self.dst_type.insert(0,"account"); self.dst_type.pack(fill="x")
        tk.Label(self, text="Назначение id:").pack(anchor="w")
        self.dst_id = tk.Entry(self); self.dst_id.pack(fill="x")
        tk.Label(self, text="Сумма:").pack(anchor="w")
        self.amount = tk.Entry(self); self.amount.pack(fill="x")
        btn = tk.Button(self, text="Перевести", command=self.do_transfer)
        btn.pack(pady=8)

        tk.Label(self, text="(Подсказка) Ваши счета и вклады:").pack(anchor="w", pady=(6,0))
        info = tk.Text(self, height=6)
        info.pack(fill="both", expand=True)
        for a in self.store.accounts_index.values():
            if a.owner_id == self.user.id:
                info.insert("end", f"ACC {a.id} balance={a.balance:.2f}\n")
        for d in self.store.deposits_index.values():
            if d.owner_id == self.user.id:
                info.insert("end", f"DEP {d.id} principal={d.principal:.2f}\n")
        info.config(state="disabled")

    def do_transfer(self):
        src_t = self.src_type.get().strip()
        src_id = self.src_id.get().strip()
        dst_t = self.dst_type.get().strip()
        dst_id = self.dst_id.get().strip()
        try:
            amt = float(self.amount.get().strip())
        except:
            messagebox.showerror("Ошибка", "Неверная сумма.")
            return
        try:
            tx = self.tx_service.transfer(src_t, src_id, dst_t, dst_id, amt, actor_id=self.user.id)
            messagebox.showinfo("Успех", f"Перевод выполнен. tx_id: {tx.id}")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка перевода", str(e))
