class Forest():
    def __init__(self):
        self._dictionary_tree = {}
    @property
    def get_dictionary_tree(self):
        return self._dictionary_tree
    
    @staticmethod
    def get_column_tree():
        return ["name", "count_tree", "healthy"]
    
    def add_tree(self, name, count_tree, healthy):
        new_tree = [count_tree, healthy]
        self._dictionary_tree[name] = new_tree
    
    def remove(self, name):
        self._dictionary_tree.pop(name)
