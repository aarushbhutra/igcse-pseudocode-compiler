import sys
from colorama import Fore, init

init(autoreset=True)

variables ={}
valid_data_types = ["INTEGER", "REAL", "CHAR", "STRING", "BOOLEAN"]

def is_valid_value_for_type(value, var_type):
    # Basic type validation logic
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

def process_output_command(parts):
    output_parts = parse_output_parts(parts)
    final_output = assemble_output(output_parts)
    if final_output is not None:
        print(final_output)

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

def process_declare_command(parts):
    var_declaration = parts.split(":")
    if len(var_declaration) != 2:
        print(Fore.RED + 'Error: Variable declaration format is <variable name>:<data type>.' + Fore.RESET)
        return
    var_name, var_type = var_declaration
    if ' ' in var_name:
        print(Fore.RED + 'Error: Variable name cannot contain spaces.' + Fore.RESET)
        return
    if not var_name or var_name.startswith(":"):
        print(Fore.RED + 'Error: A variable name must be provided before the data type.' + Fore.RESET)
        return
    if var_type not in valid_data_types:
        print(Fore.RED + f'Error: {var_type} is not a valid data type. Valid data types are: {", ".join(valid_data_types)}.' + Fore.RESET)
        return
    variables[var_name] = {"type": var_type, "value": "null"}


def process_assignment_command(parts):
    var_name, value = parts.split("<-")
    var_name = var_name.strip()
    value = value.strip().strip('"')
    if var_name not in variables:
        print(Fore.RED + f'Error: Variable {var_name} is not declared.' + Fore.RESET)
        return
    if not is_valid_value_for_type(value, variables[var_name]["type"]):
        print(Fore.RED + f'Error: Type mismatch or invalid value for variable {var_name}.' + Fore.RESET)
        return
    variables[var_name]["value"] = value

def process_line(line):

    line, _, _ = line.partition('//')
    line = line.strip()
    if not line:  # If the line is empty after removing the comment, skip it
        return

    if line.startswith("OUTPUT"):
        process_output_command(line[len("OUTPUT"):].strip())
    elif line.startswith("DECLARE"):
        process_declare_command(line[len("DECLARE"):].strip())
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
    print(variables)