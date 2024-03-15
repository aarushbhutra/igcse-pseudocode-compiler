
# Interpreter Script for Custom Pseudocode Documentation

This document provides detailed information about the `interpreter.py` script, which is designed to interpret and execute custom pseudocode specified in `.pseudo` files. Below, you'll find instructions on how to run the script, along with descriptions of its syntax for declaring variables, assigning values, and generating output based on www.cambridgeinternational.org/Images/697401-2026-syllabus-legacy-notice.pdf

## Features

- **Pseudocode Interpretation:** Executes pseudocode written in `.pseudo` files.
- **Variable Declaration and Management:** Supports declaring variables with specific data types.
- **Value Assignment:** Allows assigning values to variables with type checking.
- **Output Generation:** Outputs the values of variables or strings to the console.

## Supported Syntax

1. **Declaring Variables:**
   - To declare a variable with a type, use the syntax: `DECLARE <variable_name>:<DATA_TYPE>`.
   - Supported data types: `INTEGER`, `REAL`, `CHAR`, `STRING`, `BOOLEAN`.

2. **Assigning Values:**
   - To assign a value to a variable, use the syntax: `<variable_name> <- <value>`.
   - The script performs type checking to ensure the value matches the variable's declared type.

3. **Generating Output:**
   - To output the value of a variable or a string, use the syntax: `OUTPUT "<text> " + <variable_name> +" <text>"`.
   - This syntax supports combining text and variable values in a single output command.

## How to Run

1. **Prerequisites:**
   - Python installed on your system.
   - `colorama` package installed via `pip install colorama`.

2. **Running the Script with a Pseudocode File:**
   - Prepare your `.pseudo` file with the pseudocode you wish to execute.
   - Open a terminal or command prompt.
   - Navigate to the directory containing `interpreter.py`.
   - Run the script with the command: `python interpreter.py <path_to_your_pseudocode_file>.pseudo`.
   - Follow any prompts or instructions that appear in the terminal.

3. **Extending or Modifying the Script:**
   - For those familiar with Python, the script can be extended with additional features or data types, or modified to change its existing behavior.
