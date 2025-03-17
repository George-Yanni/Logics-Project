import pandas as pd

class RAM:
    def __init__(self):
        RAM.DATA_TYPE_INTEGER = 0
        RAM.DATA_TYPE_STRING = 1
        RAM.DATA_TYPE_EXPRESSION = 2
        self.ram = pd.DataFrame(columns=['address', 'value', 'varName', 'dataType'])
        self.registers = {
            'R0': 0,
            'R1': 1,
            'R2': 2,
            'R3': 3,
            'R4': 4,
            'R5': 5,
            'R6': 6,
            'R7': 7,
            'R8': 8,
            'R9': 9,
            'R10': 10,
            'R11': 11,
            'R12': 12,
            'R13': 13,
            'R14': 14,
            'R15': 15,
        }

    def write(self, address, nBits, value, varName, dataType):
        nBytes = nBits // 8

        # Prepare the value for writing
        if dataType == RAM.DATA_TYPE_INTEGER:
            value_bytes = value.to_bytes(nBytes, 'little')

            # Writing each byte to RAM
            for i in range(nBytes):
                current_address = hex(int(address, 16) + i)
                if current_address in self.ram['address'].values:
                    self.ram.loc[self.ram['address'] == current_address, ['value', 'varName', 'dataType']] = [value_bytes[i], varName, dataType]
                else:
                    new_row = pd.DataFrame({
                        'address': [current_address],
                        'value': [value_bytes[i]],
                        'varName': [varName],
                        'dataType': [dataType]
                    })
                    self.ram = pd.concat([self.ram, new_row], ignore_index=True)

        elif dataType == RAM.DATA_TYPE_STRING:
            value_bytes = value.encode('utf-8')
            if len(value_bytes) < nBytes:
                value_bytes += b'\x00' * (nBytes - len(value_bytes))  # Pad with null bytes
            value_bytes = value_bytes[:nBytes]

            # Writing the string to RAM
            for i in range(nBytes):
                current_address = hex(int(address, 16) + i)
                if i < len(value_bytes):
                    # Decode byte, check for null byte
                    if value_bytes[i:i + 1] == b'\x00':
                        value_display = "GARBAGE"  # Set to GARBAGE for null bytes
                    else:
                        value_display = value_bytes[i:i + 1].decode('utf-8')  # Decode bytes to string
                else:
                    value_display = "GARBAGE"  # Set to GARBAGE for uninitialized addresses

                if current_address in self.ram['address'].values:
                    self.ram.loc[self.ram['address'] == current_address, ['value', 'varName', 'dataType']] = [value_display, varName, dataType]
                else:
                    new_row = pd.DataFrame({
                        'address': [current_address],
                        'value': [value_display],  # Store as string or 'GARBAGE'
                        'varName': [varName],
                        'dataType': [dataType]
                    })
                    self.ram = pd.concat([self.ram, new_row], ignore_index=True)

        elif dataType == RAM.DATA_TYPE_EXPRESSION:
            # Handle expression case
            value_str = value  # Keep the original expression as a string
            current_address = hex(int(address, 16))
            if current_address in self.ram['address'].values:
                self.ram.loc[self.ram['address'] == current_address, ['value', 'varName', 'dataType']] = [value_str, varName, dataType]
            else:
                new_row = pd.DataFrame({
                    'address': [current_address],
                    'value': [value_str],  # Store as string
                    'varName': [varName],
                    'dataType': [dataType]
                })
                self.ram = pd.concat([self.ram, new_row], ignore_index=True)

            # Fill subsequent addresses with "??"
            for i in range(1, nBytes):
                current_address = hex(int(address, 16) + i)
                if current_address not in self.ram['address'].values:
                    new_row = pd.DataFrame({
                        'address': [current_address],
                        'value': ['??'],  # Store as "??" for expression
                        'varName': [varName],
                        'dataType': [dataType]
                    })
                    self.ram = pd.concat([self.ram, new_row], ignore_index=True)

        # After writing the main value, fill remaining bytes with '??'
        for i in range(nBytes):
            next_address = hex(int(address, 16) + i)
            if next_address not in self.ram['address'].values:
                self.ram = pd.concat([self.ram, pd.DataFrame({'address': [next_address], 'value': ['??'], 'varName': [varName], 'dataType': [dataType]})], ignore_index=True)

        # Sorting by address to maintain order
        self.ram = self.ram.sort_values(by='address').reset_index(drop=True)

# Example usage
ram_sim = RAM()
ram_sim.write('0x39', 32, 256, 'var1', RAM.DATA_TYPE_INTEGER)  # Writing an integer value
ram_sim.write('0x43', 32, "AAA", 'var2', RAM.DATA_TYPE_STRING)     # Writing a string
ram_sim.write('0x50', 32, 'R0 + 4', 'var3', RAM.DATA_TYPE_EXPRESSION)  # Writing an expression as string

# Check RAM content
print(ram_sim.ram)
