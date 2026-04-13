from handler import HandlerFile
from item import Forest

class Core_Task1:
    def __init__(self):
        self._handler = HandlerFile()
        self._data = self._handler.csv_read_file()

        columns = list(Forest.get_column_tree())
        self._name_col = columns[0]
        self._count_col = columns[1]
        self._healthy_col = columns[2]

    def _to_int(self, value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0
        
    def read_file(self):
        self._data = self._handler.csv_read_file()

    # --- базовые агрегаты ---

    def number_of_alls_tree(self):
        return sum(self._to_int(row.get(self._count_col)) for row in self._data)

    def number_of_healthy_tree(self):
        return sum(self._to_int(row.get(self._healthy_col)) for row in self._data)

    def number_of_unhealthy_tree(self):
        return sum(
            self._to_int(row.get(self._count_col)) -
            self._to_int(row.get(self._healthy_col))
            for row in self._data
        )

    # --- проценты ---

    def percent_of_alls_tree(self):
        total = self.number_of_alls_tree()
        if total == 0:
            return []

        return [
            self._to_int(row.get(self._count_col)) * 100 / total
            for row in self._data
        ]

    def percent_of_unhealthy_tree(self):
        total = self.number_of_unhealthy_tree()
        if total == 0:
            return []

        return [
            (
                self._to_int(row.get(self._count_col)) -
                self._to_int(row.get(self._healthy_col))
            ) * 100 / total
            for row in self._data
        ]

    # --- выборки ---

    def all_type_tree(self):
        return [row.get(self._name_col) for row in self._data]

    def informatiom_tree(self, input_name: str):
        return next(
            (row for row in self._data if row.get(self._name_col) == input_name),
            None
        )
    
a = Core_Task1()
print(a.all_type_tree())
print(a.percent_of_alls_tree())