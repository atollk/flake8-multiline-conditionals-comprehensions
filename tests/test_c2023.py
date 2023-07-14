from tests.util import BaseTest


class Test_MCC223(BaseTest):
    def error_code(self) -> str:
        return "MCC223"

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
        self.assert_error_at(result, "MCC223", 2, 8)

    def test_fail_2(self):
        code = """
        foo = (1
               if True
               else 0)
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "MCC223", 2, 8)
