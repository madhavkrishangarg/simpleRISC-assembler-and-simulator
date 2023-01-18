import sys

memory = {}

def float_bin(my_number):
    integer, fraction = str(my_number).split(".")
    integer = int(integer)
    out = str(bin(integer)).replace('0b', '')+"."
    while True:
        fraction = str('0.') + str(fraction)
        if float(fraction)==0:
            break
        temp = '%1.20f' % (float(fraction) * 2)
        integer, fraction = temp.split(".")
        out += integer
    return out

def bit_3(n):
    return '{0:03b}'.format(n)

def bit_5(x):
    while len(x)!=5:
        x=x+"0"
    return x

def binaryToDecimal(x):
    return int(x, 2)

def fraction(x):
    num=0
    for i in range(len(x)):
        num+=int(x[i])*(1/(2**(i+1)))
    return num



def bit_16(n):
    return '{0:016b}'.format(n)


def bit_8(n):
    return '{0:08b}'.format(n)


def binaryToDecimal(x):
    return int(x, 2)


reg_val = {'000': 0, '001': 0, '010': 0, '011': 0, '100': 0, '101': 0, '110': 0, "111": 0}

pc = 0


def dump():
    for reg in reg_val.keys():
        if(reg_val[reg] is float):
             
            integer, fraction = reg_val[reg].split(".")
            integer = int(integer)
            out = str(bin(integer)).replace('0b', '')+"."
            while True:
                fraction = str('0.') + str(fraction)
                if float(fraction)==0:
                    break
                temp = '%1.20f' % (float(fraction) * 2)
                integer, fraction = temp.split(".")
                out += integer

            str_bin=float_bin(out)                #calculating ieee
            l=str_bin.split(".")
            i=len(l[0])-1
            bit_exp=bit_3(i)
            x=l[0][1:]+l[-1][:5]

            bit_mantissa=bit_5(x[:5])

            print(bit_exp + bit_mantissa)
            

        else:
            print(bit_16(reg_val[reg]), end=" ")


def flag_reset():
    reg_val["111"] = 0

inputs=[]

for line in sys.stdin:
    if line!="" and line!="\n":
        inputs.append(line.strip())

while (inputs[pc] != "0101000000000000"):
    print(bit_8(pc), end=" ")
    inst = inputs[pc]
    op_code = inst[:5]
    reg1 = inst[7:10]
    reg2 = inst[10:13]
    reg3 = inst[13:]

    if (op_code == "00000"):  #addf
        reg_val[reg3] = reg_val[reg2] + reg_val[reg1]
        if reg_val[reg3] > 252:
            reg_val[reg3] = reg_val[reg3] % 252
            reg_val["111"] = 8
        else:
            flag_reset()
        pc += 1

    if (op_code == "00001"):  #subf
        reg_val[reg3] = reg_val[reg1] - reg_val[reg2]
        if reg_val[reg3] < 1:
            reg_val[reg3] = 1
            reg_val["111"] = 8
        else:
            flag_reset()
        pc += 1


    if (op_code == "10000"):  # add
        reg_val[reg3] = reg_val[reg2] + reg_val[reg1]
        if reg_val[reg3] > 65535:
            reg_val[reg3] = reg_val[reg3] % 65536
            reg_val["111"] = 8
        else:
            flag_reset()
        pc += 1
    if (op_code == "10001"):  # sub
        reg_val[reg3] = reg_val[reg1] - reg_val[reg2]
        if reg_val[reg3] < 0:
            reg_val[reg3] = 0
            reg_val["111"] = 8
        else:
            flag_reset()
        pc += 1
    if (op_code == "10110"):  # mul
        reg_val[reg3] = reg_val[reg1] * reg_val[reg2]
        if reg_val[reg3] > 65535:
            reg_val[reg3] = reg_val[reg3] % 65536
            reg_val["111"] = 8
        else:
            flag_reset()
        pc += 1
    if (op_code == "11010"):  # xor
        reg_val[reg3] = reg_val[reg1] ^ reg_val[reg2]
        flag_reset()
        pc += 1
    if (op_code == "11011"):  # or
        reg_val[reg3] = reg_val[reg2] or reg_val[reg1]
        flag_reset()
        pc += 1
    if (op_code == "11100"):  # and
        reg_val[reg3] = reg_val[reg2] and reg_val[reg1]
        flag_reset()
        pc += 1
    reg = inst[5:8]
    imm = binaryToDecimal(inst[8:])

    if (op_code == "10010"):  # movi
        reg_val[reg] = imm
        flag_reset()
        pc += 1

    reg = inst[5:8]

    exp=binaryToDecimal(inst[8:11])    #ieee to bin
    whole="1"+ inst[11:]
    frac= inst[11:]

    dec_whole=binaryToDecimal(whole)    #bin to dec
    dec_frac=fraction(frac)
    dec=dec_whole+dec_frac

    if(op_code == "00010"):  #movf
        reg_val[reg] = dec
        flag_reset()
        pc+=1

    if (op_code == "11000"):  # rs
        reg_val[reg] = reg_val[reg] >> imm
        flag_reset()
        pc += 1
    if (op_code == "11001"):  # ls
        reg_val[reg] = reg_val[reg] << imm
        if reg_val[reg] > 65535:
            reg_val[reg] = reg_val[reg] % 65536
            reg_val["111"] = 8
        else:
            flag_reset()
        pc += 1
    reg1 = inst[10:13]
    reg2 = inst[13:]
    if (op_code == "10011"):  # movr
        reg_val[reg2] = reg_val[reg1]
        flag_reset()
        pc += 1
    if (op_code == "10111"):  # divide
        reg_val["000"] = reg_val[reg1] // reg_val[reg2]
        reg_val["001"] = reg_val[reg1] % reg_val[reg2]
        flag_reset()
        pc += 1
    if (op_code == "11101"):  # invert
        reg_val[reg2] = 65535 - reg_val[reg1]
        flag_reset()
        pc += 1
    if (op_code == "11110"):  # compare
        if (reg_val[reg1] > reg_val[reg2]):
            reg_val["111"] = 2
        if (reg_val[reg1] < reg_val[reg2]):
            reg_val["111"] = 4
        if (reg_val[reg1] == reg_val[reg2]):
            reg_val["111"] = 1
        pc += 1
    reg = inst[5:8]
    mem = inst[8:]
    if (op_code == "10100"):  # load
        if (mem not in memory.keys()):
            memory[mem] = 0
        reg_val[reg] = memory[mem]
        flag_reset()
        pc += 1
    if (op_code == "10101"):  # store
        memory[mem] = reg_val[reg]
        flag_reset()
        pc += 1
    mem = binaryToDecimal(inst[8:])
    if op_code == "11111":  # jmp
        flag_reset()
        pc = mem

    if op_code == "01100":  # jlt
        if (reg_val["111"] == 4):
            pc = mem
        else:
            pc += 1
        flag_reset()
    if op_code == "01101":  # jgt
        if (reg_val["111"] == 2):
            pc = mem
        else:
            pc += 1
        flag_reset()
    if op_code == "01111":  # je
        if (reg_val["111"] == 1):
            pc = mem
        else:
            pc += 1
        flag_reset()
    dump()
    print()

flag_reset()
print(bit_8(pc), end=" ")
dump()
print()
for i in range(0, 256):
    if (i < len(inputs)):
        print(inputs[i])
    else:
        key=bit_8(i)
        if(key in memory.keys()):
            print(bit_16(memory[key]))
        else:
            print("0000000000000000")