import sys
from colorama import Fore, init

init(autoreset=True)

"""
TODO:
2D Array Creation, Assignment, and Access
"""

variables ={}
valid_data_types = ["INTEGER", "REAL", "CHAR", "STRING", "BOOLEAN"]

def is_valid_value_for_type(value, var_type):
    if var_type == "INTEGER":
        return value.isdigit() or (value.startswith('-') and value[1:].isdigit())
    elif var_type == "REAL":
        try:
            float(value)
            return True
        except ValueError:
            return False
    elif var_type == "CHAR":
        return len(value) == 1
    elif var_type == "STRING":
        return isinstance(value, str)
    elif var_type == "BOOLEAN":
        return value in ["TRUE", "FALSE"]
    return False

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

def evaluate_expression(expression):
    # Split the expression by '+' while considering potential spaces around it
    parts = expression.split('+')
    evaluated_parts = []
    
    for part in parts:
        part = part.strip()  # Remove leading and trailing spaces
        if part.startswith('"') and part.endswith('"'):
            # Directly append string literals without quotes
            evaluated_parts.append(part[1:-1])
        elif '[' in part and ']' in part:
            # Handle array access
            var_name, index = part.split('[')
            index = index.rstrip(']')
            var_name = var_name.strip()

            if var_name in variables and "bounds" in variables[var_name]:
                try:
                    index = int(index) - variables[var_name]["bounds"][0]  # Adjust for base index
                    value = variables[var_name]["value"][index]
                    if value is None:
                        print(Fore.RED + f'Error: Element at index {index + variables[var_name]["bounds"][0]} in array "{var_name}" is uninitialized.' + Fore.RESET)
                        return None
                    evaluated_parts.append(value)
                except (ValueError, IndexError):
                    print(Fore.RED + 'Error: Invalid array index.' + Fore.RESET)
                    return None
            else:
                print(Fore.RED + f'Error: {var_name} is not a declared array.' + Fore.RESET)
                return None
        elif part in variables:
            # Append variable value
            value = variables[part]["value"]
            if value is None:
                print(Fore.RED + f'Error: Variable "{part}" is uninitialized.' + Fore.RESET)
                return None
            evaluated_parts.append(value)
        else:
            # Handle other cases or undefined variables
            print(Fore.RED + f'Error: {part} is not defined.' + Fore.RESET)
            return None

    # Join evaluated parts with no space, as spaces were considered during splitting
    return ''.join(str(part) for part in evaluated_parts)



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

    if line.startswith("OUTPUT"):
        process_output_command(line[len("OUTPUT"):].strip())
    elif line.startswith("DECLARE"):
        process_declare_command(line[len("DECLARE"):].strip())
    elif line.startswith("CONSTANT"):
        process_constant_command(line[len("CONSTANT"):].strip())    
    elif "<-" in line:
        process_assignment_command(line)

def main():
    if len(sys.argv) != 2:
        print("Usage: interpreter.py <filename.pseudo>")
        return
    

    filename = sys.argv[1]

    if not filename.endswith(".pseudo"):
        print("Error: File must end with .pseudo")
        return
    
    try:
        # Open and read the file
        with open(filename, 'r') as file:
            for line in file:
                process_line(line.strip())
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")

if __name__ == "__main__":
    main()
    print("\n")
    print(variables)