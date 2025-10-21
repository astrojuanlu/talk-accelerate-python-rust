import marimo

__generated_with = "0.17.0"
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

    2025-10-21 @ PyData Toledo
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
    - Developer Relations Engineer at Canonical, the makers of Ubuntu 🥑
      - Past: McKinsey & Company, Read the Docs, Satellogic
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
    ## There are ~~too~~ many ways to make Python faster

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

    ![Screenshot of a PyVideo talk on Numba](public/juanlu-numba-pyvideo.png)
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    **Fast forward to 2025...**

    What if the bad part of compiled languages wasn't the languages themselves, but the **tooling**?

    What if there was a compiled language that was **modern**, produced binaries that **don't need a runtime**, integrated **seamlessly** with Python, and had **awesome tooling**?
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    # Python + Rust = 🤜🤛

    The most desired 🐍 and the most admired 🦀! https://survey.stackoverflow.co/2025/technology#2-programming-scripting-and-markup-languages

    ![Admired and desired](public/stack-overflow-survey-most-desired.png)
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## What is Rust?

    > The Chromium project finds that around 70% of our serious security bugs are memory safety problems.

    https://www.chromium.org/Home/chromium-security/memory-safety/

    - Created at Mozilla Research in 2006, version 1.0 in 2015
    - Emphasis on memory safety, type safety
    - Popular in data engineering (Polars, Delta Lake) and Python tooling (uv, ruff)
    - First language other than C and assembly to be included in the Linux kernel
    - MIT + Apache 2.0 licensed
    - Supported by the Rust Foundation, a US 501(c)6 non-profit
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
    - Just for fun because it's cool

    ```rust
    // main.rs
    fn main() {
        println!("Hello, world!");
    }
    ```
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
    ## Get started in 3 simple steps

    1. `uvx maturin new -b pyo3 --src py-rust && cd py-rust`
    2. `uv run python` (this will take care of everything!)
    3. Run this in the REPL:

    ```python
    >>> from py_rust import sum_as_string
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

    ```
    $ tree
    .
    ├── Cargo.toml
    ├── pyproject.toml
    └── src
        └── lib.rs

    2 directories, 3 files
    ```

    This makes use of [PyO3](https://pyo3.rs/), a project that provides "Rust bindings to the Python interpreter".

    > PyO3 can be used to write native Python modules or run Python code and modules from Rust.

    ```
    $ head -n1 src/lib.rs
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

    ```rust
    /// Formats the sum of two numbers as string.
    #[pyfunction]
    fn sum_as_string(a: usize, b: usize) -> String {
        (a + b).to_string()
    }
    ```

    - `///` Marks the beginning of a _doc comment_
    - `#[pyfunction]` is an _attribute macro_ coming from PyO3
    - `fn sum_as_string` defines the function
    - Both parameters and the function itself have annotated types
    - `(a + b).to_string()` is the last expression of the function block and becomes its return value
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        In PyO3, errors are handled using the `PyResult` type, which wraps the actual return type (it is defined as `pub type PyResult<T> = Result<T, PyErr>`):

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
    /// A Python module implemented in Rust.
    #[pyo3::pymodule]
    mod py_rust {
        use pyo3::prelude::*;

        #[pyfunction]
        fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
            Ok((a + b).to_string())
        }
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
    # pyo3 = "0.25.0"
    pyo3 = { version = "0.27.0", features = ["abi3-py310"] }
    ```

    Before:

    ```
    $ uvx maturin build
    🔗 Found pyo3 bindings
    ...
    📦 Built wheel for CPython 3.14 to .../py_rust-0.1.0/target/wheels/py_rust-0.1.0-cp314-cp314-linux_x86_64.whl
    ```

    After ✨:

    ```
    $ uvx maturin build
    🔗 Found pyo3 bindings with abi3 support
    ...
    📦 Built wheel for abi3 Python ≥ 3.10 to .../py_rust-0.1.0/target/wheels/py_rust-0.1.0-cp310-abi3-linux_x86_64.whl
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
    │   └── py_rust
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
    module-name = "py_rust._py_rust"  # <---
    ```

    ```rust
    #[pyo3::pymodule]
    #[pyo3(name = "_py_rust")]  // <---
    mod py_rust {
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
    # src/py_rust/__init__.py
    # See https://www.maturin.rs/project_layout
    from ._py_rust import *

    __doc__ = _py_rust.__doc__
    if hasattr(_py_rust, "__all__"):
        __all__ = _py_rust.__all__
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

    2025-10-21 @ PyData Toledo
    """
    )
    return


if __name__ == "__main__":
    app.run()
