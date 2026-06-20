# Publishing synth-xtal to PyPI

This guide explains how to publish `synth-xtal` to PyPI.

## Prerequisites

1.  **Install Build Tools**:
    ```bash
    pip install build twine
    ```

2.  **PyPI Account**: Ensure you have an account at [PyPI](https://pypi.org/).

## Publishing Workflow

### 1. Build the Package
```bash
# Clean old builds
rm -rf dist/ build/ *.egg-info

# Build wheels and source dist
python -m build
```

### 2. Upload to PyPI (Manual)
```bash
python -m twine upload dist/*
```

## Automated Publishing (GitHub Actions)

The repository is configured to automatically publish to PyPI when a **GitHub Release** is created.

1.  Add your PyPI API token to GitHub Secrets as `PYPI_API_TOKEN`.
2.  Update the version in `pyproject.toml`.
3.  Create and publish a new Release on GitHub.

## Bioconda Publishing

`synth-xtal` is also published on Bioconda. The recipe is maintained in a fork of `bioconda-recipes`.

### 1. Update the Recipe
The local copy of the recipe is tracked in `bioconda_recipe/`. When a new version is released on PyPI:
1.  Update `version` and `sha256` in `bioconda_recipe/meta.yaml`.
2.  Copy the recipe to your `bioconda-recipes` fork:
    ```bash
    cp bioconda_recipe/* ../bioconda-recipes/recipes/synth-xtal/
    ```

### 2. Submit to Bioconda
1.  Go to your local `bioconda-recipes` clone.
2.  Create a new branch for the release.
3.  Commit the changes and push to your fork.
4.  Open a Pull Request on the main [bioconda-recipes](https://github.com/bioconda/bioconda-recipes) repository.
