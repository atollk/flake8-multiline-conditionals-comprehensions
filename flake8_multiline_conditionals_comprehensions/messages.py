import ast
import itertools
from typing import Union

ComprehensionType = Union[ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp]


def violates_c2000(comprehension: ComprehensionType) -> bool:
    return any(
        generator1.target.lineno == generator2.target.lineno
        for generator1, generator2 in itertools.combinations(comprehension.generators, 2)
    )
