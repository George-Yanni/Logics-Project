import os
import fitz  # type: ignore
import re
import csv
import argparse
from colorama import init, Fore, Style  # type: ignore
from difflib import get_close_matches  # Import for suggesting similar MCUs

# Initialize colorama for colorful output in cmd
init(autoreset=True)

# Compile regex patterns once
address_pattern = re.compile(r'0x[0-9A-Fa-f]+', re.IGNORECASE)
register_pattern = re.compile(r'\b[A-Z][A-Z0-9_]+\b', re.IGNORECASE)

def clear_screen():
    """Clear the command prompt screen.""" 
    os.system('cls' if os.name == 'nt' else 'clear')

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def search_address_positions(text):
    """Find all addresses in the text and return them separately."""
    addresses = [normalize_hex_address(m.group()) for m in address_pattern.finditer(text)]
    positions = [m.start() for m in address_pattern.finditer(text)]
    return addresses, positions

def normalize_hex_address(address):
    """Normalize the hexadecimal address to ensure even number of digits."""
    address = address.lower().strip()  # Make it lowercase and strip any extra spaces
    if not address.startswith('0x'):
        address = '0x' + address
    address = address[2:]  # Remove '0x' prefix
    address = address.zfill(((len(address) + 1) // 2) * 2)  # Pad to even length
    return '0x' + address.upper()  # Re-attach '0x' and make it uppercase

def extract_register_names_from_context(context):
    """Extract register names from the context around the address."""
    return register_pattern.findall(context)

def get_register_names_from_address(text, address):
    """Get all potential register names for a given address from the PDF text."""
    address = normalize_hex_address(address)  # Normalize the address
    address_matches = [m.start() for m in re.finditer(re.escape(address), text, re.IGNORECASE)]
    register_names_list = []

    for match in address_matches:
        context = get_context_around_address(text, match, context_chars=25)
        register_names = extract_register_names_from_context(context)
        register_names_list.extend(register_names)

    return register_names_list

def get_context_around_address(text, address_position, context_chars=25):
    """Get context around the given address position."""
    start = max(address_position - context_chars, 0)
    end = min(address_position + context_chars, len(text))
    return text[start:end]

def address_from_register_name(text, register_name):
    """Retrieve address for a given register name."""
    register_name_pattern = re.compile(rf'\b{re.escape(register_name)}\b', re.IGNORECASE)
    matches = list(register_name_pattern.finditer(text))

    if matches:
        addresses, _ = search_address_positions(text)
        for match in matches:
            context = get_context_around_address(text, match.start(), context_chars=25)
            for addr in addresses:
                if addr in context:
                    return addr  # Return the first matched address
    return None

def verify_register_names_for_address(text, address):
    """Verify register names for a given address."""
    address = normalize_hex_address(address)  # Normalize the address
    register_names = get_register_names_from_address(text, address)

    suspected_matches = []
    for reg_name in list(set(register_names)):
        register_address = address_from_register_name(text, reg_name)
        
        if register_address == address:
            suspected_matches.append(reg_name)
        else:
            suspected_matches.append(reg_name)

    return suspected_matches

def load_mcus_from_csv(csv_path):
    """Load all MCU names from the CSV file."""
    mcu_names = set()
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mcu_names.add(row['MCU'].lower())
    return mcu_names

def load_register_names_from_csv(csv_path):
    """Load register names from the CSV file."""
    register_names = set()
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            register_names.add(row['RegisterName'])
    return register_names

def filter_actual_registers(suspected_matches, actual_register_names):
    """Filter suspected matches to only include actual register names."""
    return [reg for reg in suspected_matches if reg in actual_register_names]

def find_nearest_mcu(provided_mcu, available_mcus):
    """Find the most similar MCUs to the provided MCU name."""
    return get_close_matches(provided_mcu.lower(), available_mcus, n=3, cutoff=0.6)  # Adjust n and cutoff as needed

def print_match_details(microcontroller, csv_file, actual_matches, address_to_check):
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)

        found_any = False
        for row in reader:
            register_name = row['RegisterName']
            mcu_name = row['MCU'].lower()
            register_address = row['RegisterAddress'].strip()

            # Check if the register name matches any in actual_matches and the MCU matches the input microcontroller
            if register_name in actual_matches and mcu_name == microcontroller.lower():
                found_any = True
                print(Fore.GREEN + f"MCU: {row['MCU']}")
                print(Fore.GREEN + f"Module: {row['ModuleName']}")
                print(Fore.GREEN + f"Register: {row['RegisterName']}")
                print(Fore.GREEN + f"Caption: {row['RegisterCaption']}")
                
                # Compare addresses
                if address_to_check == register_address:
                    print(Fore.GREEN + f"Address: {register_address}")  # Print one if addresses are the same
                else:
                    print(Fore.GREEN + f"Addresses: {address_to_check}, {register_address}")  # Print both if different
                
                # Split bitfields and values by lines
                bitfields = row['Bitfields'].split(';')  # Assuming bitfields are separated by ';'
                values = row['Values'].split(';')  # Assuming values are separated by ';'

                print(Fore.GREEN + "Bitfields:")
                for bitfield in bitfields:
                    print(Fore.GREEN + f"  - {bitfield.strip()}")  # Print each bitfield on a new line
                
                print(Fore.GREEN + "Values:")
                for value in values:
                    print(Fore.GREEN + f"  - {value.strip()}")  # Print each value on a new line
                
                print(Fore.RED + "*" * 80)  # Separator for readability
        
        if not found_any:
            print(Fore.RED + f"No registers found for address {address_to_check}")

def main():
    clear_screen()
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Microcontroller Register Checker")
    parser.add_argument('--datasheet', required=True, help="Path to the PDF file")
    parser.add_argument('--mcu', required=True, help="Microcontroller model name")
    parser.add_argument('--csv', required=True, help="Path to the CSV file with register details")
    parser.add_argument('--address', required=True, help="Address to check for registers")

    # Parse arguments
    args = parser.parse_args()

    # Load MCU names from the CSV
    csv_file = args.csv
    available_mcus = load_mcus_from_csv(csv_file)

    # Check if the provided MCU exists
    microcontroller = args.mcu
    if microcontroller.lower() not in available_mcus:
        # Warn user that MCU is not found and suggest closest matches
        print(Fore.YELLOW + f"Warning: MCU '{microcontroller}' is not supported.")
        nearest_mcus = find_nearest_mcu(microcontroller, available_mcus)
        
        if nearest_mcus:
            print(Fore.YELLOW + "The closest available MCUs are:")
            for mcu in nearest_mcus:
                print(Fore.CYAN + f"  - {mcu}")
            # Use the closest match for further processing
            microcontroller = nearest_mcus[0]  # You can adjust how you want to handle it
            print(Fore.YELLOW + f"Proceeding with closest MCU '{microcontroller}'.")
        else:
            print(Fore.RED + "No similar MCUs found. Exiting.")
            return

    # Extract PDF text once
    pdf_path = args.datasheet
    text = extract_text_from_pdf(pdf_path)

    # Verify register names
    address_to_check = normalize_hex_address(args.address)  # Normalize the address
    suspected_matches = verify_register_names_for_address(text, address_to_check)

    # Load actual register names from CSV
    actual_register_names = load_register_names_from_csv(csv_file)

    # Filter suspected matches
    actual_matches = filter_actual_registers(suspected_matches, actual_register_names)

    print(Fore.BLUE + f"Possible Register(s) For address {address_to_check}:")
    print_match_details(microcontroller, csv_file, actual_matches, address_to_check)

if __name__ == "__main__":
    main()
