# Proposal

## Why

The script always greets the same name, so the only way to change the greeting is
to edit `main.py`. Every edit needs a code review for a change that is purely
presentational, and the project's documentation cannot show a personalized greeting
without a source edit.

## What Changes

Add an optional `--name` argument to the command line. With it, the script greets
that name. Without it, the script prints exactly the greeting it prints today, so
existing usage and the existing smoke test keep working.

## Capabilities

### New Capabilities

- `greeting`: which name the script greets and what it prints

### Modified Capabilities

## Impact

- `main.py`: argument parsing with the standard library's `argparse`
- `tests/test_greeting.py`: a new regression test for both behaviors
- `docs/tutorials/run-the-script.md`: how to use `--name`
- No dependency change: `argparse` is in the standard library
