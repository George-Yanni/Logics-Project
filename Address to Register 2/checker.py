import fitz  # type: ignore
import re
from collections import Counter
from colorama import Fore, Style  # type: ignore

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def search_word_positions(text, word):
    """Find all positions of the word in the text."""
    pattern = re.compile(rf'\b{re.escape(word)}\b', re.IGNORECASE)
    positions = [m.start() for m in pattern.finditer(text)]
    return positions

def search_address_positions(text):
    """Find all addresses in the text and merge close addresses."""
    address_pattern = re.compile(r'0x[0-9A-Fa-f]+', re.IGNORECASE)
    addresses = [m.group() for m in address_pattern.finditer(text)]
    positions = [m.start() for m in address_pattern.finditer(text)]

    merged_addresses = []
    merged_positions = []

    if positions:
        current_address = addresses[0]
        current_position = positions[0]
        for i in range(1, len(positions)):
            if positions[i] - positions[i-1] <= 15:
                current_address = f"{current_address}, {addresses[i]}"
            else:
                merged_addresses.append(current_address)
                merged_positions.append(current_position)
                current_address = addresses[i]
                current_position = positions[i]
        # Add the last group
        merged_addresses.append(current_address)
        merged_positions.append(current_position)

    return merged_addresses, merged_positions

def find_nearest_address(word_positions, address_positions, addresses):
    """Find the nearest addresses to the keyword positions."""
    nearest_addresses = []
    for word_pos in word_positions:
        distances = [abs(word_pos - addr_pos) for addr_pos in address_positions]
        min_index = distances.index(min(distances))
        nearest_addresses.append((addresses[min_index], distances[min_index]))
    return nearest_addresses

def print_nearest_addresses(nearest_addresses):
    """Print the nearest addresses and compare with the most common address."""
    # Limit to nearest 5 addresses
    nearest_addresses = sorted(nearest_addresses, key=lambda x: x[1])[:5]

    # Print nearest addresses
    # print("\nNearest addresses to the keyword positions:")
    # for addr, dist in nearest_addresses:
    #     print(f"Nearest address: {addr}, Distance: {dist}")

    # Find the most repeated address among these 5
    addresses = [addr for addr, _ in nearest_addresses]
    most_common_address, most_common_count = Counter(addresses).most_common(1)[0]

    # Check if the nearest address is the same as the most repeated one
    nearest_address, _ = min(nearest_addresses, key=lambda x: x[1])

    if nearest_address == most_common_address or nearest_address == addresses[0]:
        print(f"{Fore.GREEN}Address is: {nearest_address}{Style.RESET_ALL}")
    # else:
    #     print(f"{Fore.YELLOW}Almost, address is: {nearest_address}, Please double check{Style.RESET_ALL}")

def analyze_pdf(pdf_path, search_word):
    """Main function to execute the logic."""
    text = extract_text_from_pdf(pdf_path)

    # Get positions of the keyword and addresses
    word_positions = search_word_positions(text, search_word)
    addresses, address_positions = search_address_positions(text)

    if not word_positions:
        print(f"{Fore.RED}Register Not Found!{Style.RESET_ALL}")
    else:
        # Find the nearest addresses
        nearest_addresses = find_nearest_address(word_positions, address_positions, addresses)

        # Print nearest addresses and compare
        print_nearest_addresses(nearest_addresses)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <pdf_path> <search_word>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    search_word = sys.argv[2]
    analyze_pdf(pdf_path, search_word)
