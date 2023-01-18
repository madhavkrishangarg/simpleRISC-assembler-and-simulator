from re import L
from sys import stdin
import sys

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


# Changes an integer into 8 bit binary and returns the value as a string
def decimalToBinary(n,line_counter):
    assert n[0]=="$",f" Error! in line {line_counter} ,integer not declared with a '$' sign." 
    n = int(str(n)[1::])
    bnr = bin(int(n)).replace('0b', '')
    x = bnr[::-1]
    while len(x) < 8:
        x += '0'
    bnr = x[::-1]
    return bnr
def decimalToBinary2(n):
    bnr = bin(int(n)).replace('0b', '')
    x = bnr[::-1]
    while len(x) < 8:
        x += '0'
    bnr = x[::-1]
    return bnr

#   Checks if all the variables are declared at the begining and if they are not being used before declaration
def check_var(inp_lists):
    line_count=0
    var_list=[]
    var_index=[]
    for i in range(0,len(inp_lists)):
        inp_lists[i]=inp_lists[i].split()
        if(inp_lists[i][0]=="var"):
            var_list.append(inp_lists[i][-1])
            var_index.append(i)
    for i in inp_lists:
        line_count+=1
        if((i[0]=="st" or i[0]=="ld") and i[-1].isalpha() and i[-1] not in var_list):
            assert False,f"variable used before reference in line {line_count}"
    if len(var_list)!=0:
        if sorted(var_index) != list(range(0, max(var_index)+1)):
            assert False,"Error! Variables not declared at beginning ."
        else:
            return True
def check_hlt(inp_lists1):
    assert (inp_lists1[-1]!="hlt\n") or inp_lists1[-1][-3:]!="hlt","hlt not in the last line"
    for i in  range(len(inp_lists1)-1):
        if inp_lists1[i]==inp_lists1[-1]:
            assert False,f"hlt declared before the last line at line {i+1}"
              
# Dictionary of operands , registers, and variables
dict0 = {"add": "10000", "movf":"00010" , "addf":"00000" , "subf":"00001", "sub": "10001", "ld": "10100", "st": "10101", "mul": "10110",
         "div": "10111", "rs": "11000", "ls": "11001", "xor": "11010", "or": "11011", "and": "11100", "not": "11101",
         "cmp": "11110", "jmp": "11111", "jlt": "01100", "jgt": "01101", "je": "01111", "hlt": "01010",
         "mov":"erprev"
         }
reg = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110" , "r0": "000", "r1": "001", "r2": "010", "r3": "011", "r4": "100", "r5": "101", "r6": "110"}
labels={}
# Initialising some objects
list_inputs=[]
sen="hihihihi"
variables = {}
mem_adrr={}
outputs=[]
mem1=0
line_counter=1


# Dividing the operations into 5 basic categeries on basis of different things
op1 = ["add", "addf" , "subf" ,"sub", "mul", "xor", "or", "and"]
op2 = ["div", "not", "cmp"]
op3 = ["jmp", "jlt", "jgt", "je"]
op4 = ["rs", "ls"]
op5 = ["ld", "st"]


