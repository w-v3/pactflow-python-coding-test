# PactFlow Python Coding Test

Welcome to this Python coding test. This test is designed to assess your ability to write clean, well-structured, and maintainable code. You will be tasked with adding some functionality to this codebase.

We will be looking for the following aspects:

1.  The readability and clarity of your code; including aspects such as:
    -   Naming conventions
    -   Code structure
    -   Comments
    -   Documentation
2.  The correctness of your code; including aspects such as:
    -   Handling of edge cases
    -   Error handling
    -   Testing
3.  The maintainability of your code; including aspects such as:
    -   Modularity
    -   Extensibility
    -   Reusability
4.  Your familiarity with standard development tools and practices; including aspects such as:
    -   Version control
    -   Creating and using virtual environments
    -   Documenting PRs and commits

Please fork this repository and submit your solution as a pull request. Your solution should pass the existing CI checks, and you should ensure that your code is tested. This project uses the [pytest](https://docs.pytest.org/en/stable/) testing framework.

## Development

This project uses [Hatch](https://hatch.pypa.io) for managing the development environment. The code is split across two packages:

-   `pypacter`: The core logic
-   `pypacter-api`: API wrapper

The structure of the project is as follows:

```text
pypacter/
├── pypacter-api/     <== API wrapper
│  ├── src/pypacter_api/
│  ├── tests/
│  ├── pyproject.toml
│  └── README.md
├── notebooks/       <== Jupyter notebooks (if any)
├── src/
│  └── pypacter/     <== Core logic
├── tests/
├── pyproject.toml
└── README.md
```

## Tasks

The following tasks purposefully leave out some specificity to allow you to demonstrate your problem-solving skills, and give you the opportunity to make decisions about the implementation.

Each task should only take about 30 minutes to complete, and you should also allow 30 minutes to familiarize yourself with the codebase. If you find yourself spending more time on a task, submit what you have and document in the PR what you would have done if you had more time.

### Task 1

#### Summary

Add a new function to the core package to:

-   Ingest a snippet of code
-   Output the most likely programming language

Ideally, this function should make use of a large language model (LLM) to detect the language, but you can use any method you prefer.

#### Motivation

Clients will be submitting code snippets to the API, and in order to improve the customer experience, we want to automatically detect the programming language instead of requiring the client to specify it.

### Task 2

#### Summary

Add a new endpoint to the existing API which exposes the language detection functionality.

#### Motivation

This is unlikely to be useful in isolation, but we expect to use this functionality in the future to enhance other functionality.

### Task 3

#### Summary

Integrate the language-detection ability with the existing `reviewer` functionality for code reviews

#### Motivation

Enhancing the `reviewer` functionality with language detection will hopefully improve the accuracy and relevance of the code reviews, providing a better experience for the users.

### Task 4 (Optional)

Show-case your skills by adding a new feature of your choice to the core package. Ideally, this feature should make use of an LLM.
