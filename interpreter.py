import sys
from colorama import Fore
from state_manager import variables, valid_data_types, evaluate_expression, determine_type
from colorama import Fore

def process_output_command(expression):
    # Evaluate the entire expression, including handling concatenations
    output = evaluate_expression(expression)
    if output is not None:
        print(output)

def parse_output_parts(parts):
    output_parts = []
    in_quotes = False
    current_part = ''
    for char in parts:
        if char == '"':
            if in_quotes:
                # End of a string literal
                output_parts.append(f'"{current_part}"')
                current_part = ''
            in_quotes = not in_quotes
        elif not in_quotes and char == '+':
            if current_part.strip():
                # Add variable or string outside quotes to output_parts
                output_parts.append(current_part.strip())
            current_part = ''
        else:
            current_part += char
    # Add the last part if it exists
    if current_part.strip():
        output_parts.append(current_part.strip())
    return output_parts

def process_input_command(command):
    command = command[len("INPUT "):].strip()  # Remove 'INPUT ' from the command

    if '[' in command and ']' in command:
        # Splitting the command to extract array name and index
        array_name, index_str = command[:-1].split('[')  # Remove ']' and split at '['
        array_name = array_name.strip()
        index_str = index_str.strip()

        # Check if the array is declared
        if array_name not in variables or "bounds" not in variables[array_name]:
            print(Fore.RED + f'Error: {array_name} is not a declared array.')
            return

        # Evaluate the index, considering it might be provided by a variable
        try:
            if index_str.isdigit():
                index = int(index_str)
            elif index_str in variables and isinstance(variables[index_str]["value"], int):
                index = variables[index_str]["value"]
            else:
                print(Fore.RED + 'Error: Invalid index.')
                return
        except ValueError:
            print(Fore.RED + 'Error: Invalid index.')
            return

        # Check if the index is within the array bounds
        lower_bound, upper_bound = variables[array_name]["bounds"]
        if not (lower_bound <= index <= upper_bound):
            print(Fore.RED + f'Error: Array index out of bounds.')
            return

        # Input handling
        input_value = input()  # Get the input without a specific message
        determined_type = determine_type(input_value)

        # Assigning input to the array element based on its type
        if determined_type == "INTEGER":
            variables[array_name]["value"][index - lower_bound] = int(input_value)
        elif determined_type == "STRING":
            variables[array_name]["value"][index - lower_bound] = input_value
        else:
            print(Fore.RED + 'Error: Type mismatch.')
    else:
        # Handling input for simple variables
        input_value = input()  # Get the input without a specific message
        if command in variables:
            var_type = variables[command]["type"]
            if var_type == "STRING":
                variables[command]["value"] = input_value
            elif var_type == "INTEGER" and input_value.isdigit():
                variables[command]["value"] = int(input_value)
            else:
                print(Fore.RED + 'Error: Type mismatch.')
        else:
            # New variable, determining type based on input
            determined_type = determine_type(input_value)
            if determined_type == "INTEGER":
                variables[command] = {"type": "INTEGER", "value": int(input_value)}
            else:
                variables[command] = {"type": "STRING", "value": input_value}

def assemble_output(output_parts):
    final_output = ''
    for part in output_parts:
        if part.startswith('"') and part.endswith('"'):
            # It's a string literal, trim the quotes and add to final output
            final_output += part[1:-1]
        else:
            # It's supposed to be a variable, add its value without leading/trailing spaces
            var_name = part.strip()
            if var_name in variables:
                # Directly concatenate variable's value to final_output
                final_output += variables[var_name]["value"]
            else:
                print(Fore.RED + f'Error: "{var_name}" is not a declared variable.' + Fore.RESET)
                return None
    return final_output

def process_constant_command(parts):
    name_value = parts.split("=")
    if len(name_value) != 2:
        print(Fore.RED + 'Error: CONSTANT command format is incorrect. Use CONSTANT <variable name> = <value>.' + Fore.RESET)
        return
    const_name, const_value = name_value[0].strip(), name_value[1].strip().strip('"')
    if const_name in variables and variables[const_name].get("is_constant", False):
        print(Fore.RED + f'Error: {const_name} is already defined as a constant and cannot be redeclared.' + Fore.RESET)
        return
    variables[const_name] = {"value": const_value, "is_constant": True}