# This function  converts a proper instruction into 16-bit binary assembly code
def convert(sen,line_counter):
    sen_list = [x for x in sen.split()]
    assert sen_list[0] in dict0 , f"Syntax Error! in line {line_counter} Operator not present in ISO"
    if sen_list[0] != "mov":
        sen_list_assem = [dict0[sen_list[0]]]
    else:
        if sen_list[2] in reg:
            sen_list_assem = ["10011"]
        else:
            sen_list_assem = ["10010"]
    if sen_list[0] in op1:
        assert len(sen_list) == 4, f"General syntax Error at line  {line_counter}! Invalid number of operands."
        
        sen_list_assem.append("00")
        for i in range(3):
            assert sen_list[i+1] in reg, f"Syntax Error! at line {line_counter} register not present in ISO"
            sen_list_assem.append(reg[sen_list[i + 1]])
    elif sen_list[0] in op2:
        assert len(sen_list) == 3, f"General syntax Error at line {line_counter}! Invalid number of operands."

        sen_list_assem.append("00000")
        for i in range(2):
            assert sen_list[i+1] in reg, f"Syntax Error! at line {line_counter} register not present in ISO"
            sen_list_assem.append(reg[sen_list[i + 1]])
    elif sen_list[0] in op3:

        assert len(sen_list) == 2, f"General syntax Error at line {line_counter}! Invalid number of operands."

        assert sen_list[1]  in labels,f"Error!, at line {line_counter} wrong name for  label"
        sen_list_assem.append("000")
        sen_list_assem.append(labels[sen_list[1]])
    elif sen_list[0] in op4:

        assert len(sen_list) == 3, f"General syntax Error at line {line_counter}! Invalid number of operands."

        assert sen_list[1] in reg, f"Syntax Error! at at line {line_counter} register not present in ISO"
        sen_list_assem.append(reg[sen_list[1]])
        assert  0<=int(sen_list[2][1::])<256,f"Error! , the illiegal immideate value at line {line_counter}"
        sen_list_assem.append(decimalToBinary(sen_list[2],line_counter))
    elif sen_list[0] in op5:

        assert len(sen_list) == 3, f"General syntax Error at line {line_counter}! Invalid number of operands."

        assert sen_list[1] in reg, f"Syntax Error! at line {line_counter} register not present in ISO"
        sen_list_assem.append(reg[sen_list[1]])
        assert sen_list[2] in variables,f"Error!, at line {line_counter} Variable not declared"
        sen_list_assem.append(variables[sen_list[2]])
    elif sen_list[0] == "hlt":

        assert len(sen_list) == 1, f"General syntax Error at line {line_counter}! Invalid number of operands."

        sen_list_assem.append("00000000000")
    elif sen_list[0] == "mov":

        assert len(sen_list) == 3, f"General syntax Error at line {line_counter}! Invalid number of operands."

        if sen_list[2] not in reg:
            assert sen_list[1] in reg, f"Syntax Error! at line {line_counter} register not present in ISO"
            sen_list_assem.append(reg[sen_list[1]])
            assert  0<=int(sen_list[2][1::])<256,f"Error! ,at line {line_counter} the illiegal immideate value"
            sen_list_assem.append(decimalToBinary(sen_list[2],line_counter))
        elif sen_list[1]!="FLAGS":
            sen_list_assem.append("00000")
            assert sen_list[1] in reg, f"Syntax Error! at line {line_counter} register not present in ISO"
            sen_list_assem.append(reg[sen_list[1]])
            assert sen_list[2] in reg, f"Syntax Error! at line {line_counter} register not present in ISO"
            sen_list_assem.append(reg[sen_list[2]])
        else:
            sen_list_assem.append("00000")
            assert ((sen_list[1] in reg) or (sen_list[1]=="FLAGS")), f"Syntax Error! at line {line_counter} register not present in ISO"
            sen_list_assem.append("111")
            sen_list_assem.append(reg[sen_list[2]])

    
            
    elif sen_list[0]=="movf":
        yajat = ""
        integer, fraction = str(sen_list[2]).split(".")
        integer = int(integer[1:])
        out = str(bin(integer)).replace('0b', '')+"."
        while True:
            fraction = str('0.') + str(fraction)
            if float(fraction)==0:
                break
            temp = '%1.20f' % (float(fraction) * 2)
            integer, fraction = temp.split(".")
            out += integer    

        str_bin=float_bin(sen_list[2][1:])                #calculating ieee
        l=str_bin.split(".")
        i=len(l[0])-1
        bit_exp=bit_3(i)
        x=l[0][1:]+l[-1][:5]
        bit_mantissa=bit_5(x[:5])

        
            
        assert len(out)<7 ,f"Invalid number on line {line_counter}."
        sen_list_assem.append(reg[sen_list[1]])
        sen_list_assem.append(bit_exp)
        sen_list_assem.append(bit_mantissa)

 

    elif sen_list[0]=="addf":

        yajat =""
        
        yajat += ("00000")
        yajat+=(reg[sen_list[1]])
        yajat+=(reg[sen_list[2]])
        yajat+=(reg[sen_list[3]])

        print(yajat)

    elif sen_list[0]=="subf":
        
        yajat =""
        
        yajat += ("00001")
        yajat+=(reg[sen_list[1]])
        yajat+=(reg[sen_list[2]])
        yajat+=(reg[sen_list[3]])
        print(yajat)

    outputs.append("".join(sen_list_assem))

# Taking inputs in loops and saving them in list_inputs
for line in stdin:
    if line!="" and line!="\n":
        list_inputs.append(line)


# Assigning memory adresses to variables and labels and addiding them to dicts
for sen in list_inputs:
    if sen.split()[0] != "var":
        if sen.split()[0][-1]==':':
            labels[sen.split()[0][0:-1]]=decimalToBinary2(mem1)
            mem1+=1
        else:    
            mem_adrr[sen]=decimalToBinary2(mem1)
            mem1+=1
for sen in list_inputs:
    if sen.split()[0] == "var":
        assert sen.split()[1] not in variables,f"Variable redeclaration error at line {len(variables)+1}"
        variables[sen.split()[1]]=decimalToBinary2(mem1)
        mem1+=1
line_counter+=len(variables)


#   Checking for proper declaration of variables, presence of hlt and memory overflow errors.
list_inputs_check=list_inputs.copy()
list_inputs_check_2=list_inputs.copy()
check_var(list_inputs_check)
check_hlt(list_inputs_check)
# print(list_inputs)
assert list_inputs[-1]=="hlt\n" or list_inputs[-1][-3:]!="hlt","last line is not halt"
assert mem1<257,"Memory overflow Error! , too many instructions for the ISO to handle"

#   Converting to bin-codes
for sen in list_inputs:
    if sen.split()[0] != "var" and sen.split()[0][0:-1] not in labels:
        convert(sen,line_counter)
        line_counter+=1
    elif sen.split()[0][::-1][0]==":":
        label_inp=sen.split()
        label_inp.pop(0)
        r=" ".join(label_inp)
        convert(r,line_counter)
        line_counter+=1

#    Printing the output
for x in outputs:
    sys.stdout.write(x)
    sys.stdout.write("\n")