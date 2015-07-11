import sys
import json


def jsonencode(commands):
    out = []
    for item in commands:
        out.append([item.line, item.opcode, item.arguments])
    return(json.dumps(out))


def jsondecode(jsonstring):
    out = []
    for item in json.loads(jsonstring):
        out.append(Command(item[0], item[1], item[2]))
    return out


class Command:
    def __init__(self, line, opcode, arguments):
        self.line = line
        self.opcode = opcode
        self.arguments = arguments
        self.size = -1

        if self.opcode == "SET":
            self.size = 4  # FORMAT: SET *x y
        elif self.opcode == "JUMP" or self.opcode == "JUMPL":
            self.size = 3  # FORMAT: JUMP *x
        elif self.opcode == "IFE" or self.opcode == "IFEL":
            self.size = 7  # FORMAT: IFE *x *y *z
        elif self.opcode == "ADD" or self.opcode == "SUB":
            self.size = 5  # FORMAT: ADD/SUB *x *y
        elif self.opcode == "GCHR":
            self.size = 3
        elif self.opcode == "PCHR":
            self.size = 3
        else:
            print(str(self.line) + ": Invalid opcode of " + str(self.opcode))
            sys.exit(1)
