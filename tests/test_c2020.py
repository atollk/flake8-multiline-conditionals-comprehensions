from tests.util import BaseTest


class Test_C2020(BaseTest):
    def error_code(self) -> str:
        return "C2020"

    def test_pass_1(self):
        code = """
        foo = 1 if 10 < 20 else 0
        """
        result = self.run_flake8(code, True)
        assert result == []

    def test_pass_2(self):
        code = """
        foo = (1
               if True
               else 0)
        """
        result = self.run_flake8(code, True)
        assert result == []

    def test_fail_1(self):
        code = """
        foo = (1 if 10 < 20 else 
               0)
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "C2020", 1, 8)

    def test_fail_2(self):
        code = """
        foo = (1 if 10 < 20
               else 0)
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "C2020", 1, 8)

    def test_fail_3(self):
        code = """
        foo = (1 if (10 <
               20) else 0)
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "C2020", 1, 8)

    def test_fail_4(self):
        code = """
        foo = (1 if
               10 < 20 else 0)
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "C2020", 1, 8)

    def test_fail_5(self):
        code = """
        foo = (1
               if 10 < 20 else 0)
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "C2020", 1, 8)
