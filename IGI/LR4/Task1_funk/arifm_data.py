from typing import List, Optional
from Task1_funk.item import Tree
from Task1_funk.handler import TreeRepository


class TreeService:
    def __init__(self, repo: TreeRepository):
        self.repo = repo

    def get_all(self) -> List[Tree]:
        return self.repo.get_all()

    def add(self, tree: Tree) -> None:
        trees = self.repo.get_all()
        trees.append(tree)
        self.repo.save_all(trees)

    def remove(self, name: str) -> None:
        trees = self.repo.get_all()
        trees = [t for t in trees if t.name != name]
        self.repo.save_all(trees)

    def find(self, name: str) -> Optional[Tree]:
        return next((t for t in self.repo.get_all() if t.name == name), None)

    def sort_by_count(self, reverse: bool = True) -> List[Tree]:
        return sorted(self.repo.get_all(), key=lambda t: t.count, reverse=reverse)

    def total_count(self) -> int:
        return sum(t.count for t in self.repo.get_all())

    def total_healthy(self) -> int:
        return sum(t.healthy for t in self.repo.get_all())

    def total_unhealthy(self) -> int:
        return sum(t.unhealthy for t in self.repo.get_all())

    def percent_by_type(self):
        trees = self.repo.get_all()
        total = self.total_count()
        if total == 0:
            return []
        return [(t.name, t.count * 100 / total) for t in trees]

    def percent_unhealthy_by_type(self):
        return [(t.name, t.percent_unhealthy) for t in self.repo.get_all()]