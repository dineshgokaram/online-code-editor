# test_lint.py (optional)
def test_linting():
    result = os.system("ruff .")
    assert result == 0