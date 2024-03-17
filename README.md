
# Interpreter Script for Custom Pseudocode Documentation

This document provides detailed information about the `main.py` script, designed to interpret and execute custom pseudocode specified in `.pseudo` files. Below, you'll find instructions on how to run the script, along with descriptions of its syntax for declaring variables and constants, assigning values, declaring arrays, and generating output based on www.cambridgeinternational.org/Images/697401-2026-syllabus-legacy-notice.pdf (USER DEFINED VARIABLES ARE NOT INCLUDED)

## Features

- **Pseudocode Interpretation:** Executes pseudocode written in `.pseudo` files.
- **Variable and Constant Declaration and Management:** Supports declaring variables with specific data types and defining constants.
- **Array Management:** Allows declaring and utilizing arrays with defined boundaries.
- **Value Assignment:** Enables assigning values to variables and array elements with type checking.
- **Output Generation:** Outputs the values of variables, constants, array elements, or strings to the console.
- **Input Assignment** Allows for asking users to input values which will be stored as new or old variables which are reassigned.
- **Arithemetic Opperations** Using Arithemetic is now possible however cant be used in output. Supports +,-,*,/.MOD and DIV

## Supported Syntax

1. **Declaring Variables and Constants:**
   - For variables: `DECLARE <variable_name>:<DATA_TYPE>`.
   - For constants: `CONSTANT <constant_name> = <value>`.
   - Supported data types: `INTEGER`, `REAL`, `CHAR`, `STRING`, `BOOLEAN`.

2. **Declaring Arrays:**
   - Syntax: `DECLARE <identifier>:ARRAY[<lower_bound>:<upper_bound>] OF <data_type>` and to assign array values `<array_name>[position] <- <value>`.
   - This allows for the declaration of arrays with specified bounds and a data type for the elements.

3. **Assigning Values:**
   - To assign a value to a variable or an array element, use: `<variable_name> <- <value>` which supports arrays.
   - The script ensures that the assigned values match the declared types.

4. **Generating Output:**
   - Syntax: `OUTPUT "<text> " + <variable_name> + " <text>"` for arrays you can use `<array_name>[position]`.
   - Supports combining text with the values of variables, constants, or array elements in a single output command.

5. **Asking for Input**
   - For Variables `INPUT <variable_name>`
   - For Arrays `INPUT <variable_name>[position]`
   - Supports automatic assignment to either String or Integer for simplicity

## How to Run

1. **Prerequisites:**
   - Python installed on your system.
   - `colorama` package installed via `pip install colorama`.

2. **Running the Script with a Pseudocode File:**
   - Prepare your `.pseudo` file with the pseudocode you wish to execute.
   - Open a terminal or command prompt.
   - Navigate to the directory containing `main.py`.
   - Run the script with: `python main.py <path_to_your_pseudocode_file>.pseudo`.
   - Follow any prompts or instructions that appear in the terminal.

3. **Extending or Modifying the Script:**
   - The script can be extended with additional features or modified to change its existing behavior for those familiar with Python.
