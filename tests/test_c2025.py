from tests.util import BaseTest


class Test_C2025(BaseTest):
    def error_code(self) -> str:
        return "C2025"

    def test_fail_1(self):
        code = """
        foo = (1 if True
               else 0)
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "C2025", 1, 7)

    def test_fail_2(self):
        code = """
        foo = (1
               if True
               else 0)
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "C2025", 1, 7)

    def test_fail_3(self):
        code = """
        foo = (1 if True else 0)
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "C2025", 1, 7)
