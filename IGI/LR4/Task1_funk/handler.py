from abc import ABC, abstractmethod
import csv
import pickle
from pathlib import Path
from typing import List
from Task1_funk.item import Tree

class TreeRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Tree]:
        raise NotImplementedError

    @abstractmethod
    def save_all(self, trees: List[Tree]) -> None:
        raise NotImplementedError


class CsvTreeRepository(TreeRepository):
    def __init__(self, filename: str = "forest.csv"):
        self.filename = Path(filename)
        self._ensure_file()

    def _ensure_file(self) -> None:
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        if not self.filename.exists():
            with self.filename.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["name", "count_tree", "healthy"])
                writer.writeheader()

    def get_all(self) -> List[Tree]:
        self._ensure_file()
        trees: List[Tree] = []

        try:
            with self.filename.open("r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if not row:
                        continue
                    trees.append(
                        Tree(
                            name=row["name"],
                            count=int(row["count_tree"]),
                            healthy=int(row["healthy"]),
                        )
                    )
        except (FileNotFoundError, KeyError, ValueError):
            return []

        return trees

    def save_all(self, trees: List[Tree]) -> None:
        self._ensure_file()
        with self.filename.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "count_tree", "healthy"])
            writer.writeheader()
            for tree in trees:
                writer.writerow(
                    {
                        "name": tree.name,
                        "count_tree": tree.count,
                        "healthy": tree.healthy,
                    }
                )

class PickleTreeRepository(TreeRepository):
    def __init__(self, filename: str = "forest.pkl"):
        self.filename = Path(filename)
        self._ensure_file()

    def _ensure_file(self) -> None:
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        if not self.filename.exists():
            with self.filename.open("wb") as f:
                pickle.dump([], f)

    def get_all(self) -> List[Tree]:
        self._ensure_file()

        try:
            with self.filename.open("rb") as f:
                data = pickle.load(f)
                if isinstance(data, list):
                    return data
                return []
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            with self.filename.open("wb") as f:
                pickle.dump([], f)
            return []

    def save_all(self, trees: List[Tree]) -> None:
        self._ensure_file()
        with self.filename.open("wb") as f:
            pickle.dump(trees, f)