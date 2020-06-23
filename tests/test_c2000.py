import pytest

from flake8_multiline_conditionals_comprehensions.mcc_checker import PYTHON_38
from tests.util import BaseTest


class Test_C2000(BaseTest):
    def error_code(self) -> str:
        return "C2000"

    def test_pass_1(self):
        code = """
        foo = [x for x in range(10)
               for y in range(3)]
        """
        result = self.run_flake8(code, True)
        assert result == []

    def test_fail_1(self):
        code = """
        foo = [x for x in range(10) for y in range(3)]
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "C2000", 1, 7 if PYTHON_38 else 8)

    @pytest.mark.skip("TODO this probably needs Token parsing")
    def test_fail_2(self):
        code = """
        foo = (x for x in range(10) for
               y in range(3))
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "C2000", 1, 7)

    def test_fail_3(self):
        code = """
        foo = {x for x in range(10) for y
               in range(3)}
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "C2000", 1, 7)

    def test_fail_4(self):
        code = """
        foo = {x: y for x in range(10) for y in
               range(3)}
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "C2000", 1, 7)

    def test_fail_5(self):
        code = """
        foo = [x for x in range(10) for y in range(3)
               ]
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "C2000", 1, 7 if PYTHON_38 else 8)

    def test_fail_6(self):
        code = """
        foo = [x for x in
               range(10) for y in range(3)]
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "C2000", 1, 7 if PYTHON_38 else 8)
