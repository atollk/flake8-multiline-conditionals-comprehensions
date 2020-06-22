def test_C400_pass_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = [x + 1 for x in range(10)]
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []
