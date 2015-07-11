import sys
import json

import cmdio
from cmdio import Command

EXTRA = True


def jb(p1, p2):
    p1 = int(p1)
    p2 = int(p2)
    count = 0
    count = count + p1 * 256
    count = count + p2
    return count


def splitbytes(x):
    try:
        x = int(x)
    except ValueError:
        return x
    p1 = x // 256
    p2 = x - (p1 * 256)
    return(p1, p2)


def listin(lst, check):
    for item in lst:
        if check in item:
            return True
    return False


def search(line, argnumber):
    addr = 0
    for item in commands:
        if str(item.line) == str(line.arguments[argnumber]):
            break
        addr = addr + item.size
    else:
        sys.stderr.write("{}: Could not find line number {}\n".format(
                         line.line, line.arguments[argnumber]))
    return(addr)


def searchnoerr(linenum):
    addr = 0
    for item in commands:
        if str(linenum) == str(item.line):
            break
        addr = addr + item.size
    return(addr)


opcodes = {
    "SET": 4,
    "JUMP": 5,
    "JUMPL": 5,
    "IFE": 6,
    "IFEL": 6,
    "ADD": 7,
    "SUB": 8,
    "GCHR": 9,
    "PCHR": 10,
}

commands = []

if len(sys.argv) == 2:
    with open(sys.argv[1]) as f:
        for item in cmdio.jsondecode(f.read()):
            commands.append(item)
else:
    with sys.stdin as f:
        for item in cmdio.jsondecode(f.read()):
            commands.append(item)

output = []


def out(*arg):
    global output
    for item in arg:
        try:
            if isinstance(item, tuple):
                for x in item:
                    output.append(x)
            elif isinstance(item, int):
                output.append(item)
            elif isinstance(item, str):
                try:
                    output.append(int(item))
                except ValueError:
                    output.append(item)
        except TypeError:
            output.append(item)
for cmd in commands:
    out(opcodes[cmd.opcode])
    if cmd.opcode == "SET":
        out(splitbytes(cmd.arguments[0]))
        out(cmd.arguments[1])
    elif cmd.opcode == "JUMP" or (EXTRA and cmd.opcode == "JUMPL"):
        if cmd.opcode == "JUMP":
            out(splitbytes(cmd.arguments[0]))
        if cmd.opcode == "JUMPL":
            out(splitbytes(search(cmd, 0)))
    elif cmd.opcode == "IFE" or (EXTRA and cmd.opcode == "IFEL"):
        out(splitbytes(cmd.arguments[0]))
        out(splitbytes(cmd.arguments[1]))
        if cmd.opcode == "IFE":
            out(splitbytes(cmd.arguments[2]))
        if cmd.opcode == "IFEL":
            out(splitbytes(search(cmd, 2)))
    elif cmd.opcode == "ADD" or cmd.opcode == "SUB":
        out(splitbytes(cmd.arguments[0]))
        out(splitbytes(cmd.arguments[1]))
    elif cmd.opcode == "GCHR":
        out(splitbytes(cmd.arguments[0]))
    elif cmd.opcode == "PCHR":
        out(splitbytes(cmd.arguments[0]))
strout = []
for item in output:
    if isinstance(item, int):
        strout.append(str(item))
    elif item.startswith("!"):
        linenum = item.split("+")[0][1:]
        offset = item.split("+")[1]
        for x in splitbytes(searchnoerr(linenum)+int(offset)):
            strout.append(str(x))
    else:
        strout.append(str(item))
print(json.dumps(strout))
