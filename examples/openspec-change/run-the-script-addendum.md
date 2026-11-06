## Greet a name from the command line

`main.py` accepts `--name`, so the greeting does not need a source edit:

```bash
uv run --locked python main.py --name Ada
```

The output is `Hello from Ada!`. Running the script without the argument prints the
default greeting, so existing usage is unchanged:

```bash
uv run --locked python main.py
```

`tests/test_greeting.py` covers both behaviors. Edit `DEFAULT_NAME` in `main.py` if
your project's default greeting should name something else.
