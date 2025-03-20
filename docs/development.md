# Development

Depends on:

* Python >=3.9

---

1. Clone the repository and create and activate a python virtual environment of your choice.
1. Inside a virtual environment or machine: `python -m pip install -r requirements-docs.txt`

## Release/Versioning

Version numbers should be used in tagging commits on the `main` branch and should be of the form `v0.1.7` using the semantic versioning convention.

## Building & deploying the documentation

Run `mkdocs build` to build the docs.

Then run `mkdocs gh-deploy` to deploy to the `gh-pages` branch of the repository. You must have write access to the repo.
