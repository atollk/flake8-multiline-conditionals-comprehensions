from tests.util import BaseTest


class Test_C2022(BaseTest):
    def error_code(self) -> str:
        return "C2022"

    def test_pass_1(self):
        code = """
        foo = (1 if 10 < 20 else 0)
        """
        result = self.run_flake8(code, True)
        assert result == []

    def test_pass_2(self):
        code = """
        if x > 0:
            return 1
        elif x < 0:
            return -1
        else:
            return 0
        """
        result = self.run_flake8(code, True)
        assert result == []

    def test_fail_1(self):
        code = """
        foo = (1 if x > 0 else -1 if x < 0 else 0)
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "C2022", 1, 8)

    def test_fail_2(self):
        code = """
        foo = (1 if (x if True else y) > 0 else -1)
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "C2022", 1, 8)
