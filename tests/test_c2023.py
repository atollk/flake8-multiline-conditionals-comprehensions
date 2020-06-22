from tests.util import BaseTest


class Test_C2023(BaseTest):
    def error_code(self) -> str:
        return "C2023"

    def test_pass_1(self):
        code = """
        foo = (1 if True else 0)
        """
        result = self.run_flake8(code, True)
        assert result == []

    def test_fail_1(self):
        code = """
        foo = (1 if True
               else 0)
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "C2023", 1, 7)

    def test_fail_2(self):
        code = """
        foo = (1
               if True
               else 0)
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "C2023", 1, 7)
