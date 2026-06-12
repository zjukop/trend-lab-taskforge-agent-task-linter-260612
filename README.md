# TaskForge

Lint and upgrade vague coding tasks into bounded, agent-ready implementation specs.

## Install

```bash
pip install -e .
```

## Use

```bash
taskforge "Fix login bug and clean up auth"
```

Or pipe text:

```bash
echo "Improve API errors" | taskforge
```

## Test

```bash
pytest
```
