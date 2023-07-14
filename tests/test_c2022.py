from tests.util import BaseTest


class Test_MCC222(BaseTest):
    def error_code(self) -> str:
        return "MCC222"

    def test_pass_1(self):
        code = """
        foo = (1 if 10 < 20 else 0)
        """
        result = self.run_flake8(code, True)
        assert result == []

    def test_pass_2(self):
        code = """
        if 0 == 0:
            print(0)
        else:
            print(1 if True else 2)
        """
        result = self.run_flake8(code, True)
        assert result == []

    def test_fail_1(self):
        code = """
        foo = (1 if 1 > 0 else -1 if 1 < 0 else 0)
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "MCC222", 2, 24)

    def test_fail_2(self):
        code = """
        foo = (1 if (1 if True else 2) > 0 else -1)
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "MCC222", 2, 14)
