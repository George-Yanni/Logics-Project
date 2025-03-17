import re

def parse_registers(lines):
    """Parse the register information and return a mapping of addresses to descriptions, captions, bitfields, and values."""
    register_info = {}
    current_address = None
    mcu_name = None
    module_name = None
    register_name = None
    caption = None
    bitfields = []
    values = []
    in_bitfields_section = False
    in_values_section = False

    for line in lines:
        # Match possible register entry (case insensitive)
        address_match = re.search(r'Possible Register\(s\) For address (0x[0-9A-Fa-f]+):', line, re.IGNORECASE)
        if address_match:
            if current_address:
                # Store previous register information before moving to a new address
                store_register_info(register_info, current_address, module_name, register_name, caption, bitfields, values)
            
            current_address = address_match.group(1).lower()  # Store addresses in lowercase for consistency
            # Reset variables for new register info
            mcu_name = None
            module_name = None
            register_name = None
            caption = None
            bitfields = []
            values = []
            in_bitfields_section = False
            in_values_section = False
            continue

        # If we are currently processing a register info section
        if current_address:
            # Look for register captions and module name (case insensitive)
            if 'MCU:' in line:
                mcu_name = line.split('MCU: ')[1].strip()  # Extract the MCU name
            if 'Module:' in line:
                module_name = line.split('Module: ')[1].strip()  # Extract the Module name
            if 'Register:' in line:
                register_name = line.split('Register: ')[1].strip()  # Extract the Register name
            if 'Caption:' in line:
                caption = line.split('Caption: ')[1].strip()  # Extract the Caption
            
            # Capture bitfields
            if 'Bitfields:' in line:
                in_bitfields_section = True
                continue
            
            if in_bitfields_section:
                if line.strip() == '':  # Skip empty lines
                    continue
                if 'Values:' in line:  # Transition to values section
                    in_bitfields_section = False
                    in_values_section = True
                    continue
                # Capture bitfield information
                bitfield_match = re.match(r'^\s*-\s*Bit (\d+): (.+)', line.strip())
                if bitfield_match:
                    bitfields.append(f"Bit {bitfield_match.group(1)}: {bitfield_match.group(2)}")
                continue
            
            # Capture values
            if in_values_section:
                if line.strip() == '':  # Skip empty lines
                    continue
                if '********************************************************************************' in line:  # End of the register section
                    store_register_info(register_info, current_address, module_name, register_name, caption, bitfields, values)
                    current_address = None  # Reset current address after processing
                    continue
                values.append(line.strip())  # Capture values

    return register_info

def store_register_info(register_info, current_address, module_name, register_name, caption, bitfields, values):
    """Helper function to store register information in the dictionary."""
    bitfields_string = ", ".join(bitfields) if bitfields else "No Bitfields"
    values_string = ", ".join(values) if values else "No Values"
    full_description = f"{module_name}_{register_name} ({caption}, Bitfields: [{bitfields_string}], Values: [{values_string}])"
    
    if current_address not in register_info:
        register_info[current_address] = []
    register_info[current_address].append(full_description)

def analyze_functions(lines, register_info):
    """Extract function analysis lines and replace addresses with their descriptions."""
    function_analysis = []
    function_line_pattern = re.compile(r'In function .*::', re.IGNORECASE)

    for line in lines:
        # Check if the line is a function analysis line
        if function_line_pattern.match(line):
            function_analysis.append(line)  # Add the function line directly
            continue  # Skip further processing for function lines

        # Replace addresses in register-related lines with their descriptions (case insensitive)
        original_line = line  # Keep original line for comparison
        for address, descriptions in register_info.items():
            if address in original_line.lower():  # Compare in lowercase for case insensitivity
                # Prepare description string, concatenate descriptions for the same address
                description_string = ' or '.join(descriptions)
                line = line.replace(address, description_string)

        # If the line is relevant to function analysis, add it
        if 'suspected dealing with internal register' in line.lower() or 'detected, may impact control registers' in line.lower():
            function_analysis.append(line)

    return function_analysis

def analyze_output_file(input_file, output_file):
    """Main function to analyze the output file."""
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Parse register information
    register_info = parse_registers(lines)

    # Analyze function lines and replace addresses with descriptions
    function_analysis = analyze_functions(lines, register_info)

    # Write the analyzed output to a new file
    with open(output_file, 'w') as file:
        for line in function_analysis:
            file.write(line)

# Specify the input and output file names
input_file = 'output.txt'
output_file = 'analyzed_output.txt'

# Run the analysis
analyze_output_file(input_file, output_file)

print("Analysis complete. Check analyzed_output.txt for results.")
