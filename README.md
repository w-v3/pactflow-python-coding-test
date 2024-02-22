# PactFlow Python Coding Test

Welcome to this Python coding test. This test is designed to assess your ability
to write clean, well-structured, and maintainable code. You will be tasked with
adding some functionality to this codebase.

## Documentation

MkDocs is used to generate all the documentation, which can be viewed by running

```console
hatch run docs
```

## Development

This project uses [Hatch](https://hatch.pypa.io) for managing the development
environment. The code is split across three packages:

-   `pypacter`: The core logic
-   `pypacter-api`: API wrapper
-   `pypacter-cli`: CLI to interact with the API

The structure of the project is as follows:

```text
pypacter/
├── pypacter-api/     <== API wrapper
│  ├── src/pypacter_api/
│  ├── tests/
│  ├── pyproject.toml
│  └── README.md
├── pypacter-cli/     <== CLI to interact with API
│  ├── src/pypacter_cli/
│  ├── tests/
│  ├── pyproject.toml
│  └── README.md
├── docs/            <== MkDocs documentation
├── notebooks/       <== Jupyter notebooks
├── src/
│  └── pypacter/     <== Core logic
├── tests/
├── mkdocs.yml
├── pyproject.toml
└── README.md
```

## Tasks

### Task 1

#### Summary

Add a new function to the core package to:

-   Ingest a snippet of code
-   Output the most likely programming language

#### Motivation

Clients will be submitting code snippets to the API, and in order to improve the
customer experience, we want to automatically detect the programming language
instead of requiring the client to specify it.

### Task 2

#### Summary

Add a new API endpoint for the language detection function.

#### Motivation

Another team is building a feature that requires the language detection
functionality, and instead of duplicating the work, they have asked us to
expose the functionality via a new API endpoint.

### Task 3

#### Summary

Add a new CLI command for the language detection function. The CLI should
accept the code snippet either as a file path, or through standard input.

#### Motivation

The CLI is the primary way that developers interact with the API, and we want to
make sure that the new functionality is easily accessible.

### Task 4 (Optional)

Show-case your skills by adding a new feature of your choice to the core package. Ideally, this feature should make use of an LLM.
