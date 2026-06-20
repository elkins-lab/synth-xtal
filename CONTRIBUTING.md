# Contributing to synth-xtal

Thank you for your interest in contributing to **synth-xtal**! We welcome contributions in the form of bug reports, feature requests, documentation improvements, and code changes.

## 🚀 Getting Started

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally:
    ```bash
    git clone https://github.com/YOUR_USERNAME/synth-xtal.git
    cd synth-xtal
    ```
3.  **Install development dependencies**:
    ```bash
    pip install -e ".[dev,viz,docs]"
    ```
4.  **Install pre-commit hooks**:
    ```bash
    pre-commit install
    ```

## 🛠 Development Workflow

### Coding Standards
We use **Ruff** for linting and formatting, and **Mypy** for static type checking. These are enforced via pre-commit hooks.

-   **Linting/Formatting**: `ruff check .` and `ruff format .`
-   **Type Checking**: `mypy .`

### Testing
We use **Pytest** for testing. All new features and bug fixes must include corresponding tests. We aim for 100% test coverage.

-   **Run tests**: `pytest`
-   **Run tests with coverage**: `pytest --cov=synth_xtal --cov-report=term-missing`

### Documentation
Documentation is built with **MkDocs**.

-   **Serve documentation locally**: `mkdocs serve`

## 📬 Submitting a Pull Request

1.  **Create a new branch** for your changes:
    ```bash
    git checkout -b feature/my-new-feature
    ```
2.  **Commit your changes** with descriptive commit messages.
3.  **Ensure all tests pass** and coverage is maintained.
4.  **Push your branch** to your fork:
    ```bash
    git push origin feature/my-new-feature
    ```
5.  **Open a Pull Request** against the `main` branch of the original repository.

## ⚖️ Code of Conduct
By participating in this project, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).

## 📄 License
By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
