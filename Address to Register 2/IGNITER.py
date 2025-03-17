import re
from collections import defaultdict
import subprocess

# Define regex patterns for the AVR operations that likely deal with internal registers
patterns = {
    'in_out': re.compile(r'\b(in|out)\s+r\d+,\s*0x([0-9A-Fa-f]+)'),
    'sbi_cbi': re.compile(r'\b(sbi|cbi)\s+0x([0-9A-Fa-f]+),\s*(\d+)'),
    'lds_sts': re.compile(r'\b(lds|sts)\s+r\d+,\s*0x([0-9A-Fa-f]+)'),
    'ld_st': re.compile(r'\b(ld|st)\s+r\d+,\s*[XYZ]'),
    'sbiw_adiw': re.compile(r'\b(adiw|sbiw)\s+r\d+,\s*0x([0-9A-Fa-f]+)'),
    'bitwise_op': re.compile(r'\b(andi|ori)\s+r\d+,\s*0x([0-9A-Fa-f]+)'),
    'cli_sei': re.compile(r'\b(cli|sei)\b')
}

# Dictionary for instruction descriptions
instruction_descriptions = {
    'in': "loads a value from an I/O register",
    'out': "stores a value to an I/O register",
    'sbi': "sets a bit in an I/O register",
    'cbi': "clears a bit in an I/O register",
    'lds': "loads a value from a data space address",
    'sts': "stores a value to a data space address",
    'ld': "loads a value from the address pointed by a register",
    'st': "stores a value to the address pointed by a register",
    'adiw': "adds an immediate value to a register pair",
    'sbiw': "subtracts an immediate value from a register pair",
    'andi': "performs a bitwise AND with an immediate value",
    'ori': "performs a bitwise OR with an immediate value",
    'cli': "disables global interrupts",
    'sei': "enables global interrupts"
}

def parse_asm(file_path):
    findings = defaultdict(list)  # Store findings grouped by function
    suspected_addresses = set()  # Use a set to avoid duplicates

    with open(file_path, 'r') as f:
        lines = f.readlines()

    current_function = None  # Track the current function

    for line in lines:
        # Check for function labels
        if re.match(r'^\s*\w+\s*<\w+>:', line):
            current_function = line.strip()  # Capture the current function label

        # Search for patterns in each line
        for op_type, pattern in patterns.items():
            match = pattern.search(line)
            if match:
                address = match.group(2) if op_type in {'in_out', 'sbi_cbi', 'lds_sts', 'sbiw_adiw', 'bitwise_op'} else None
                if op_type in {'in_out', 'sbi_cbi', 'lds_sts', 'sbiw_adiw', 'bitwise_op'}:
                    instruction = match.group(1)
                    description = instruction_descriptions[instruction]
                    findings[current_function].append(f"'{instruction}' instruction ({description}) suspected dealing with internal register at address 0x{address}")
                    if address: 
                        suspected_addresses.add(f"0x{address}")

                elif op_type == 'ld_st':
                    instruction = line.split()[0]  # Get the instruction from the line
                    description = instruction_descriptions.get(instruction, "unknown instruction")
                    findings[current_function].append(f"'{instruction}' instruction ({description}) suspected dealing with internal register via pointer")

                elif op_type == 'cli_sei':
                    instruction = match.group(0)  # Capture cli or sei
                    description = instruction_descriptions[instruction]
                    findings[current_function].append(f"'{instruction}' ({description}) detected, may impact control registers")

    # Write findings grouped by function to the output file
    with open("output.txt", 'w') as output_file:  # Changed to write mode to avoid appending
        for func, results in findings.items():
            output_file.write(f"\nIn function {func}:\n")
            output_file.writelines(f" - {result}\n" for result in results)

    # Run the runner script with suspected addresses if there are any
    if suspected_addresses:
        run_runner_script(suspected_addresses)

def run_runner_script(addresses):
    # Create the command to run the RUNNER.py script with the suspected addresses
    command = ["python", "C:/Users/Yanni/Desktop/Logics Project/RUNNER.py", "--addresses"] + list(addresses)

    # Run the command and capture the output
    subprocess.run(command, check=True, capture_output=True, text=True)

# Example usage
if __name__ == "__main__":
    asm_file_path = "C:/Users/Yanni/Desktop/Logics Project/output.asm"
    parse_asm(asm_file_path)
    print("Analysis Done!")
