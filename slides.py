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
        # Accelerate your Python code with Rust

        Juan Luis Cano Rodríguez <hello@juanlu.space>
        2025-01-29 @ DoEPy
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        # Outline

        1. Python is slow, you say?
        2. Python + Rust = 🤜🤛
        3. Demo
        4. Conclusions
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        # Intro

        Juan Luis (he/him/él 🇪🇸)

        - Aerospace Engineer passionate about tech communities and sustainability ♻️
        - Product Manager at QuantumBlack, AI by McKinsey, for Kedro, an open source pipeline framework 🥑
        - Organizer of the PyData Madrid monthly meetup (ex Python España, ex PyCon Spain) 🐍
        - Contributor to the SciPy and PyData ecosystem 🧪
        - Music lover 🎵

        Follow me! 🧑‍💻 [github.com/astrojuanlu](https://github.com/astrojuanlu)

        ![Mini Juanlu](public/minijuanlu.png)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        # Python + Rust = 🤜🤛

        The most desired 🐍 and the most admired 🦀! https://survey.stackoverflow.co/2024/technology/#2-programming-scripting-and-markup-languages

        ![Admired and desired](public/stack-overflow-survey-most-desired.png)
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

        ### Broaden compatibility of built wheels

        Adjust `pyo3` to use the stable Python ABI:

        ```toml
        # Cargo.toml
        [dependencies]
        # pyo3 = "0.23.3"
        pyo3 = { version = "0.23.3", features = ["abi3-py38"] }
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


@app.cell
def _(mo):
    mo.md(
        """
        ### Improve the project layout

        You can also place the Rust code in a separate `rust` directory and use the common src-layout for the Python code:

        ```
        ├── README.md
        ├── pyproject.toml
        ├── src
        │   └── guessing_game
        │       └── __init__.py
        └── rust
            ├── Cargo.toml
            └── src
                └── lib.rs
        ```

        - https://www.maturin.rs/project_layout#alternate-python-source-directory-src-layout
        - https://github.com/PyO3/maturin/blob/de6b75e1/src/project_layout.rs#L158-L161
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ...mark the Rust code as protected:

        ```toml
        [tool.maturin]
        features = ["pyo3/extension-module"]
        module-name = "guessing_game._guessing_game"  # <---
        ```

        ```rust
        #[pymodule]
        #[pyo3(name = "_guessing_game")]  // <---
        fn guessing_game(m: &Bound<'_, PyModule>) -> PyResult<()> {
        ```
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ...and write your own Python code:

        ```python
        # src/guessing_game/__init__.py
        # See https://www.maturin.rs/project_layout#pure-rust-project
        from ._guessing_game import *

        __doc__ = _guessing_game.__doc__
        if hasattr(_guessing_game, "__all__"):
            __all__ = _guessing_game.__all__
        ```
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Make `uv` smarter

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


if __name__ == "__main__":
    app.run()
