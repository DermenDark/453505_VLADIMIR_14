import pickle, csv
from item import Forest

class HandlerFile():
    def __init__(self):
        self._my_tree_data = Forest()
        self._my_tree_data.add_tree("липа", 10000, 200)
        self._my_tree_data.add_tree("липа2", 20000, 200)
        self.pi_name_file = "Default"
        self.csv_name_file = "Default.csv"

    def pi_read_file(self):
        with open(self.pi_name_file,"rb") as fh:
            data = pickle.load(fh)
            print(data)
        return data

    def pi_write_file(self):
        with open(self.pi_name_file,"wb") as fh:
            pickle.dump(self._my_tree_data.get_dictionary_tree, fh)

    def csv_read_file(self):
        new_list = []
        with open(self.csv_name_file, "r", newline="", encoding="utf-8") as fh:
            data = csv.DictReader(fh)
            for row in data:
                new_list.append(row)
        return new_list

    def csv_write_file(self, write_data: list):
        fieldnames = self._my_tree_data.get_column_tree()
        with open(self.csv_name_file, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames = fieldnames, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerows(write_data)

# a = HandlerFile()

# data = a.csv_read_file()
# print(data)

# a.csv_write_file(data)
# print(data)