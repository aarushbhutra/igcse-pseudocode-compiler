import sys
from interpreter import process_line
from colorama import init
from state_manager import variables

init(autoreset=True)

"""
TODO:
+ 2D arrays (setup, access, assignment)
"""

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <filename.pseudo>")
        return

    filename = sys.argv[1]
    if not filename.endswith(".pseudo"):
        print("Error: File must end with .pseudo")
        return

    try:
        with open(filename, 'r') as file:
            for line in file:
                process_line(line.strip())
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")

if __name__ == "__main__":
    main()
    print(variables)
