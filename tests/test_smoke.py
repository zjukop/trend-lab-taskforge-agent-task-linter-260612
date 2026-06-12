from taskforge.main import forge_spec, lint_task, main


def test_lint_task_returns_score():
    result = lint_task("Fix the login endpoint and add tests for invalid passwords")
    assert 0 <= result.score <= 100


def test_forge_spec_contains_sections():
    spec = forge_spec("Fix the login endpoint and add tests for invalid passwords")
    assert "/goal" in spec
    assert "/acceptance_tests" in spec
    assert "/task_lint" in spec


def test_main_no_input_errors(capsys):
    code = main([])
    captured = capsys.readouterr()
    assert code == 2
    assert "Provide task text" in captured.err
