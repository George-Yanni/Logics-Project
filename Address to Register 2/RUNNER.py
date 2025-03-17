import subprocess
import argparse

def run_command(addresses):
    # Prepare commands in bulk for efficiency
    commands = [
        [
            "python", 
            "./AVR_ASM_ANALYZER.py",
            "--datasheet", "C:/Users/Yanni/Desktop/328pFULL.PDF", 
            "--mcu", "atmega328p", 
            "--csv", "C:/Users/Yanni/Desktop/Logics Project/Address To Register/DETAILED_AVR.csv", 
            "--address", address
        ]
        for address in addresses
    ]

    # Execute commands in parallel to improve speed
    processes = [subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for command in commands]

    # Capture the output
    for process in processes:
        stdout, stderr = process.communicate()
        if stdout:
            print(stdout.decode())
        if stderr:
            print(stderr.decode())

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Fetch data for specified addresses.")
    parser.add_argument(
        "--addresses", 
        nargs='+',  # Accept multiple addresses
        help="List of addresses to fetch data for (e.g. 0x33 0x39 0x40 0x20)",
        required=True  # This argument is required
    )

    # Parse arguments
    args = parser.parse_args()
    
    # Pass the list of addresses to the run_command function
    run_command(args.addresses)
