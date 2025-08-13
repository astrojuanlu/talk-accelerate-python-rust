import marimo

__generated_with = "0.14.17"
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

    2025-06-26 @ PyData Madrid
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

    Follow me! ::octicon:mark-github-16:: [github.com/astrojuanlu](https://github.com/astrojuanlu)

    ![Mini Juanlu](public/minijuanlu.png)
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
    # Python is slow, you say?

    ## Yes...

    Pereira, R. _et al._ (2021) ‘Ranking programming languages by Energy Efficiency’, _Science of Computer Programming_, 205, p. 102609. doi:10.1016/j.scico.2021.102609.

    ![Language efficiency](public/energy-time-memory-programming-languages.png)
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
    ## ...but

    ...the community has known _reasonable_ ways to get around that for 25+ years

    ![SciPy languages](public/scipy-languages.png)
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
    ## There are many ways to make Python faster

    - NumPy
    - Cython
    - Pythran
    - Numba
    - PyPy
    - mypyc
    - ...write an extension in a compiled language: C, C++, FORTRAN

    Each option has pros and cons, there's no silver bullet.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
    My first experience contributing a compiled extension to SciPy didn't go really well...

    ![@astrojuanlu rewriting odeint in Fortran 95 in 2013](public/astrojuanlu-odeint.png)
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    And that's why I was so excited about the alternatives!

    ![Old screenshot of Pybonacci first blog post on numba](public/pybonacci-numba-2012.png)
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Developer Experience wins

    What if the bad part of compiled languages wasn't the languages themselves, but the **tooling**?

    What if there was a compiled language that was **modern**, produced binaries that **don't need a runtime**, integrated **seamlessly** with Python, and had **awesome tooling**?
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
    I became obsessed with numba, gave a dozen talks about it or more, and then focused on other things for a few years.

    _Until..._
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
    ## Why Rust?

    - Because there are so many awesome crates (I care about ecosystems, not languages)
    - Because many great Python libraries and tools have a Rust core (Polars, Pydantic, uv, ruff)
    - Because the error messages and the IDE integration helps you learn
    - Because it's memory safe
    - Just for fun because it's cool
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
    ## How does this all work?

    This makes use of [PyO3](https://pyo3.rs/), a project that provides "Rust bindings to the Python interpreter".

    > PyO3 can be used to write native Python modules or run Python code and modules from Rust.

    ```rust
    use pyo3::prelude::*;
    ```
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Defining functions

    You can create a Python function from a Rust function adding the `#[pyfunction]` attribute:

    ```rust
    #[pyfunction]
    fn sum_as_string(a: usize, b: usize) -> String {
        (a + b).to_string()
    }
    ```
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        This function was trivial, but in case you need to handle errors, you should return `PyResult`, defined as `pub type PyResult<T> = Result<T, PyErr>`:

        ```rust
        #[pyfunction]
        fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
            Ok((a + b).to_string())
        }
        ```
        """
    ).callout(kind="info")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Adding functions to modules

    To be able to actually call the function from Python it needs to be added to a module. Modules are defined with the `#[pymodule]` attribute:

    ```rust
    #[pymodule]
    #[pyo3(name = "_rode")]
    fn rode(m: &Bound<'_, PyModule>) -> PyResult<()> {
        m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
        Ok(())
    }
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
    # pyo3 = "0.25.1"
    pyo3 = { version = "0.25.1", features = ["abi3-py39"] }
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
    📦 Built wheel for abi3 Python ≥ 3.9 to .../guessing-game/target/wheels/guessing_game-0.1.0-cp39-abi3-manylinux_2_34_x86_64.whl
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


@app.cell
def _(mo):
    mo.md(
        """
    # It's demo time!

    ::octicon:mark-github-16:: https://github.com/astrojuanlu/rode

    ![Near-parabolic orbit propagation](public/farnocchia.png)
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
    # Conclusions

    - Integrating Python with Rust is straightforward
    - For simple scientific code Rust is not that difficult to pick up
    - Rewriting slow code fragments in Rust is a very effective strategy to accelerate Python code

    **Thank you!**

    ::octicon:mark-github-16:: https://github.com/astrojuanlu/talk-accelerate-python-rust

    Juan Luis Cano Rodríguez <hello@juanlu.space>

    2025-06-26 @ PyData Madrid
    """
    )
    return


if __name__ == "__main__":
    app.run()
