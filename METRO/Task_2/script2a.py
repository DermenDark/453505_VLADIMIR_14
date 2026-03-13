# gilb_mccabe_analyzer.py
import ast
import os
import math
import customtkinter as ctk
from tkinter import filedialog, messagebox
from tabulate import tabulate

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MetricsVisitor(ast.NodeVisitor):
    """
    AST-visitor that collects:
      - CL (Gilb absolute complexity)
      - total statements (N_ops proxy)
      - maximum nesting depth of conditional operators (CLI)
      - cyclomatic complexity per function (Z = 1 + decision_points)
    """

    def __init__(self):
        self.total_statements = 0 
        self.CL = 0  
        self.max_if_depth = 0  
        self._if_depth_stack = [0]

        self.cyclomatic = {} 
        self._func_decision_stack = [] 
        self._current_func_name_stack = [] 

    def _inc_statement(self):
        self.total_statements += 1

    def _add_decision(self, count=1):
        """Add decision points to current function (if any) and to CL."""
        self.CL += count
        if self._func_decision_stack:
            self._func_decision_stack[-1] += count
        else:
            self.cyclomatic.setdefault('<module>', 0)
            self.cyclomatic['<module>'] += count

    def _enter_if(self):
        self._if_depth_stack.append(self._if_depth_stack[-1] + 1)
        if self._if_depth_stack[-1] > self.max_if_depth:
            self.max_if_depth = self._if_depth_stack[-1]

    def _exit_if(self):
        self._if_depth_stack.pop()

    def visit(self, node):
        if isinstance(node, ast.stmt):
            self._inc_statement()
        return super().visit(node)

    def generic_visit(self, node):
        super().generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        name = node.name
        self._func_decision_stack.append(0)
        self._current_func_name_stack.append(name)
        self.generic_visit(node)
        d = self._func_decision_stack.pop()
        z = 1 + d
        self.cyclomatic[name] = z
        self._current_func_name_stack.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.visit_FunctionDef(node)

    def visit_If(self, node: ast.If):
        self._add_decision(1)
        self._enter_if()
        self.generic_visit(node.test)
        for stmt in node.body:
            self.visit(stmt)
        self._exit_if()
        for stmt in node.orelse:
            self.visit(stmt)

    def visit_For(self, node: ast.For):
        self._add_decision(1)
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor):
        self.visit_For(node)

    def visit_While(self, node: ast.While):
        self._add_decision(1)
        self.generic_visit(node)

    def visit_IfExp(self, node: ast.IfExp):
        self._add_decision(1)
        self._enter_if()
        self.generic_visit(node)
        self._exit_if()

    def visit_BoolOp(self, node: ast.BoolOp):
        count = max(0, len(node.values) - 1)
        if count:
            self._add_decision(count)
        self.generic_visit(node)

    def visit_Match(self, node: ast.Match):
        cases = len(node.cases)
        if cases >= 2:
            match_decisions = cases
            self._add_decision(match_decisions)
            depth_increment = max(0, cases)
        else:
            depth_increment = 0

        self._if_depth_stack.append(self._if_depth_stack[-1] + depth_increment)
        if self._if_depth_stack[-1] > self.max_if_depth:
            self.max_if_depth = self._if_depth_stack[-1]

        self.generic_visit(node.subject)
        for case in node.cases:
            self.generic_visit(case.pattern)
            if case.guard:
                self.visit(case.guard)
            for stmt in case.body:
                self.visit(stmt)

        self._if_depth_stack.pop()

    def visit_comprehension(self, node: ast.comprehension):
        if node.ifs:
            self._add_decision(len(node.ifs))
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try):
        handlers = len(node.handlers)
        if handlers:
            self._add_decision(handlers)

        self.generic_visit(node)



