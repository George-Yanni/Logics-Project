import re
import csv
import os

def extract_registers_from_atdf(atdf_content, output_csv, mcu_name):
    # Regex pattern to match lines with 'register caption' and extract the register name
    pattern = r'<register\s+caption="[^"]+"\s+name="([^"]+)"'

    # Find all matches in the ATDF content
    register_names = re.findall(pattern, atdf_content)

    # Append to the CSV file
    with open(output_csv, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write the register names with the second column as 'Register' and third column as MCU name
        for name in register_names:
            csv_writer.writerow([name, 'Register', mcu_name])

def process_all_atdf_files(base_directory, output_csv):
    # Open the CSV file once and write the header
    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write the header
        csv_writer.writerow(['Register Name', 'Register', 'MCU'])

    # Walk through all directories and files in the base_directory
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith(".atdf"):
                # Full file path
                atdf_file_path = os.path.join(root, file)
                
                # Extract MCU name from the filename (everything before .atdf)
                mcu_name = os.path.splitext(file)[0]
                
                # Reading the ATDF file content
                with open(atdf_file_path, 'r') as file_content:
                    atdf_content = file_content.read()

                # Extract registers and append to CSV
                extract_registers_from_atdf(atdf_content, output_csv, mcu_name)

# Sample usage
base_directory = 'C:/Users/Yanni/Desktop/Logics Project/ALL AVR MCUs/avr-mcu-master/packs'
output_csv = 'ALL_AVR_REGISTERS.csv'

# Process all ATDF files and save to CSV
process_all_atdf_files(base_directory, output_csv)

print(f'Registers extracted from all ATDF files and saved to {output_csv}')
