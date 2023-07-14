from tests.util import BaseTest


class Test_MCC202(BaseTest):
    def error_code(self) -> str:
        return "MCC202"

    def test_pass_1(self):
        code = """
        foo = [x for x in range(10) for y in range(3) if x != 0]
        """
        result = self.run_flake8(code, True)
        assert result == []

    def test_pass_2(self):
        code = """
        foo = {x for x in range(10)}
        """
        result = self.run_flake8(code, True)
        assert result == []

    def test_fail_1(self):
        code = """
        foo = {x for x in range(10) for y in range(3)
               if x != 0 if y != 0}
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "MCC202", 3, 21)

    def test_fail_2(self):
        code = """
        foo = {x: y
               for x in range(10)
               for y in range(3)
               if x != 0
               if y != 0}
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "MCC202", 6, 11)

    def test_fail_3(self):
        code = """
        foo = {x: y
               for x in range(10)
               if x != 0
               for y in range(3)
               if y != 0}
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "MCC202", 6, 11)
