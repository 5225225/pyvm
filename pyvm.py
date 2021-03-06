import sys
import json
import tty
import termios

def jb(p1,p2):
    count = 0
    count = count + p1 * 256
    count = count + p2
    return count


DEBUG = True
prog_test = [1,0,6,5,0,7,1,0]
prog_mult = [5,0,8,10,10,1,0,9,7,0,3,0,4,8,0,7,0,5,6,0,7,0,6,0,255,5,0,8] #INPUTS: 3(num1),4(num2),7(num1 - 1) OUTPUTS: 3(result)
prog_test2 = [4,0,20,1,4,0,21,2,7,0,20,0,21,5,0,3,0,18]


memory = []
if len(sys.argv) == 2:
    for item in json.loads(open(sys.argv[1]).read()):
        memory.append(int(item))
else:
    for item in json.loads(sys.stdin.read()):
        memory.append(int(item))

#16 bits of addresses, 8 bits an address.
#TODO add overflow and underflow when incrementing and decrementing.

while len(memory) < 2**16:
    memory.append(0)

counter = 0
while True:
    command = memory[counter]
    args = []
    for x in range(1,8): #Easier then fixing the code that relied on instructions
        try:
            args.append(memory[counter + x])
        except IndexError:
            pass
    if DEBUG:
        sys.stdout.write(str(counter) + ":" + str(command) + ": ")
        if False: pass
        elif command == 4: #SET
            print("SET *{} TO {}".format(jb(args[0],args[1]),args[2]))
        elif command == 5: #JUMP
            print("JUMPED TO {}".format(jb(args[0],args[1])))
        elif command == 6:
            if memory[jb(args[0],args[1])] == memory[jb(args[2],args[3])]:
                print("*{}({}) WAS EQUAL TO *{}({}), JUMPED TO {}".format(jb(args[0],args[1]),memory[jb(args[0],args[1])],jb(args[2],args[3]),memory[jb(args[2],args[3])],jb(args[4],args[5])))
            else:
                print("*{}({}) WAS NOT EQUAL TO *{}({})".format(jb(args[0],args[1]),memory[jb(args[0],args[1])],jb(args[2],args[3]),memory[jb(args[2],args[3])]))
        elif command == 7:
            print("*{}({}) WAS ADDED TO *{}({}), LEAVING RESULT IN FIRST ADDRESS".format( jb(args[0],args[1]), memory[jb(args[0],args[1])], jb(args[2],args[3]), memory[jb(args[2],args[3])]))
        elif command == 8:
            print("*{}({}) WAS SUBTRACTED FROM *{}({}), LEAVING RESULT IN FIRST ADDRESS".format(jb(args[0],args[1]),memory[jb(args[0],args[1])],jb(args[2],args[3]),memory[jb(args[2],args[3])]))
        elif command == 9:
            pass
            #Moved debug to where it's run, or the gotten character would not display properly.
        elif command == 10:
            print("PRINTED *{}({}) TO STDERR".format(jb(args[0],args[1]),memory[jb(args[0],args[1])]))
        else:
            print("INVALID COMMAND")

    if False: pass
    elif command == 4: #SET
        memory[jb(args[0],args[1])] = args[2]
        counter = counter + 4
    elif command == 5: #JUMP
        counter = jb(args[0],args[1])
    elif command == 6:
        if memory[jb(args[0],args[1])] == memory[jb(args[2],args[3])]:
            counter = jb(args[4],args[5])
        else:
            counter = counter + 7
    elif command == 7:
        memory[jb(args[0],args[1])] += memory[jb(args[2],args[3])]
        counter = counter + 5
    elif command == 8:
        memory[jb(args[0],args[1])] -= memory[jb(args[2],args[3])]
        counter = counter + 5
    elif command == 9:
        fd = sys.stdin.fileno()
        try:
            old_settings = termios.tcgetattr(fd)
        except termios.error:
            print("Couldn't read one character, are you piping into stdin?")
            print("All of the commands support using a file instead of stdin")
            sys.exit(1)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        key = ord(ch)
        if key == 27:
            counter = 2**16 #Quit program on ESC key
        memory[jb(args[0],args[1])] = key
        if DEBUG: print("GOT A CHARACTER: {}, LEFT IT IN *{}".format(memory[jb(args[0],args[1])],jb(args[0],args[1])))
        counter = counter + 3
    elif command == 10:
        sys.stderr.write(chr(memory[jb(args[0],args[1])]))
        counter = counter + 3
    else:
        #Command not found, must be data. I have to increment the counter anyway
        counter = counter + 1
    if counter >= 2**16:
        memorydump= open("memory.bin","wb")
        memorydump.write(bytes(memory))
        sys.exit(0)
