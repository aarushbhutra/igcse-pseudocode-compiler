from colorama import Fore
import operator
import re
from collections import deque

variables = {}
valid_data_types = ["INTEGER", "REAL", "CHAR", "STRING", "BOOLEAN"]

def determine_type(value):
    try:
        int(value)
        return "INTEGER"
    except ValueError:
        return "STRING"
    
ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,  # Note: Division always results in a REAL type
    'DIV': operator.floordiv,
    'MOD': operator.mod,
}

precedence = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    'DIV': 2,
    'MOD': 2,
    '(': 0,
    ')': 0,
}

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def preprocess_expression(expression):
    # Tokenize the expression for variables, operators, numbers, and parentheses
    tokens = re.findall(r"\b\w+\[\d+\]|\b\w+\b|[+/*\-DIVMOD()]|[\d.]+", expression)
    new_expression = []

    for token in tokens:
        if token in variables:  # Variable
            value = variables[token]['value']
            if isinstance(value, list):  # Handle array variables separately
                raise ValueError(f"Array usage without index is not supported: {token}")
            new_expression.append(str(value))
        elif re.match(r"\b\w+\[\d+\]", token):  # Array access, e.g., numbers[2]
            var_name, index = re.findall(r"(\w+)\[(\d+)\]", token)[0]
            index = int(index) - 1  # Assuming 1-based indexing
            if var_name not in variables or 'bounds' not in variables[var_name] or variables[var_name]['value'][index] is None:
                raise ValueError(f"Invalid array access or uninitialized array element: {token}")
            new_expression.append(str(variables[var_name]['value'][index]))
        else:  # Operator, number, or parentheses
            new_expression.append(token.replace('DIV', '//').replace('MOD', '%'))

    return " ".join(new_expression)

def infix_to_rpn(expression):
    output_queue = deque()
    operator_stack = []

    tokens = expression.split()

    for token in tokens:
        if is_number(token):
            output_queue.append(token)
        elif token in ops:
            while (operator_stack and precedence[operator_stack[-1]] >= precedence[token]):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            top_token = operator_stack.pop()
            while top_token != '(':
                output_queue.append(top_token)
                top_token = operator_stack.pop()

    while operator_stack:
        output_queue.append(operator_stack.pop())

    return list(output_queue)


def evaluate_rpn(rpn):
    stack = []

    for token in rpn:
        if is_number(token):
            stack.append(float(token) if '.' in token else int(token))
        else:
            if len(stack) < 2:
                raise ValueError("Invalid expression")
            b, a = stack.pop(), stack.pop()
            if token == '//':  # Integer division
                stack.append(a // b)
            elif token == '%':  # Modulus
                stack.append(a % b)
            else:
                stack.append(ops[token](a, b))

    return stack[0]

    

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
    evaluated_parts = []
    # Split the expression by '+' but treat quoted strings as single tokens to avoid splitting inside them
    expression_parts = re.split(r'(\+)', expression)

    arithmetic_mode = False  # Flag to track whether we are in arithmetic mode or not

    for part in expression_parts:
        part = part.strip()
        if part == '+':
            evaluated_parts.append(part)  # Keep the plus sign for now and decide later based on context
            continue

        # Check if the part is a string literal
        if part.startswith('"') and part.endswith('"'):
            evaluated_parts.append(part[1:-1])  # Remove quotes and add to result
            arithmetic_mode = False  # Exiting arithmetic mode
        else:
            # Attempt to preprocess and evaluate potential arithmetic expression
            preprocessed_part = preprocess_expression(part)
            try:
                # If the part represents a valid arithmetic expression, evaluate it
                result = str(evaluate_rpn(infix_to_rpn(preprocessed_part)))
                if evaluated_parts and evaluated_parts[-1] == '+':
                    if arithmetic_mode:
                        # If in arithmetic mode, perform addition
                        evaluated_parts[-2] = str(ops['+'](int(evaluated_parts[-2]), int(result)))
                        evaluated_parts.pop()  # Remove the last '+'
                    else:
                        evaluated_parts[-1] = result  # Replace '+' with the arithmetic result
                else:
                    evaluated_parts.append(result)
                arithmetic_mode = True  # Entering arithmetic mode
            except Exception as e:
                # If preprocessing or evaluation fails, treat as a non-arithmetic expression
                print(Fore.RED + f'Error processing expression part "{part}": {str(e)}')
                return ""

    return ''.join(evaluated_parts)

