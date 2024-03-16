from colorama import Fore

variables = {}
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

def evaluate_expression(expression):
    # This function needs to handle expressions that may include concatenation ('+')
    evaluated_parts = []
    expression_parts = expression.split('+')  # Split the expression by '+'

    for part in expression_parts:
        part = part.strip()
        if part.startswith('"') and part.endswith('"'):
            # Handle string literals by removing the surrounding quotes
            evaluated_parts.append(part[1:-1])
        elif '[' in part and ']' in part:
            # Array element access
            array_name, index = part.split('[')
            index = index.rstrip(']').strip()
            array_name = array_name.strip()

            if array_name in variables and "bounds" in variables[array_name]:
                try:
                    index = int(index) - variables[array_name]["bounds"][0]  # Adjust for base index
                    value = variables[array_name]["value"][index]
                    if value is None:
                        print(Fore.RED + f'Error: Element at index {index + variables[array_name]["bounds"][0]} in array "{array_name}" is uninitialized.' + Fore.RESET)
                        return ""
                    evaluated_parts.append(str(value))
                except (ValueError, IndexError):
                    print(Fore.RED + 'Error: Invalid array index.' + Fore.RESET)
                    return ""
            else:
                print(Fore.RED + f'Error: {array_name} is not a declared array.' + Fore.RESET)
                return ""
        elif part.isdigit() or (part[0] == '-' and part[1:].isdigit()):
            # Handle integers directly
            evaluated_parts.append(part)
        elif part in variables:
            # Handle variables
            value = variables[part]["value"]
            if value is None:
                print(Fore.RED + f'Error: Variable "{part}" is uninitialized.' + Fore.RESET)
                return ""
            evaluated_parts.append(str(value))
        else:
            print(Fore.RED + f'Error: {part} is not defined.' + Fore.RESET)
            return ""

    return ''.join(evaluated_parts)  # Join the evaluated parts into a single string