import ast
import pickle
from typing import Tuple, Iterable


class MCCChecker:
    """
    A flake8 plugin to make sure complex conditional expressions and comprehension expressions are split over several
    lines.
    """

    name = "flake8-multiline-conditionals-comprehensions"
    version = "1.0"

    def __init__(self, tree: ast.AST, *args, **kwargs):
        self.tree = tree
        with open("ast.pickle", "wb") as file:
            pickle.dump(tree, file)

    def run(self) -> Iterable[Tuple[int, int, str, type]]:
        yield (
            1,
            1,
            "C2023 asdasd!!",
            type(self),
        )
