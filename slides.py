import marimo

__generated_with = "0.10.17"
app = marimo.App(width="medium", layout_file="layouts/slides.slides.json")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        """
        # Accelerate Python with Rust

        Juan Luis Cano Rodríguez <hello@juanlu.space>
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Get started in 3 simple steps

        1. `uvx maturin new -b pyo3 --src guessing-game && cd guessing-game`
        2. `uv run python` (this will take care of everything!)
        3. Run this in the REPL:

        ```python
        >>> from guessing_game import sum_as_string
        >>> sum_as_string(2, 3)
        '5'
        ```
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Now, a few adjustments

        Tell `uv` to rebuild the package when the Rust sources change:

        ```toml
        # pyproject.toml
        [tool.uv]
        # Rebuild package when any Rust files change
        cache-keys = [{file = "pyproject.toml"}, {file = "rust/Cargo.toml"}, {file = "**/*.rs"}]
        # Uncomment to build rust code in development mode
        # config-settings = { build-args = '--profile=dev' }
        ```
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Adjust `pyo3` to use the stable Python ABI:

        ```toml
        [dependencies]
        # pyo3 = "0.23.3"
        pyo3 = { version = "0.23.3", features = ["abi3-py39"] }
        ```

        Before:

        ```
        $ uv run maturin build
        ...
        📦 Built wheel for CPython 3.11 to .../guessing-game/target/wheels/guessing_game-0.1.0-cp311-cp311-manylinux_2_34_x86_64.whl
        ```

        After ✨:

        ```
        $ uv run maturin build
        ...
        📦 Built wheel for abi3 Python ≥ 3.8 to .../guessing-game/target/wheels/guessing_game-0.1.0-cp38-abi3-manylinux_2_34_x86_64.whl
        ```
        """
    )
    return


if __name__ == "__main__":
    app.run()
