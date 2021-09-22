#!/usr/bin/python3
import sys


COMP_MAP = {
    "0": "0101010",
    "M": "1110000",
    "D": "0001100",
    "D-M": "1010011",
}

DST_MAP = {
    "0": "000",
    "D": "010",
    "M": "001",
}

JUMP_MAP = {
    "0": "000",
    "JGT": "001",
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
for i in range(15):
    SYMBOL_MAP[f"R{i}"] = i

RAM_ADDR = 16


def main(args):
    """Main function of assembler."""
    translated_lines = []
    with open(args[0]) as f:
        kept_lines = initialize_symbols(f)
        for line in kept_lines:
            if line.startswith("@"):
                translated_lines.append(f"{assemble_a_command(line)}\n")
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


def assemble_a_command(line):
    """Assemble A command."""
    constant = line[1:]
    if constant.isdigit():
        return f"{int(constant):b}".zfill(16)
    if constant not in SYMBOL_MAP:
        SYMBOL_MAP[constant] = RAM_ADDR
        RAM_ADDR += 1
    return f"{SYMBOL_MAP[constant]:b}".zfill(16)


def assemble_c_command(line):
    """Assemble C command."""
    if ";" in line:
        print(line)
        print(COMP_MAP["0"])
        return f"111{COMP_MAP[line[0]]}{DST_MAP['0']}{JUMP_MAP[line[2:]]}"
    return f"111{COMP_MAP[line[2:]]}{DST_MAP[line[0]]}{JUMP_MAP['0']}"


if __name__ == '__main__':
    main(sys.argv[1:])
