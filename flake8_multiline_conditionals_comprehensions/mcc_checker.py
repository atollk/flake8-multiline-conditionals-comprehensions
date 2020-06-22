import argparse
import ast
import itertools
import tokenize
from typing import Tuple, Iterable, Union, List

import flake8.options.manager

ComprehensionType = Union[ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp]

DEFAULT_SELECT = [
    "C2000",
    "C2001",
    "C2002",
    "C2020",
    "C2021",
    "C2023",
]


class MCCChecker:
    """
    A flake8 plugin to make sure complex conditional expressions and comprehension expressions are split over several
    lines.
    """

    name = "flake8-multiline-conditionals-comprehensions"
    version = "1.0"
    enabled_errors = None

    def __init__(self, tree: ast.AST, file_tokens: List[tokenize.TokenInfo]):
        self.tree = tree
        self.tokens = file_tokens

    @staticmethod
    def add_options(option_manager: flake8.options.manager.OptionManager):
        option_manager.add_option('--select_c20', type=str, comma_separated_list=True, default=DEFAULT_SELECT,
                                  parse_from_config=True, help="Error types to use. Default: %(default)s")

    @staticmethod
    def parse_options(option_manager: flake8.options.manager.OptionManager, options: argparse.Namespace, extra_args):
        MCCChecker.enabled_errors = [int(option[1:]) for option in options.select_c20]

    def _get_tokens_with_surrounding(self, node: ast.AST, margin: int) -> Iterable[tokenize.TokenInfo]:
        start_index, end_index = None, None
        for i, token in enumerate(self.tokens):
            token_line, token_col = token.start
            if (token_line > node.lineno or (token_line == node.lineno and token_col >= node.col_offset)) and (
                    token_line < node.end_lineno or (
                    token_line == node.end_lineno and token_col <= node.end_col_offset)):
                if start_index is None:
                    start_index = i
            else:
                if end_index is None and start_index is not None:
                    end_index = i
                    break
        return self.tokens[start_index - margin:end_index + margin]

    def run(self) -> Iterable[Tuple[int, int, str, type]]:
        for node in ast.walk(self.tree):
            if any(isinstance(node, comp) for comp in [ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp]):
                if 2000 in MCCChecker.enabled_errors:
                    yield from _c2000(node)
                if 2001 in MCCChecker.enabled_errors:
                    yield from _c2001(node)
                if 2002 in MCCChecker.enabled_errors:
                    yield from _c2002(node)
                if 2003 in MCCChecker.enabled_errors:
                    yield from _c2003(node)
                if 2004 in MCCChecker.enabled_errors:
                    yield from _c2004(node)

            if isinstance(node, ast.Assign) and isinstance(node.value, ast.IfExp):
                if 2021 in MCCChecker.enabled_errors:
                    yield from _c2021(node, list(self._get_tokens_with_surrounding(node.value, 1)))

            if isinstance(node, ast.IfExp):
                if 2020 in MCCChecker.enabled_errors:
                    yield from _c2020(node)
                if 2022 in MCCChecker.enabled_errors:
                    yield from _c2022(node)
                if 2023 in MCCChecker.enabled_errors:
                    yield from _c2023(node)
                if 2024 in MCCChecker.enabled_errors:
                    yield from _c2024(node)
                if 2025 in MCCChecker.enabled_errors:
                    yield from _c2025(node)


ERROR_MESSAGES = {
    2000: "Generators in comprehension expression are on the same line.",
    2001: "Different segments of a comprehension expression share a line.",
    2002: "Multiple filter segments within a single comprehension expression.",
    2003: "Multiline comprehension expression are forbidden.",
    2004: "Singleline comprehension expression are forbidden.",
    2020: "Different segments of a conditional expression share a line.",
    2021: "Conditional expression used for assignment not surrounded by parantheses.",
    2022: "Nested conditional expressions are forbidden.",
    2023: "Multiline conditional expression are forbidden.",
    2024: "Singleline conditional expression are forbidden.",
    2025: "Conditional expressions are forbidden.",
}


def _error_tuple(error_code: int, node: ast.AST) -> Tuple[int, int, str, type]:
    return node.lineno, node.col_offset, f"C{error_code} {ERROR_MESSAGES[error_code]}", MCCChecker


def _c2000(node: ComprehensionType) -> Iterable[Tuple[int, int, str, type]]:
    """
    A comprehension expression should place each of its generators on a separate line.
    """
    for generator1, generator2 in itertools.combinations(node.generators, 2):
        if (generator1.target.lineno <= generator2.target.lineno <= generator1.iter.end_lineno or
                generator2.target.lineno <= generator1.target.lineno <= generator2.iter.end_lineno):
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
            yield _error_tuple(2001, node.key)
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
    if node.lineno == node.end_lineno:
        return ()  # single line expression

    if len({node.body.lineno, node.test.lineno, node.orelse.lineno}) < 3:
        yield _error_tuple(2020, node)


def _c2021(node: ast.Assign, tokens: List[tokenize.TokenInfo]) -> Iterable[Tuple[int, int, str, type]]:
    """
    A conditional expression used for assignment must be surrounded by parantheses.
    """
    if tokens[0].type != tokenize.OP or "(" not in tokens[0].string:
        yield _error_tuple(2021, node)


def _c2022(node: ast.IfExp) -> Iterable[Tuple[int, int, str, type]]:
    """
    A conditional expression should not contain further conditional expressions.
    """
    for ancestor in itertools.chain(ast.walk(node.body), ast.walk(node.test), ast.walk(node.orelse)):
        if isinstance(ancestor, ast.IfExp):
            yield _error_tuple(2022, ancestor)


def _c2023(node: ast.IfExp) -> Iterable[Tuple[int, int, str, type]]:
    """
    A conditional expression should not span over multiple lines.
    """
    if node.lineno != node.end_lineno:
        yield _error_tuple(2023, node)


def _c2024(node: ast.IfExp) -> Iterable[Tuple[int, int, str, type]]:
    """
    A conditional expression should span over multiple lines.
    """
    if node.lineno == node.end_lineno:
        yield _error_tuple(2024, node)


def _c2025(node: ast.IfExp) -> Iterable[Tuple[int, int, str, type]]:
    """
    Conditional expressions should not be used.
    """
    yield _error_tuple(2025, node)
