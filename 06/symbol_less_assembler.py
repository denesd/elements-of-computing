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


def main(args):
    """Main function of assembler."""
    translated_lines = []
    with open(args[0]) as f:
        for line in f.readlines():
            line = line.strip("\n")
            if line.startswith("//") or line == "":
                continue
            elif line[0] == "@":
                translated_lines.append(assemble_a_command(line))
            else:
                translated_lines.append(assemble_c_command(line))
    for translated in translated_lines:
        print(translated)


def assemble_a_command(line):
    """Assemble A command."""
    return f"{int(line[1:]):b}".zfill(16)


def assemble_c_command(line):
    """Assemble C command."""
    if ";" in line:
        return f"111{COMP_MAP['0']}{DST_MAP[line[0]]}{JUMP_MAP[line[2:]]}"
    return f"111{COMP_MAP[line[2:]]}{DST_MAP[line[0]]}{JUMP_MAP['0']}"


if __name__ == '__main__':
    main(sys.argv[1:])
