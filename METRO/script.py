import customtkinter as ctk
from tkinter import filedialog, messagebox
import re
import math
import os
from tabulate import tabulate 

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class HalsteadMetricsAnalyzer:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Анализатор метрик Холстеда для Python")
        self.root.geometry("1200x800")
        
        self.current_file_path = ctk.StringVar(value="")
        
        self.create_widgets()
        
    def create_widgets(self):
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            self.main_container, 
            text="Анализатор метрик Холстеда",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=10)
        
        file_frame = ctk.CTkFrame(self.main_container)
        file_frame.pack(fill="x", padx=20, pady=10)
        
        self.file_path_label = ctk.CTkLabel(
            file_frame,
            textvariable=self.current_file_path,
            font=ctk.CTkFont(size=12),
            wraplength=600,
            text_color="gray"
        )
        self.file_path_label.pack(side="left", padx=10, expand=True, fill="x")
        
        self.select_file_btn = ctk.CTkButton(
            file_frame,
            text="Выбрать файл",
            command=self.select_file,
            width=150,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.select_file_btn.pack(side="right", padx=10)
        
        self.tabview = ctk.CTkTabview(self.main_container)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.tabview.add("Код программы")
        self.code_tab = self.tabview.tab("Код программы")
        
        self.code_text = ctk.CTkTextbox(
            self.code_tab,
            font=ctk.CTkFont(family="Courier New", size=12),
            wrap="none"
        )
        self.code_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.code_text.configure(scrollbar_button_color="gray")
        
        self.tabview.add("Результаты анализа")
        self.results_tab = self.tabview.tab("Результаты анализа")
        
        self.results_text = ctk.CTkTextbox(
            self.results_tab,
            font=ctk.CTkFont(family="Courier New", size=12)
        )
        self.results_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        button_frame = ctk.CTkFrame(self.main_container)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        self.analyze_btn = ctk.CTkButton(
            button_frame,
            text="Анализировать код",
            command=self.analyze_code,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#28a745",
            hover_color="#218838"
        )
        self.analyze_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        self.load_example_btn = ctk.CTkButton(
            button_frame,
            text="Загрузить пример",
            command=self.load_example_code,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#17a2b8",
            hover_color="#138496"
        )
        self.load_example_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        self.clear_btn = ctk.CTkButton(
            button_frame,
            text="Очистить",
            command=self.clear_all,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        self.clear_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        self.status_bar = ctk.CTkLabel(
            self.main_container,
            text="Готов к работе",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.status_bar.pack(side="bottom", fill="x", pady=5)
        
        self.load_example_code()
        
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Выберите Python файл",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        
        if file_path:
            self.current_file_path.set(f"Файл: {os.path.basename(file_path)}")
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    code = file.read()
                self.code_text.delete("1.0", "end")
                self.code_text.insert("1.0", code)
                self.update_status(f"Загружен файл: {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")
                self.current_file_path.set("")
    
    def get_example_code(self):
        return '''def calculate_fibonacci(n):
    """Вычисление чисел Фибоначчи рекурсивно и итеративно"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    def fib_recursive(k):
        if k <= 1:
            return k
        elif k == 2:
            return 1
        else:
            return fib_recursive(k-1) + fib_recursive(k-2)
    
    fib_iterative = [0, 1]
    for i in range(2, n):
        fib_iterative.append(fib_iterative[i-1] + fib_iterative[i-2])
    
    fib_recursive_list = []
    for i in range(n):
        fib_recursive_list.append(fib_recursive(i))
    
    fib_recursive_list.sort()
    assert fib_recursive_list == fib_iterative, "Результаты не совпадают!"
    
    return fib_iterative

def main():
    try:
        num = int(input("Введите количество чисел Фибоначчи: "))
        if num < 0:
            raise ValueError("Число должно быть неотрицательным")
        elif num == 0:
            print("Пустой список")
        else:
            result = calculate_fibonacci(num)
            print(f"Первые {num} чисел Фибоначчи:")
            print(result)
        
        sum_fib = 0
        sum_fib = (5 + 3) * 2
        product_fib = 1
        for value in result:
            sum_fib += value
            if value > 0:
                product_fib *= value
        
        print(f"Сумма: {sum_fib}")
        print(f"Произведение (исключая нули): {product_fib}")
        
    except ValueError as e:
        print(f"Ошибка ввода: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")

if __name__ == "__main__":
    main()'''
    
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
    
    def update_status(self, message):
        self.status_bar.configure(text=message)
    
    def analyze_code(self):
        code = self.code_text.get("1.0", "end").strip()
        if not code:
            messagebox.showwarning("Предупреждение", "Введите код для анализа!")
            return
        
        try:
            compile(code, '<string>', 'exec')
            
            self.update_status("Анализ кода...")
            metrics = self.calculate_halstead_metrics(code)
            self.display_results(metrics)
            self.update_status("Анализ завершен успешно")
            
        except SyntaxError as e:
            messagebox.showerror("Ошибка синтаксиса", f"Ошибка в коде: {e}")
            self.update_status("Ошибка синтаксиса")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при анализе: {e}")
            self.update_status("Ошибка при анализе")
    
    def calculate_halstead_metrics(self, code):
        operators = {
            '+', '-', '*', '/', '//', '%', '**',
            '==', '!=', '<', '>', '<=', '>=',
            'and', 'or', 'not',
            '&', '|', '^', '~', '<<', '>>',
            '=', '+=', '-=', '*=', '/=', '//=', '%=', '**=', 
            '&=', '|=', '^=', '<<=', '>>=',
            'in', 'is', 'is not', 'not in',
            ':', ';', ',', '.',
            'if/elif', 'else', 'for', 'while', 'break', 'continue', 'return',
            'def', 'class', 'try', 'except', 'finally', 'raise', 'with', 'as',
            'import', 'from', 'lambda', 'yield', 'assert', 'del', 'global', 'nonlocal',
            'pass', 'async', 'await', 'print',
            '@', '->', '...'
        }
        
        function_keywords = {'def', 'class', 'lambda'}
        math_brackets = {'(', ')', '[', ']', '{', '}'}
        
        tokens = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            if line.strip().startswith('#'):
                continue
            
            prev_line = lines[i-1] if i > 0 else ""
            next_line = lines[i+1] if i < len(lines)-1 else ""
            
            line_tokens = re.findall(
                r'[a-zA-Z_][a-zA-Z0-9_]*|\.\.\.|<<=|>>=|[<>!=]=|[-+*/%&|^~<>]=|[-+*/%&|^~<>]|[(){}\[\].,:;=]|".*?"|\'.*?\'|\d+\.?\d*|#.*$',
                line
            )
            
            for j, token in enumerate(line_tokens):
                if token.startswith('#'):
                    break
                
                if token == 'if' or token == 'elif':
                    token = 'if/elif'
                
                is_math_context = False
                if token in math_brackets:
                    prev_token = line_tokens[j-1] if j > 0 else ""
                    next_token = line_tokens[j+1] if j < len(line_tokens)-1 else ""
                    
                    if (prev_token in {'+', '-', '*', '/', '=', '=='} or 
                        next_token in {'+', '-', '*', '/', '=', '=='} or
                        '=' in line or '+' in line or '-' in line or '*' in line or '/' in line):
                        is_math_context = True
                
                if token.startswith(('"', "'")):
                    tokens.append(('string', token))
                elif token.replace('.', '').isdigit():
                    tokens.append(('number', token))
                elif token in operators:
                    tokens.append(('operator', token))
                elif token in function_keywords:
                    tokens.append(('function_def', token))
                elif token in math_brackets and is_math_context:
                    tokens.append(('operator', '()'))
                else:
                    tokens.append(('operand', token))
        
        unique_operators = set()
        unique_operands = set()
        operator_count = 0
        operand_count = 0
        operator_freq = {}
        operand_freq = {}
        
        for token_type, token_value in tokens:
            if token_type == 'operator' or token_type == 'function_def':
                unique_operators.add(token_value)
                operator_count += 1
                operator_freq[token_value] = operator_freq.get(token_value, 0) + 1
            elif token_type == 'operand':
                unique_operands.add(token_value)
                operand_count += 1
                operand_freq[token_value] = operand_freq.get(token_value, 0) + 1
            elif token_type in ['string', 'number']:
                unique_operands.add(token_value)
                operand_count += 1
                operand_freq[token_value] = operand_freq.get(token_value, 0) + 1

        eta1 = len(unique_operators)
        eta2 = len(unique_operands)
        N1 = operator_count
        N2 = operand_count
        
        eta = eta1 + eta2
        N = N1 + N2
        
        if eta > 0:
            V = N * math.log2(eta)
        else:
            V = 0
        
        return {
            'eta1': eta1,
            'eta2': eta2,
            'N1': N1,
            'N2': N2,
            'operator_freq': operator_freq,
            'operand_freq': operand_freq,
            'eta': eta,
            'N': N,
            'V': V
        }
    
    def display_results(self, metrics):
        self.results_text.delete("1.0", "end")
        
        result_text = "="*100 + "\n"
        result_text += " " * 35 + "Результаты анализа метрик Холстеда\n"
        result_text += "="*100 + "\n\n"


        sorted_ops = sorted(metrics['operator_freq'].items(), key=lambda x: x[1], reverse=True)
        sorted_operands = sorted(metrics['operand_freq'].items(), key=lambda x: x[1], reverse=True)
        
        max_len = max(len(sorted_ops), len(sorted_operands))
        

        table_data = []
        for idx in range(max_len):
            row = []
            if idx < len(sorted_ops):
                row.extend([idx+1, sorted_ops[idx][0], sorted_ops[idx][1]])
            else:
                row.extend(["", "", ""])


            if idx < len(sorted_operands):
                row.extend([idx+1, sorted_operands[idx][0], sorted_operands[idx][1]])
            else:
                row.extend(["", "", ""])
            
            table_data.append(row)
        

        headers = ["№", "Оператор", "Частота", "№", "Операнд", "f1j/f2i"]
        

        table1 = tabulate(
            table_data, 
            headers=headers, 
            tablefmt="fancy_grid",  
            stralign="left",  
            numalign="center"  
        )
        
        result_text += "Таблица 1 - Базовые метрики (операторы и операнды)\n"
        result_text += table1 + "\n\n"
        

        summary_data = [[
            f"η1 = {metrics['eta1']}", 
            f"N1 = {metrics['N1']}",
            f"η2 = {metrics['eta2']}", 
            f"N2 = {metrics['N2']}"
        ]]
        
        summary_table = tabulate(
            summary_data,
            tablefmt="fancy_grid",
            stralign="center"
        )
        result_text += summary_table + "\n\n"
        

        extended_metrics = [
            ["Словарь программы", f"η = η1 + η2", f"{metrics['eta']:.0f}"],
            ["Длина программы", f"N = N1 + N2", f"{metrics['N']:.0f}"],
            ["Объем программы", "V = N * log₂(η)", f"{metrics['V']:.2f} бит"]
        ]
        
        table2 = tabulate(
            extended_metrics,
            headers=["Метрика", "Формула", "Значение"],
            tablefmt="fancy_grid",
            stralign="left",
            numalign="right"
        )
        
        result_text += "Таблица 2 - Расширенные метрики Холстеда\n"
        result_text += table2 + "\n"
        
        self.results_text.insert("1.0", result_text)
    
    def run(self):
        self.root.mainloop()

def main():
    app = HalsteadMetricsAnalyzer()
    app.run()

if __name__ == "__main__":
    main()