def process_declare_command(parts):
    if 'ARRAY' in parts:
        # Process ARRAY declaration
        var_name, rest = parts.split(':', 1)
        array_info, var_type = rest.split('OF', 1)
        var_name = var_name.strip()
        var_type = var_type.strip()
        if ' ' in var_name:
            print(Fore.RED + 'Error: Variable name cannot contain spaces.' + Fore.RESET)
            return
        if '[' not in array_info or ']' not in array_info:
            print(Fore.RED + 'Error: Invalid array declaration.' + Fore.RESET)
            return
        bounds = array_info[array_info.find('[')+1:array_info.find(']')].split(':')
        if len(bounds) != 2:
            print(Fore.RED + 'Error: Array bounds must be specified as [lower:upper].' + Fore.RESET)
            return
        lower_bound, upper_bound = bounds
        try:
            lower_bound = int(lower_bound)
            upper_bound = int(upper_bound)
        except ValueError:
            print(Fore.RED + 'Error: Array bounds must be integers.' + Fore.RESET)
            return
        if lower_bound > upper_bound:
            print(Fore.RED + 'Error: Lower bound cannot be greater than upper bound.' + Fore.RESET)
            return
        if var_type not in valid_data_types:
            print(Fore.RED + f'Error: {var_type} is not a valid data type for an array.' + Fore.RESET)
            return
        # Store the array with its bounds and type
        variables[var_name] = {
            "type": f"ARRAY OF {var_type}",
            "bounds": (lower_bound, upper_bound),
            "value": [None] * (upper_bound - lower_bound + 1)  # Use None instead of "null"
        }
    else:
        # Process non-ARRAY declaration
        var_declaration = parts.split(":")
        var_name, var_type = var_declaration[0].strip(), var_declaration[1].strip()
        if ' ' in var_name:
            print(Fore.RED + 'Error: Variable name cannot contain spaces.' + Fore.RESET)
            return
        if var_type not in valid_data_types:
            print(Fore.RED + f'Error: {var_type} is not a valid data type. Valid data types are: {", ".join(valid_data_types)}.' + Fore.RESET)
            return
        variables[var_name] = {"type": var_type, "value": "null"}



def process_assignment_command(parts):
    left_side, right_side = parts.split("<-")
    left_side, right_side = left_side.strip(), right_side.strip()

    evaluated_right_value = evaluate_expression(right_side)

    if '[' in left_side and ']' in left_side:
        array_name, index = left_side.split('[')
        index = index.rstrip(']')
        array_name = array_name.strip()

        if array_name in variables and "bounds" in variables[array_name]:
            try:
                index = int(index) - variables[array_name]["bounds"][0]  # Adjust for base index
                if index < 0 or index >= len(variables[array_name]["value"]):
                    print(Fore.RED + 'Error: Invalid array index.' + Fore.RESET)
                    return
                variables[array_name]["value"][index] = evaluated_right_value
            except ValueError:
                print(Fore.RED + 'Error: Invalid array index.' + Fore.RESET)
        else:
            print(Fore.RED + f'Error: {array_name} is not a declared array.' + Fore.RESET)
    else:
        if left_side in variables:
            variables[left_side]["value"] = evaluated_right_value
        else:
            print(Fore.RED + f'Error: {left_side} is not declared.' + Fore.RESET)


def process_line(line):
    line, _, _ = line.partition('//')
    line = line.strip()
    if not line:
        return
    if line.startswith("INPUT"):
        process_input_command(line)
    elif line.startswith("OUTPUT"):
        process_output_command(line[len("OUTPUT"):].strip())
    elif line.startswith("DECLARE"):
        process_declare_command(line[len("DECLARE"):].strip())
    elif line.startswith("CONSTANT"):
        process_constant_command(line[len("CONSTANT"):].strip())    
    elif "<-" in line:
        process_assignment_command(line)
