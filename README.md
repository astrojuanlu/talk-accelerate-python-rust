# Accelerate Python with Rust

Talk "Accelerate Python with Rust".

## Notes

Flat structure:

```shell
$ uvx maturin new -b pyo3 --src guessing-game
$ cd guessing-game
$ # Adjust Python version
$ sd 'requires-python = ">=3.8"' 'requires-python = ">=3.9"' pyproject.toml
$ # Add features to pyo3 Rust dependency
$ sd 'pyo3 = "(.*)"' 'pyo3 = { version = "$1", features = ["abi3-py39"] }' Cargo.toml
$ # Just launch Python (runs 'maturin' under the hood!)
$ uv run python
>>> import guessing_game
>>> guessing_game.sum_as_string(2, 3)
'5'
>>> ^D
```

Now remember to add this to `pyproject.toml`:

```toml
[tool.uv]
# Rebuild package when any rust files change
cache-keys = [{file = "pyproject.toml"}, {file = "rust/Cargo.toml"}, {file = "**/*.rs"}]
# Uncomment to build rust code in development mode
# config-settings = { build-args = '--profile=dev' }
```

(From https://github.com/PyO3/maturin/issues/2314#issuecomment-2488542771)

Alternative, with workspaces (inspired by https://github.com/astral-sh/uv/issues/9015#issue-2649309300):

```shell
$ uv init
$ mkdir packages
$ uvx maturin new -b pyo3 --src packages/guessing-game
$ pushd packages/guessing-game
$ # Adjust pyproject.toml, same as before (including `cache-keys`)
$ sd ...
$ popd
```

Then add this to `pyproject.toml`:

```toml
dependencies = [
    "guessing-game",
]

[tool.uv.workspace]
members = ["packages/*"]

[tool.uv.sources]
guessing-game = { workspace = true }
```

You will need to configure `rust-analyzer.linkedProjects` manually
because the extension only auto-discovers one level deep:

```shell
$ cat .vscode/settings.json
{
    "rust-analyzer.linkedProjects": [
        "packages/guessing-game/Cargo.toml"
    ]
}
```
