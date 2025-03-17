import REG_INFO
import sys
import re

def remove_color_codes(input_file):
    # Define the regex pattern for ANSI color codes
    ansi_escape_pattern = re.compile(r'\x1B\[[0-?9;]*[mK]')
    
    with open(input_file, 'r') as file:
        cleaned_content = ansi_escape_pattern.sub('', file.read())
    
    with open(input_file, 'w') as file:
        file.write(cleaned_content)

def main():
    # Step 1: Capture output in output.txt and console
    with open('output.txt', 'a') as f:
        original_stdout = sys.stdout  # Save a reference to the original standard output
        sys.stdout = f  # Redirect standard output to the file
        REG_INFO.main()  # Call the main function from REG_INFO.py
        sys.stdout.flush()  # Ensure everything is written before resetting stdout
        sys.stdout = original_stdout  # Reset standard output to its original value

    # Step 2: Remove ANSI color codes
    remove_color_codes('output.txt')

if __name__ == "__main__":
    main()
