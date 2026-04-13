from Task1.
import pickle
'''
Исходные данные представляют собой словарь.
Необходимо поместить их в файл, используя сериализатор.
Организовать считывание данных, поиск, сортировку в соответствии
с индивидуальным заданием.
Обязательно использовать классы.
Реализуйте два варианта: 1)формат файлов CSV; 2)модуль pickle

Хранятся сведения о лесе:
    вид дерева, общая численность, численность здоровых деревьев.

Составьте программу вычисления:
    1) суммарного числа деревьев на контрольном участке;
    2) суммарного числа здоровых деревьев;
    3) относительную численность (%) больных деревьев;
    4) относительную численность (%) различных видов,
    в том числе больных (%) для каждого вида.

Выведите информацию о виде дерева, введенном с клавиатуры'''

class Menu:
    def __init__(self):
        self.core = Core_Task1()
        self.handler = HandlerFile()

    def show(self):
        while True:
            print("""
==== Forest Menu ====
1 - Показать все виды деревьев
2 - Общая статистика
3 - Найти дерево по названию
4 - Добавить запись
5 - Удалить запись
6 - Сортировка по количеству деревьев
7 - Сохранить в CSV
8 - Сохранить в pickle
9 - Загрузить из pickle
0 - Выход
""")
            try:
                choice = int(input("Выбор: "))
            except ValueError:
                print("Ошибка ввода")
                continue

            if choice == 0:
                print("Выход.")
                break

            elif choice == 1:
                self.core.read_file()
                print(self.core.all_type_tree())

            elif choice == 2:
                self.core.read_file()
                print("Всего деревьев:", self.core.number_of_alls_tree())
                print("Здоровых:", self.core.number_of_healthy_tree())
                print("Больных:", self.core.number_of_unhealthy_tree())
                print("Процент по видам:", self.core.percent_of_alls_tree())
                print("Процент больных:", self.core.percent_of_unhealthy_tree())

            elif choice == 3:
                name = input("Введите название: ")
                self.core.read_file()
                print(self.core.informatiom_tree(name))

            elif choice == 4:
                name = input("Название: ")
                count = int(input("Количество: "))
                healthy = int(input("Здоровые: "))

                data = self.handler.csv_read_file()
                data.append({
                    "name": name,
                    "count_tree": count,
                    "healthy": healthy
                })

                self.handler.csv_write_file(data)
                print("Добавлено.")

            elif choice == 5:
                name = input("Удалить название: ")

                data = self.handler.csv_read_file()
                data = [row for row in data if row["name"] != name]

                self.handler.csv_write_file(data)
                print("Удалено.")

            elif choice == 6:
                data = self.handler.csv_read_file()

                data.sort(key=lambda x: int(x["count_tree"]), reverse=True)

                for row in data:
                    print(row)

            elif choice == 7:
                print("CSV уже используется как основной формат.")

            elif choice == 8:
                data = self.handler.csv_read_file()

                with open("forest.pkl", "wb") as f:
                    pickle.dump(data, f)

                print("Сохранено в pickle.")

            elif choice == 9:
                with open("forest.pkl", "rb") as f:
                    data = pickle.load(f)

                self.handler.csv_write_file(data)
                print("Загружено из pickle.")

if __name__ == "__main__":
    menu = Menu()
    menu.show()