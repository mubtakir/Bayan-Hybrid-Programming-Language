# CONTRIBUTING to Bayan

Thank you for considering contributing to Bayan! This file outlines how to set up your environment, coding standards, testing, and the contribution workflow.

## Prerequisites
- Python 3.10+
- Git
- Recommended: virtualenv or venv

## Setup
```bash
git clone <repo-url>
cd bayanLang/bayan
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt  # if present; otherwise pytest only
```

## Running tests
```bash
pytest -q
pytest -q tests/test_error_reporting.py  # single file
pytest -q -k substring                    # filter by name
```

## Code style
- Follow PEP8 where applicable.
- Prefer clear, explicit code over clever one-liners.
- Type hints are encouraged where reasonable.
- Keep functions small and focused; minimize side effects.

## Commits and branching
- Use Conventional Commits (recommended):
  - feat: new feature
  - fix: bug fix
  - docs: documentation only changes
  - refactor: code change that neither fixes a bug nor adds a feature
  - test: adding/adjusting tests
  - chore: build/tooling/misc
- Branching model:
  - main: stable
  - feature/*, fix/*: development branches

## Adding or changing language features
1. Open an issue describing the change with examples and rationale.
2. Start with tests (TDD if possible).
3. Update the lexer (new token/keyword), then the parser (grammar/AST), then the interpreter (evaluation), then tests/docs.
4. Ensure AST nodes carry line/column/filename via `with_pos`.
5. Verify error messages include Bayan stack and code frames for new constructs.

## Documentation
- Update docs/basics.md and docs/reference.md to reflect behavioral changes.
- For bigger design changes, update docs/architecture.md.
- Add examples to docs/cookbook.md where helpful.

## Pull requests
- Keep PRs small and focused.
- Add/adjust tests for every change.
- Ensure `pytest -q` passes locally.
- Describe what changed and why; include screenshots or snippets when relevant.

## Code review
- Be respectful and constructive.
- Ask clarifying questions; suggest alternatives when spotting issues.
- Approve only when tests pass and docs are up to date.

## Security and imports
- Python interop is allowed via a safe import whitelist; avoid enabling arbitrary imports.
- Do not include secrets or credentials in tests or docs.

## Release notes
- For user-facing changes, add a brief note to the release changelog (if present).

Thank you for contributing to Bayan!

