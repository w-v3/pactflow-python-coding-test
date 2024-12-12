# PactFlow Python Coding Test

### Task 1

#### Summary

Add a new function to the core package to:

-   Ingest a snippet of code
-   Output the most likely programming language

Ideally, this function should make use of a large language model (LLM) to detect the language, but you can use any method you prefer.

#### Solution Approach

The approach utilizes a structured methodology combining prompt engineering, LLM integration, and a well-defined input-output schema to achieve accurate and flexible language detection. Follows design approach similar to code reviewr class to keep the overall project structure same for future improvments.
Added a small preprocessing method whose functionality can be extended as per requirements. As Currently there were no complex preprocessing requirements it was implmented only as function, though it is important to keep in mind that this can be changed in future wherein a separate runnable can be implemented and added to the current chain for preprocessing the input.   
error handling is implemented in the invoke method to manage exceptions, ensuring the system gracefully handles unexpected failures. If an error occurs, a fallback output is provided with a message indicating the issue.

### Task 2

#### Summary

Add a new endpoint to the existing API which exposes the language detection functionality.

#### Solution Approach

adding two new endpoints: one for language detection and one for code review. Used Pydantic's classes for validation of input and output to the API endpoints along with fastapi's dependency injection system ensuring appropriate instance is available for the endpoint while keeping the code clean and modular.

### Task 3

#### Summary

Integrate the language-detection ability with the existing `reviewer` functionality for code reviews

#### Solution Approach

To integrate the Language Detector class with the Reviewer class, the Reviewer class was modified to include language detection as part of its workflow. 
This integration ensures that the code snippet is first analyzed for its programming language and then reviewed accordingly. This enhancement will make the code review process more context-aware by tailoring feedback based on the detected language. 

Along with this unit testing was also implemented for all modules 

### Task 4 (Optional)

Show-case your skills by adding a new feature of your choice to the core package. Ideally, this feature should make use of an LLM.

#### Solution Approach

Though I didn't find enough bandwidth to develop and integrate a new feature around the Code review process but I had some ideas which could be easily implemented to enhance the code review api.

1. Automatic code Commenting Feature
A Code Commentor class can be designed to either just generate comments for a given code file or to insert those comments directly into the code.

Here are two potential ways this can be handled:

- Generating Comments Without Inserting
In this approach, the CodeCommentor class analyzes the code, generates comments, and returns them as a separate output without modifying the original code. 
This allows developers to review and decide how to integrate the comments manually. This is useful for situations where you want to keep the original code unaltered and review comments before applying them.

- Inserting Comments Directly into Code
In this more advanced approach, the CodeCommentor class not only generates comments but also inserts them directly into the code at appropriate places. This can be done by parsing the code and determining where the comments should be placed (e.g., before a function definition, above a loop, or near complex code blocks). This approach automates the process of enhancing code readability and documentation.

The First Approach should always be priortised and implmented as it is the most easiest to implment and test.

2. Automated Documentation Generator
This API would generates comprehensive documentation for a codebase, including descriptions of functions, classes, and modules. This tool would provide a starting point for creating more detailed documentation, improving the maintainability and collaboration of code teams.
