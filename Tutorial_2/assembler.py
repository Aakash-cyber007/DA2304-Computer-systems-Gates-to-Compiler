import sys

class Parser:
    def __init__(self, filepath):
        with open(filepath, 'r') as f:
            # Strip whitespace and remove comments
            self.lines = []
            for line in f:
                clean_line = line.split('//')[0].strip()
                if clean_line:
                    self.lines.append(clean_line)
        self.current_command = ""
        self.current_line_index = -1

    def has_more_commands(self):
        return self.current_line_index + 1 < len(self.lines)

    def advance(self):
        self.current_line_index += 1
        self.current_command = self.lines[self.current_line_index]

    def command_type(self):
        if self.current_command.startswith('@'):
            return 'A_COMMAND'
        elif self.current_command.startswith('(') and self.current_command.endswith(')'):
            return 'L_COMMAND'
        else:
            return 'C_COMMAND'

    def symbol(self):
        if self.command_type() == 'A_COMMAND':
            return self.current_command[1:]
        elif self.command_type() == 'L_COMMAND':
            return self.current_command[1:-1]
        return ""

    def dest(self):
        if '=' in self.current_command:
            return self.current_command.split('=')[0]
        return "null"

    def comp(self):
        temp = self.current_command
        if '=' in temp:
            temp = temp.split('=')[1]
        if ';' in temp:
            temp = temp.split(';')[0]
        return temp

    def jump(self):
        if ';' in self.current_command:
            return self.current_command.split(';')[1]
        return "null"


class Code:
    _dest_map = {
        "null": "000", "M": "001", "D": "010", "MD": "011",
        "A": "100", "AM": "101", "AD": "110", "AMD": "111"
    }
    
    _jump_map = {
        "null": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
        "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
    }
    
    _comp_map = {
        "0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100",
        "A": "0110000", "M": "1110000", "!D": "0001101", "!A": "0110001",
        "!M": "1110001", "-D": "0001111", "-A": "0110011", "-M": "1110011",
        "D+1": "0011111", "A+1": "0110111", "M+1": "1110111", "D-1": "0001110",
        "A-1": "0110010", "M-1": "1110010", 
        "D+A": "0000010", "A+D": "0000010", # Added A+D
        "D+M": "1000010", "M+D": "1000010", # Added M+D
        "D-A": "0010011", "D-M": "1010011", "A-D": "0000111", "M-D": "1000111",
        "D&A": "0000000", "A&D": "0000000", # Added A&D
        "D&M": "1000000", "M&D": "1000000", # Added M&D
        "D|A": "0010101", "A|D": "0010101", # Added A|D
        "D|M": "1010101", "M|D": "1010101"  # Added M|D
    }

    @classmethod
    def dest(cls, mnemonic):
        return cls._dest_map.get(mnemonic, "000")

    @classmethod
    def comp(cls, mnemonic):
        return cls._comp_map.get(mnemonic, "0000000")

    @classmethod
    def jump(cls, mnemonic):
        return cls._jump_map.get(mnemonic, "000")


class SymbolTable:
    def __init__(self):
        self.table = {
            "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
            "SCREEN": 16384, "KBD": 24576
        }
        for i in range(16):
            self.table[f"R{i}"] = i

    def add_entry(self, symbol, address):
        self.table[symbol] = address

    def contains(self, symbol):
        return symbol in self.table

    def get_address(self, symbol):
        return self.table[symbol]


def assemble(filepath):
    # Pass 1: Build the Symbol Table with ROM addresses for Labels
    parser1 = Parser(filepath)
    symbol_table = SymbolTable()
    rom_address = 0
    
    while parser1.has_more_commands():
        parser1.advance()
        if parser1.command_type() in ('A_COMMAND', 'C_COMMAND'):
            rom_address += 1
        elif parser1.command_type() == 'L_COMMAND':
            symbol = parser1.symbol()
            if not symbol_table.contains(symbol):
                symbol_table.add_entry(symbol, rom_address)

    # Pass 2: Translate to binary and handle variable RAM allocation
    parser2 = Parser(filepath)
    out_filepath = filepath.replace('.asm', '.hack')
    next_ram_address = 16  # Custom variables map starting here 
    
    with open(out_filepath, 'w') as out_file:
        while parser2.has_more_commands():
            parser2.advance()
            cmd_type = parser2.command_type()
            
            if cmd_type == 'A_COMMAND':
                symbol = parser2.symbol()
                if symbol.isdigit():
                    address = int(symbol)
                else:
                    if not symbol_table.contains(symbol):
                        symbol_table.add_entry(symbol, next_ram_address)
                        next_ram_address += 1
                    address = symbol_table.get_address(symbol)
                
                # Convert to 16-bit binary
                binary_out = f"{address:016b}"
                out_file.write(binary_out + '\n')
                
            elif cmd_type == 'C_COMMAND':
                comp_bits = Code.comp(parser2.comp())
                dest_bits = Code.dest(parser2.dest())
                jump_bits = Code.jump(parser2.jump())
                
                # C-instruction prefix is 111
                binary_out = f"111{comp_bits}{dest_bits}{jump_bits}"
                out_file.write(binary_out + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <file.asm>")
    else:
        assemble(sys.argv[1])
        print("Assembly complete.")