from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class LintResult:
    score: int
    warnings: list[str]


def lint_task(text: str) -> LintResult:
    warnings: list[str] = []
    lowered = text.lower()

    if len(text.split()) < 8:
        warnings.append("Task is very short; add context and expected behavior.")
    if not any(word in lowered for word in ["test", "verify", "acceptance", "expected"]):
        warnings.append("Missing explicit verification or acceptance criteria.")
    if any(word in lowered for word in ["everything", "all", "rewrite", "clean up"]):
        warnings.append("Scope may be too broad; name files or boundaries.")
    if not any(word in lowered for word in ["file", "module", "endpoint", "component", "function"]):
        warnings.append("Missing likely files, modules, or surfaces to touch.")

    score = max(0, 100 - 15 * len(warnings))
    return LintResult(score=score, warnings=warnings)


def forge_spec(text: str) -> str:
    result = lint_task(text)
    warning_lines = "\n".join(f"- {w}" for w in result.warnings) or "- None"

    return f"""/goal
Ship a small, verifiable change for the following task:

{text.strip()}

/acceptance_tests
- Define or update automated tests that fail before the change and pass after it.
- Verify the primary user-visible or API behavior described by the task.
- Confirm no unrelated behavior changes are introduced.

/constraints
- Keep the change minimal and reversible.
- Avoid broad rewrites unless explicitly required.
- Do not introduce new dependencies without justification.
- Prefer touching the smallest set of files needed.

/files_to_touch
- Identify exact files after initial inspection.
- If scope expands, stop and explain why before continuing.

/rollback_plan
- Revert the implementation commit or restore modified files.
- Remove any added tests only if they are specific to the reverted behavior.

/completion_evidence
- Tests run and results.
- Summary of files changed.
- Before/after behavior notes.

/task_lint
Score: {result.score}/100
Warnings:
{warning_lines}
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Forge vague coding tasks into agent-ready specs.")
    parser.add_argument("task", nargs="*", help="Task text. If omitted, stdin is used.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    text = " ".join(args.task).strip() or sys.stdin.read().strip()
    if not text:
        print("Provide task text as an argument or via stdin.", file=sys.stderr)
        return 2
    print(forge_spec(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
