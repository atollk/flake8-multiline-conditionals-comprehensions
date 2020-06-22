import ast
import itertools
import pickle
from typing import Tuple, Iterable, Union

ComprehensionType = Union[ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp]


class MCCChecker:
    """
    A flake8 plugin to make sure complex conditional expressions and comprehension expressions are split over several
    lines.
    """

    name = "flake8-multiline-conditionals-comprehensions"
    version = "1.0"

    def __init__(self, tree: ast.AST, file_tokens):
        self.tree = tree
        self.tokens = file_tokens
        with open("ast.pickle", "wb") as file:
            pickle.dump(self.tokens, file)

    def run(self) -> Iterable[Tuple[int, int, str, type]]:
        for node in ast.walk(self.tree):
            if any(isinstance(node, comp) for comp in [ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp]):
                yield from _c2000(node)
                yield from _c2001(node)
                yield from _c2002(node)
                yield from _c2003(node)
                yield from _c2004(node)

            if isinstance(node, ast.Assign):
                pass

            if isinstance(node, ast.IfExp):
                pass


def _error_tuple(error_code: int, node: ast.AST) -> Tuple[int, int, str, type]:
    return node.lineno, node.col_offset, f"C{error_code} error message", MCCChecker


def _c2000(node: ComprehensionType) -> Iterable[Tuple[int, int, str, type]]:
    """
    A comprehension expression should place each of its generators on a separate line.
    """
    violates = any(
        generator1.target.lineno == generator2.target.lineno
        for generator1, generator2 in itertools.combinations(node.generators, 2)
    )
    if violates:
        yield _error_tuple(2000, node)


def _c2001(node: ComprehensionType) -> Iterable[Tuple[int, int, str, type]]:
    """
    A multiline comprehension expression should place each of its segments (map, generator, filter) on a separate line.
    """
    if node.lineno == node.end_lineno:
        return ()  # single line comprehension

    seen_line_nos = set()

    for generator in node.generators:
        if generator.target.lineno in seen_line_nos:
            yield _error_tuple(2001, generator.target)
        seen_line_nos.add(generator.target.lineno)

        for if_clause in generator.ifs:
            if if_clause.lineno in seen_line_nos:
                yield _error_tuple(2001, if_clause)
            seen_line_nos.add(if_clause.lineno)

    if isinstance(node, ast.DictComp):
        if node.value.lineno in seen_line_nos:
            yield _error_tuple(2001, node.value)
        seen_line_nos.add(node.value.lineno)
    else:
        if node.elt.lineno in seen_line_nos:
            yield _error_tuple(2001, node.elt)
        seen_line_nos.add(node.elt.lineno)


def _c2002(node: ComprehensionType) -> Iterable[Tuple[int, int, str, type]]:
    """
    A comprehension expression should not contain multiple filters.
    """
    ifs_seen = 0
    for generator in node.generators:
        for if_clause in generator.ifs:
            ifs_seen += 1
            if ifs_seen > 1:
                yield _error_tuple(2002, if_clause)


def _c2003(node: ComprehensionType) -> Iterable[Tuple[int, int, str, type]]:
    """
    A comprehension expression should not span over multiple lines.
    """
    if node.lineno != node.end_lineno:
        yield _error_tuple(2003, node)


def _c2004(node: ComprehensionType) -> Iterable[Tuple[int, int, str, type]]:
    """
    A comprehension expression should span over multiple lines.
    """
    if node.lineno == node.end_lineno:
        yield _error_tuple(2004, node)


def _c2020(node: ast.IfExp) -> Iterable[Tuple[int, int, str, type]]:
    """
    A multiline conditional expression should place each of its segments on a separate line.
    """


def _c2021(node: ast.Assign) -> Iterable[Tuple[int, int, str, type]]:
    """
    A conditional expression used for assignment must be surrounded by parantheses.
    """


def _c2022(node: ast.IfExp) -> Iterable[Tuple[int, int, str, type]]:
    """
    A multiline conditional expression should place each of its segments on a separate line.
    """


def _c2023(node: ast.IfExp) -> Iterable[Tuple[int, int, str, type]]:
    """
    A conditional expression should not span over multiple lines.
    """


def _c2024(node: ast.IfExp) -> Iterable[Tuple[int, int, str, type]]:
    """
    A conditional expression should span over multiple lines.
    """


def _c2025(node: ast.IfExp) -> Iterable[Tuple[int, int, str, type]]:
    """
    Conditional expressions should not be used.
    """
