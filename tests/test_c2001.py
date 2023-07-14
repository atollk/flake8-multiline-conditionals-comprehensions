from tests.util import BaseTest


class Test_MCC201(BaseTest):
    def error_code(self) -> str:
        return "MCC201"

    def test_pass_1(self):
        code = """
        foo = [x for x in range(10) for y in range(3) if x != 0]
        """
        result = self.run_flake8(code, True)
        assert result == []

    def test_pass_2(self):
        code = """
        foo = (x
               for x in range(10)
               for y in range(3)
               if x != 0)
        """
        result = self.run_flake8(code, True)
        assert result == []

    def test_fail_1(self):
        code = """
        foo = {x for x in range(10) for y in range(3)
               if x != 0}
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "MCC201", 2, 8)

    def test_fail_2(self):
        code = """
        foo = {x: y for x in range(10)
               for y in range(3) if x != 0}
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "MCC201", 2, 8)

    def test_fail_3(self):
        code = """
        foo = [x
               for x in range(10) for y in range(3) if x != 0]
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "MCC201", 3, 31)

    def test_fail_4(self):
        code = """
        foo = [x
               for x in range(10) for y in range(3)
               if x != 0]
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "MCC201", 3, 31)

    def test_fail_5(self):
        code = """
        foo = (x for x in range(10) for y in range(3) if (x !=
               0))
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "MCC201", 2, 8)

    def test_fail_6(self):
        code = """
        foo = [x for x in range(10) for
               y in range(3) if x != 0]
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "MCC201", 2, 8)

    def test_fail_7(self):
        code = """
        foo = [x for x in range(10) for y
               in range(3) if x != 0]
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "MCC201", 2, 8)

    def test_fail_8(self):
        code = """
        foo = [x for x in range(10) for y in
               range(3) if x != 0]
        """
        result = self.run_flake8(code, True)
        self.assert_error_at(result, "MCC201", 2, 8)
