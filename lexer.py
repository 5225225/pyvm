# This is meant to strip out every comment and parse stdin into a list of
# Commands, put it into json, and print it to stdout.  Memory addresses are
# unchanged, and once support for variables are added, They will be either
# declared at the top of the list, or put into a seperate list.

import json
import sys

import cmdio
from cmdio import Command


def decomment(commands):
    output = []
    for item in commands:
        if item == "":
            output.append("#")
        elif item.startswith("#"):
            output.append("#")  # Magic value, read on line 30
        elif "#" in item:
            output.append(item[:item.find("#")])
        else:
            output.append(item)
    return output
if len(sys.argv) == 2:
    infile = decomment(open(sys.argv[1]).read().strip().split("\n"))
else:
    infile = decomment(sys.stdin.read().strip().split("\n"))

commands = []

for index, item in enumerate(infile, start=1):
    line = index
    if not item == "#":
        opcode = item.split(" ")[0]
        arguments = item.split(" ")[1:]
        while "" in arguments:
            arguments.remove("")
        intargs = []
        for item in arguments:
            if item.startswith("$"):
                intargs.append(int(item[1:], 16))
            elif item.startswith("%"):
                intargs.append(int(item[1:], 2))
            elif item.startswith("0"):
                intargs.append(int(item[1:], 8))
            else:
                intargs.append(int(item))
        cmd = Command(line, opcode, intargs)
        commands.append(cmd)


sys.stdout.write(cmdio.jsonencode(commands))
