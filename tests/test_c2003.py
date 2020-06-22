from tests.util import BaseTest


class Test_C2003(BaseTest):
    def error_code(self) -> str:
        return "C2003"

    def test_pass_1(self):
        code = """
        foo = (x for x in range(10))
        """
        result = self.run_flake8(code, True)
        assert result == []

    def test_pass_2(self):
        code = """
        foo = {x: x for x in range(10) for y in range(3) if x != 0}
        """
        result = self.run_flake8(code, True)
        assert result == []

    def test_fail_1(self):
        code = """
        foo = {x for x in range(10) for y in range(3)
               if x != 0 if y != 0}
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "C2003", 1, 7)

    def test_fail_2(self):
        code = """
        foo = [x for x in range(
               3)]
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "C2003", 1, 7)
