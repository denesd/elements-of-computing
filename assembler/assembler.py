#!/usr/bin/python3
import sys


COMP_MAP = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101",
}

DST_MAP = {
    "0": "000",
    "D": "010",
    "M": "001",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111",
}

JUMP_MAP = {
    "0": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}

SYMBOL_MAP = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
}
for i in range(16):
    SYMBOL_MAP[f"R{i}"] = i

RAM_ADDR = 16


def main(args):
    """Main function of assembler."""
    translated_lines = []
    with open(args[0]) as f:
        kept_lines = initialize_symbols(f)
        ram_addr = 16
        for line in kept_lines:
            if line.startswith("@"):
                ram_addr, tline = assemble_a_command(line, ram_addr)
                translated_lines.append(f"{tline}\n")
            else:
                translated_lines.append(f"{assemble_c_command(line)}\n")
    output = args[1] if len(args) > 1 else "Prog.hack"
    with open(output, "w") as f:
        f.writelines(translated_lines)


def initialize_symbols(f):
    """Initialize symbols into a symbol table."""
    kept_lines = []
    rom_addr = 0
    for line in f.readlines():
        line = line.strip("\n")
        if line.startswith("//") or line == "":
            continue
        line = line.split("//")[0].strip()
        if line.startswith("("):
            SYMBOL_MAP[line[1:-1]] = rom_addr
        else:
            rom_addr += 1
            kept_lines.append(line)
    return kept_lines


def assemble_a_command(line, ram_addr):
    """Assemble A command."""
    constant = line[1:]
    if constant.isdigit():
        return ram_addr, f"{int(constant):b}".zfill(16)
    if constant not in SYMBOL_MAP:
        SYMBOL_MAP[constant] = ram_addr
        ram_addr += 1
    return ram_addr, f"{SYMBOL_MAP[constant]:b}".zfill(16)


def assemble_c_command(line):
    """Assemble C command."""
    if ";" in line:
        comp, jmp = line.split(";")
        return f"111{COMP_MAP[comp]}{DST_MAP['0']}{JUMP_MAP[jmp]}"
    dst, comp = line.split("=")
    return f"111{COMP_MAP[comp]}{DST_MAP[dst]}{JUMP_MAP['0']}"


if __name__ == '__main__':
    main(sys.argv[1:])
