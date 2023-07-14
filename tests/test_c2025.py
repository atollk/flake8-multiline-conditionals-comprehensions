from tests.util import BaseTest


class Test_MCC225(BaseTest):
    def error_code(self) -> str:
        return "MCC225"

    def test_fail_1(self):
        code = """
        foo = (1 if True
               else 0)
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "MCC225", 1, 8)

    def test_fail_2(self):
        code = """
        foo = (1
               if True
               else 0)
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "MCC225", 1, 8)

    def test_fail_3(self):
        code = """
        foo = (1 if True else 0)
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "MCC225", 1, 8)
