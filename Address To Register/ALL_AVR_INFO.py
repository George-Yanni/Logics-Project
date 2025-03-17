import re
import csv
import os
import xml.etree.ElementTree as ET

def extract_registers_from_atdf(atdf_content, output_csv, mcu_name):
    # Parse the ATDF content as XML
    root = ET.fromstring(atdf_content)

    # Collect value groups for quick lookup
    value_groups = {}
    for value_group in root.findall(".//value-group"):
        group_name = value_group.get('name')
        values = {}
        for value in value_group.findall(".//value"):
            value_caption = value.get('caption')
            value_name = value.get('name')
            value_value = value.get('value')
            values[value_value] = value_caption
        value_groups[group_name] = values

    # Iterate over each module in the ATDF
    for module in root.findall(".//module"):
        module_name = module.get('name')
        
        # Iterate over each register group within the module
        for reg_group in module.findall(".//register-group"):
            # Iterate over each register within the register group
            for register in reg_group.findall(".//register"):
                register_name = register.get('name')
                register_caption = register.get('caption')  # Extract register caption
                register_address = register.get('offset')
                
                # Collect bitfield names, bit numbers, and descriptions
                bitfields = []
                values_description = []
                for bitfield in register.findall(".//bitfield"):
                    bit_name = bitfield.get('name')
                    bit_caption = bitfield.get('caption')
                    bit_mask = bitfield.get('mask')
                    bit_values = bitfield.get('values')

                    # Calculate the bit number from the bit mask
                    bit_number = calculate_bit_number(bit_mask)
                    
                    # Append bit name, number, and caption to the list
                    bitfields.append(f"Bit {bit_number}: {bit_name} - {bit_caption}")
                    
                    # If value group is specified, get values description
                    if bit_values and bit_values in value_groups:
                        values_description.append(f"{bit_name} Values: {', '.join([f'{v}: {desc}' for v, desc in value_groups[bit_values].items()])}")

                # Join all bitfields as a single string
                bitfields_description = "; ".join(bitfields)
                
                # Join all values descriptions as a single string
                values_description = "; ".join(values_description) if values_description else "No Values"

                # Write to the CSV file with the register caption and values description
                with open(output_csv, 'a', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([module_name, register_name, register_caption, register_address, bitfields_description, values_description, mcu_name])

def calculate_bit_number(bit_mask):
    # Convert hex mask to an integer, then calculate the position of the highest set bit
    mask_value = int(bit_mask, 16)
    bit_number = (mask_value).bit_length() - 1
    return bit_number

def process_all_atdf_files(base_directory, output_csv):
    # Open the CSV file once and write the header
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write the header, adding 'Values'
        csv_writer.writerow(['ModuleName', 'RegisterName', 'RegisterCaption', 'RegisterAddress', 'Bitfields', 'Values', 'MCU'])

    # Walk through all directories and files in the base_directory
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith(".atdf"):
                # Full file path
                atdf_file_path = os.path.join(root, file)
                
                # Extract MCU name from the filename (everything before .atdf)
                mcu_name = os.path.splitext(file)[0]
                
                # Reading the ATDF file content
                with open(atdf_file_path, 'r', encoding='utf-8') as file_content:
                    atdf_content = file_content.read()

                # Extract registers and append to CSV
                extract_registers_from_atdf(atdf_content, output_csv, mcu_name)

# Sample usage
base_directory = 'C:/Users/Yanni/Desktop/Logics Project/ALL AVR MCUs/avr-mcu-master/packs'
output_csv = 'DETAILED_AVR.csv'

# Process all ATDF files and save to CSV
process_all_atdf_files(base_directory, output_csv)

print(f'Registers, captions, bitfields, and values extracted from all ATDF files and saved to {output_csv}')