def analyze_code_metrics(code_text: str):
    """
    Parse code_text, run MetricsVisitor, and return dictionary:
      - CL, N_ops, cl, CLI
      - cyclomatic per function (Z)
      - total/module-level Z
    """
    try:
        tree = ast.parse(code_text)
    except Exception as e:
        raise SyntaxError(f"Ошибка парсинга AST: {e}")

    visitor = MetricsVisitor()
    visitor.visit(tree)

    CL = visitor.CL
    N_ops = visitor.total_statements if visitor.total_statements > 0 else 1
    cl = CL / N_ops
    CLI = visitor.max_if_depth

    cyclomatic = {}
    for name, z_or_d in visitor.cyclomatic.items():
        if isinstance(z_or_d, int):
            cyclomatic[name] = 1 + z_or_d if name == '<module>' else z_or_d
        else:
            cyclomatic[name] = z_or_d

    if '<module>' in cyclomatic and isinstance(cyclomatic['<module>'], int):
        cyclomatic['<module>'] = 1 + cyclomatic['<module>']

    total_Z = sum(cyclomatic.values())

    return {
        'CL': CL,
        'N_ops': N_ops,
        'cl': cl,
        'CLI': CLI-1,
        'cyclomatic_per_name': cyclomatic,
        'total_Z': total_Z
    }

class GilbMcCabeAnalyzerGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Анализатор метрик: Gilb & McCabe")
        self.root.geometry("1200x820")

        self.current_file_path = ctk.StringVar(value="")

        self.create_widgets()

    def create_widgets(self):
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=16, pady=16)

        title_label = ctk.CTkLabel(
            self.main_container,
            text="Анализатор метрик: Gilb (CL, cl, CLI) и McCabe (Z)",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(6, 12))

        file_frame = ctk.CTkFrame(self.main_container)
        file_frame.pack(fill="x", padx=6, pady=6)

        self.file_path_label = ctk.CTkLabel(
            file_frame,
            textvariable=self.current_file_path,
            font=ctk.CTkFont(size=12),
            wraplength=700,
            text_color="gray"
        )
        self.file_path_label.pack(side="left", padx=8, expand=True, fill="x")

        self.select_file_btn = ctk.CTkButton(
            file_frame,
            text="Выбрать файл",
            command=self.select_file,
            width=150,
            height=35
        )
        self.select_file_btn.pack(side="right", padx=8)

        self.tabview = ctk.CTkTabview(self.main_container)
        self.tabview.pack(fill="both", expand=True, padx=6, pady=8)

        self.tabview.add("Код программы")
        self.code_tab = self.tabview.tab("Код программы")

        self.code_text = ctk.CTkTextbox(
            self.code_tab,
            font=ctk.CTkFont(family="Courier New", size=12),
            wrap="none"
        )
        self.code_text.pack(fill="both", expand=True, padx=8, pady=8)

        self.tabview.add("Результаты анализа")
        self.results_tab = self.tabview.tab("Результаты анализа")

        self.results_text = ctk.CTkTextbox(
            self.results_tab,
            font=ctk.CTkFont(family="Courier New", size=12),
            wrap="word"
        )
        self.results_text.pack(fill="both", expand=True, padx=8, pady=8)

        button_frame = ctk.CTkFrame(self.main_container)
        button_frame.pack(fill="x", padx=6, pady=8)

        self.analyze_btn = ctk.CTkButton(
            button_frame,
            text="Анализировать код",
            command=self.analyze_code,
            height=40,
            fg_color="#28a745"
        )
        self.analyze_btn.pack(side="left", padx=6, expand=True, fill="x")

        self.load_example_btn = ctk.CTkButton(
            button_frame,
            text="Загрузить пример",
            command=self.load_example_code,
            height=40,
            fg_color="#17a2b8"
        )
        self.load_example_btn.pack(side="left", padx=6, expand=True, fill="x")

        self.clear_btn = ctk.CTkButton(
            button_frame,
            text="Очистить",
            command=self.clear_all,
            height=40,
            fg_color="#dc3545"
        )
        self.clear_btn.pack(side="left", padx=6, expand=True, fill="x")

        self.status_bar = ctk.CTkLabel(
            self.main_container,
            text="Готов к работе",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.status_bar.pack(side="bottom", fill="x", pady=4)

        self.load_example_code()

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Выберите Python файл",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                self.current_file_path.set(f"Файл: {os.path.basename(file_path)}")
                self.code_text.delete("1.0", "end")
                self.code_text.insert("1.0", code)
                self.update_status(f"Загружен файл: {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")
                self.current_file_path.set("")

    def get_example_code(self):
        return '''def calculate_discount(age, amount, day):
    discount = 0
    # simple conditional
    if age < 18:
        discount += 5
    else:
        discount += 2

    # loop with nested if
    for i in range(amount):
        if i % 2 == 0:
            discount += 1
            if discount > 10:
                discount -= 2
                if discount > 11:
                    discount -= 2
                    if discount > 12:
                        discount -= 2


    # match/case example (Python 3.10+)
    if age <2000:
        match day:
            case "monday":
                if age <100:
                    discount +=2
                discount += 3
            case "tuesday":
                discount += 2
            case "wednesday":
                discount += 4
            case _:
                discount += 1

    return discount
'''

    def load_example_code(self):
        self.code_text.delete("1.0", "end")
        self.code_text.insert("1.0", self.get_example_code())
        self.current_file_path.set("Пример кода")
        self.update_status("Загружен пример кода")

    def clear_all(self):
        self.code_text.delete("1.0", "end")
        self.results_text.delete("1.0", "end")
        self.current_file_path.set("")
        self.update_status("Все поля очищены")

    def update_status(self, message: str):
        self.status_bar.configure(text=message)

    def analyze_code(self):
        code = self.code_text.get("1.0", "end").rstrip()
        if not code:
            messagebox.showwarning("Предупреждение", "Введите код для анализа!")
            return

        try:
            metrics = analyze_code_metrics(code)
        except SyntaxError as e:
            messagebox.showerror("Ошибка синтаксиса", str(e))
            self.update_status("Ошибка синтаксиса")
            return
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при анализе: {e}")
            self.update_status("Ошибка при анализе")
            return

        self.display_results(metrics)
        self.update_status("Анализ завершён")

    def display_results(self, metrics: dict):
        self.results_text.delete("1.0", "end")

        CL = metrics['CL']
        N_ops = metrics['N_ops']
        cl = metrics['cl']
        CLI = metrics['CLI']
        cyclomatic = metrics['cyclomatic_per_name']
        total_Z = metrics['total_Z']

        header = "=" * 100 + "\n"
        header += " " * 30 + "Результаты анализа метрик Gilb & McCabe\n"
        header += "=" * 100 + "\n\n"
        self.results_text.insert("1.0", header)

        gilb_table = [
            ["CL (абс. сложность)", CL],
            ["N_ops (число операторов / stmt)", N_ops],
            ["cl (отн. сложность = CL / N_ops)", f"{cl:.4f}"],
            ["CLI (макс. вложенность IF)", CLI],
        ]
        self.results_text.insert("end", tabulate(gilb_table, tablefmt="fancy_grid") + "\n\n")

        rows = []
        for name, z in cyclomatic.items():
            rows.append([name, z])

        self.results_text.insert("end", "Цикломатическая сложность (по именам):\n")
        self.results_text.insert("end", tabulate(rows, headers=["Имя / область", "Z(G)"], tablefmt="fancy_grid") + "\n\n")

        self.results_text.insert("end", f"Суммарная Z(G) (все области): {total_Z}\n\n")

        recommendations = []
        if cl > 0.2:
            recommendations.append("Высокая относительная насыщенность условными операторами (cl > 0.2). Рассмотреть разбиение модуля на функции/классы.")
        if CLI > 3:
            recommendations.append("Глубокая вложенность IF (CLI > 3). Рефакторинг: вынос логики в функции, ранние возвраты, таблицы решений.")
        if total_Z > 20:
            recommendations.append("Высокая суммарная цикломатическая сложность. Нужны дополнительные тесты/разбиение кода.")

        if recommendations:
            self.results_text.insert("end", "Рекомендации:\n")
            for r in recommendations:
                self.results_text.insert("end", "- " + r + "\n")
        else:
            self.results_text.insert("end", "Рекомендаций не требуется (проверить вручную при необходимости).\n")

    def run(self):
        self.root.mainloop()


def main():
    app = GilbMcCabeAnalyzerGUI()
    app.run()


if __name__ == "__main__":
    main()