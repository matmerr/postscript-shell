import re

# Flip this for verbose error handling
debugging = False

### Functions for the Operand Stack
OpStack = list()

def opPop():
    try:
        obj = OpStack.pop();
        return obj
    except Exception as ex:
        print("opPop: \tcannot pop, empty stack")
        debug("\tException Error: ", ex)
    return
    
# adds the argument to the Operator Stack
def opPush(add):
    OpStack.append(add)
    return


### Functions fot the Dictionary Stack
DictStack = list()

# Pop the dictionary from the hot end, i.e. DictStack[-1]
def dictPop():
    try:
        dic = DictStack.pop();
        return dic
    except Exception as ex:
        print("dictPop: \tcannot pop, empty stack")
        debug("\tException Error: ", ex)
    return

# Push a dictionary on the dictionary stack
def dictPush(dic):
    DictStack.append(dic)
    return

# This function defines a variable with a value, and adds it to the hot
# dictionary in the dictionary stack
def define(name, value):
    dic = dictPop();
    dic[name] = value
    dictPush(dic)
    return

# This function loops through every dictionary in the dictionary stack, 
# and returns the corresponding value to a supplied name.
# If the name doesn't exist, boolean False is returned indicating
# the name does not exist in the dictionary stack
def lookup(name):
    for dictionary in reversed(DictStack):
        if name in dictionary:
            return dictionary[name]
    return False
    
    
### Arithmetic Operators

# This function pops the top two items in the operator stack, and pushes
# the sum back to the operand stack
def add():
    op1 = opPop()
    op2 = opPop()
    try:
        opPush(op2 + op1)
    except Exception as ex:
        print("add: \terror in addition")
        debug("\tException Error: ", ex)
    return


# This function pops the top two items in the operator stack, and pushes
# the difference back to the operand stack
def sub():
    op1 = opPop()
    op2 = opPop()
    try:
        opPush(op2 - op1)
    except Exception as ex:
        print("sub: \terror in subtraction")
        debug("\tException Error: ", ex)
    return

# This function pops the top two items in the operator stack, 
# and pushes the product back to the operand stack
def mul():
    op1 = opPop()
    op2 = opPop()
    try:
        opPush(op2 * op1)
    except Exception as ex:
        print("mul: \terror in multiplication")
        debug("\tException Error: ", ex)
    return

# This function pops the top two items in the operator stack, 
# and pushes the quotient back to the operand stack
def div():
    op1 = opPop()
    op2 = opPop()
    try:
        opPush(op2 / op1)
    except Exception as ex:
        print("div: \terror in division")
        debug("\tException Error: ", ex)
    return

# This function pops the top two items in the operator stack, 
# and pushes the remainder back to the operand stack
def mod():
    op1 = opPop()
    op2 = opPop()
    try:
        opPush(op2 % op1)
    except Exception as ex:
        print("mod: \terror in modulus")
        debug("\tException Error: ", ex)
    return


### String Manipulation Operators

# this function pops the hot string from the operator stack,
# and pushes the length of the string back to the operator stack
def length():
    s1 = opPop()
    try:
        opPush(len(s1))
    except Exception as ex:
        print("length: \tstring error")
        debug("\tException Error: ", ex)
    return


# this function pops off an index and a string from the operator stack,
# then returns the character at the index in the string to the operator stack
def get():
    index = opPop()
    string = opPop()
    try: 
        opPush(string[index])
    except Exception as ex:
        print("get: \terror in getting string index")
        debug("\tException Error: ", ex)
    return

# this function pops off an index, a char, and a string from the operator stack, 
# and replaces the char at the index in the string with the char supplied from the stack
def put():
    place = opPop()
    index = opPop()
    string = opPop()
    try: 
        # create new string with all chars leading up to index, insert place char, 
        # add remaining chars in string
        s = string[:index] + place + string[index+1:]
        opPush(s)
    except Exception as ex:
        print("get: \terror in replacing string index")
        debug("\tException Error: ", ex)
    return

# This function pops off a character count, an index and a string. Creates
# a substring of length count, starting at string index, and pushes it back
# back to the stack.
def getinterval():
    count = opPop()
    index = opPop()
    string = opPop()

    try:
        s = string[index:index+count]
        opPush(s)
    except Exception as ex:
        print("get: \terror in getting string interval")
        debug("\tException Error: ", ex)
    return
    

### Stack Manipulation Operators

# This function pops the hot item from the operator stack,
# then pushes back twice to create a duplicate. (Duplicates the hot item)
def dup():
    top = opPop()
    try:
        opPush(top)
        opPush(top)
    except Exception as ex: 
        print("dup: \terror in duplication")
        debug("\tException Error: ", ex)
    return

# This function pops the two hottest items from the operator stack, swaps them
# then pushes them back to the stack in the swapped order
def exch():
    first = opPop()
    second = opPop()
    try:
        opPush(first)
        opPush(second)
    except Exception as ex:
        print("exch: \terror in exchange")
        debug("\tException Error: ", ex)
    return


# This function pops two integers from the operator stack. 
# One indicates how many integers in the stack are going to be rolled,
# and the other indicates how far the integers are going to be rolled
def roll():

    PositionCount = opPop()
    TopCount = opPop()  # "roll top 5 (top) by 2 positions (PositionCount)"

    global OpStack

    try:
        elements = OpStack[(TopCount * -1):]
        OpStack = OpStack[:(TopCount * -1)]

        # roll forwards (positive movement), move the last element to the front, delete the last element
        if PositionCount > 0:
            for i in range(0, PositionCount):
                elements.insert(0,elements[-1])
                elements.pop()
            OpStack = OpStack + elements

        # roll backwards, move the first element to the back, delete the first element
        else:
            for i in range(0, abs(PositionCount)):
                elements.append(elements[0])
                elements.pop(0)
            OpStack = OpStack + elements

    except Exception as ex:
        print("roll: \terror in rolling ")
        debug("\tException Error: ", ex)
        
    return

# This function pops an index from the top of the stack, then copies the 
# n amount of items back on to the stack, as supplied by the popped index
def copy():
    index = opPop()

    try:
        for i in range(0, index):
            opPush(OpStack[-1 * index])     # length of the string

    except Exception as ex:
        print("copy: \tfailure in copying")
        debug("\tException Error: ", ex)
    return


# this function clears both dictionary and operator stack
def clear():
    OpStack.clear()
    DictStack.clear()
    return


# this function prints the operator stack to the console
def stack():
    for op in reversed(OpStack):
        print(op)



### Dictionary Manipulation Operators

# pop dictionary from operand stack, and put it on the dictionary stack
def begin():
    dictionary = opPop()
    dictPush(dictionary)
    return

# pops the hot dictionary from the dictionary stack
def end():
    try:
        dict = DictStack.pop();
    except Exception as ex:
        print("pop: \tcannot pop, empty stack")
        debug("\tException Error: ", ex)
    return 

# This function assumes there is a dictionary already on the dictionary stack. 
# It pops the hot dictionary from the dictionary stack, then pops a value and
# a variable from the operand stack. The variable is paired with the value in the 
# dictionary, then the dictonary is re-pushed to the dictionary stack
def psDef():
    
    if len(DictStack) == 0:
        dictionary = {}
    else:
        dictionary = dictPop()

    value = opPop()
    variable = opPop()
    try:
        dictionary[variable] = value
        dictPush(dictionary)
    except Exception as ex:
        print("psDef: \terror in variable declaraton")
        debug("\tException Error: ", ex)
    
    return


# creates a dictionary and puts it on the OpStack,
def psDict():
    size = opPop()
    dictionary = dict()
    opPush(dictionary)
    return 


        
### Test Cases

# This tests all arithmetic operators define above in the "Arithmetic Operators" region
def testArithmeticOperators():
    clear()

    global DictStack
    global OpStack

    # 1 + 2 = 3
    opPush(1)
    opPush(2)
    add()
    if opPop() != 3: return False

    # 3 - 1 = 2
    opPush(3)
    opPush(1)
    sub()
    if opPop() != 2: return False

    # 2 - (-1) = 3
    opPush(2)
    opPush(-1)
    sub()
    if opPop() != 3: return False

    # 3 * 4 = 12
    opPush(3)
    opPush(4)
    mul()
    if opPop() != 12: return False

    # -7 * 0 = 0
    opPush(-7)
    opPush(0)
    mul()
    if opPop() != 0: return False

    # 12 / (-3) = (-4)
    opPush(12)
    opPush(-3)
    div()
    if opPop() != -4: return False

    # 16 / 5 = 3.2
    opPush(16)
    opPush(5)
    div()
    if opPop() != 3.2: return False

    # 5 / 16 = 3.2
    opPush(5)
    opPush(16)
    div()
    if opPop() != .3125: return False
    
    # -4 % -3 = -1
    opPush(-4)
    opPush(-3) 
    mod()
    if opPop() != -1: return False

    # 3 % 3 = -1
    opPush(3)
    opPush(3) 
    mod()
    if opPop() != 0: return False


    # ((3 * 4) + (8 / 4) + (10 - 6)) % 7 = 4
    opPush(3)
    opPush(4)
    mul()
    opPush(8)
    opPush(4)
    div()
    opPush(10)
    opPush(6)
    sub()
    add()
    add()
    opPush(7)
    mod()
    if opPop() != 4: return False

    return True


# This function tests the string operators defined in the "String Operators" region above
def testStringOperators():
    
    # Test string length with space
    opPush("CPT_S Three Fifty 5")
    length()
    if opPop() != 19: return False

    #Test generic get
    opPush("CPT_S Three Fifty 5")
    opPush(3)
    get()
    if opPop() != '_': return False

    # Test reverse index
    opPush("CPT_S Three Fifty 5")
    opPush(-1)
    get()
    if opPop() != '5': return False

    # Test put
    opPush("CPT_S Three Fifty 5")
    opPush(3)
    opPush(' ')
    put()
    if opPop() != "CPT S Three Fifty 5": return False

    # test getinterval with spaces
    opPush("CPT_S Three Fifty 5")
    opPush(6)
    opPush(11)
    getinterval()
    if opPop() != "Three Fifty": return False

    return True


# This function tests the string operators defined in the "Stack Manipulation Operators" region above
def testStackManipulationOperators():
    
    # test dup
    opPush(2)
    dup()
    if opPop() != 2: return False
    if opPop() != 2: return False

    # test exch
    # stack contans 1 2 where 2 is the hot end, 
    # swap the top two, then first popped should be 1 then 2
    opPush(1)
    opPush(2)
    exch()
    if opPop() != 1: return False
    if opPop() != 2: return False

    #test opPop
    opPush(1)
    if opPop() != 1: return False

    clear()
    #test roll forwards
    opPush(4)
    opPush(3)
    opPush(2)
    opPush(1)

    opPush(3)
    opPush(1)
    roll()
    global OpStack
    answer = [2,3,1,4]
    if len(set(OpStack).intersection(answer)) != 4: return False

    # using the previous set, test roll backwards
    opPush(3)
    opPush(-1)
    answer = [1,2,3,4]
    if len(set(OpStack).intersection(answer)) != 4: return False

    # roll all integers by more than one slot
    opPush(4)
    opPush(2)
    answer = [3,4,1,2]
    if len(set(OpStack).intersection(answer)) != 4: return False

    clear()
    #test copy function
    opPush(4)
    opPush(3)
    opPush(2)
    opPush(1)
    opPush(2) # copy two items from the hot end of stack, to the hot end
    copy()
    answer = [4,3,2,1,2,1]

    # four characters overlap between the answer and the OpStack,
    # but there should be two occurrances of 1 and 2 in the OpStack

    if len(set(OpStack).intersection(answer)) != 4: return False 
    if OpStack.count(2) != 2: return False  
    if OpStack.count(1) != 2: return False

    clear()
    if len(OpStack) != 0: return False

    return True


# This function tests the string operators defined in the "Dictionary Manipulation Operators" region above
def testDictionaryManipulationOperators():

    opPush(1)   #set dictionary size
    psDict()    # create dictionary of size on the operator stack
    begin()     # move dictionary from op stack to dictionary stack
    opPush("n1")    # push "n1" to OpStack
    opPush(3)       # push 3 top OpStack
    psDef()         # pop "n1" and 3, create definition in hot dictionary in dictionary stack
    if lookup("n1") != 3: return False  # lookup in dictionary stack
        
    if len(DictStack) != 1: return False    #one dictionary exists in DictStack
    end()   #pop hot dictionary from dictionary stack
    if len(DictStack) != 0: return False

    clear()

    return True


## Begin Parsing Functions

def tokenize(s):
    return re.findall("/?[a-zA-Z][a-zA-Z0-9_]*|[(][\w \W]*[)]|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)


# Creates a sublist of sequential items starting with the curly brace, 
# ommitting the curly brace. 
# If the curly braces are not properly nested, returns False.
def groupMatching(it):
    res = []
    for c in it:
        if c=='}':
            return res
        elif c== '{':
            # recursivly build sub code-array
            res.append(groupMatching(it))       
        else:
            try:
                # element is a number, convert to int and add
                res.append(int(c))

            except:
                # element is a number, just add
                res.append(c) 
    return res

# Follows the postfix for loop specifications 
def psFor():
    proc = opPop()
    lim = opPop()
    incr = opPop()
    init = opPop()
    
    for i in range(init,lim,incr):
        opPush(i)
        parse(proc)

 
# global dictionary of all functions contained in this program
functions = {
    'add': add,
    'sub': sub,
    'mul': mul,
    'div': div,
    'mod' : mod,
    'length' : length,
    'get' : get,
    'put' : put,
    'getinterval' : getinterval,
    'dup' : dup,
    'exch' : exch,
    'pop' : opPop,
    'roll' : roll,
    'copy' : copy,
    'clear' : clear,
    'dict' : psDict,
    'begin' : begin,
    'end' : end,
    'def' : psDef,
    'for' : psFor,
    'stack' : stack
    }


# Parse checks to see if the argument is a string or a code array, as
# psFor() may send a code array if a code array is nested.
def parse(s):
    # a for loop with a code array may pass 
    if (type(s) is str):
        tokens = tokenize(s)
    else:
        tokens = s
    iterator = tokens.__iter__()
    tokenList = groupMatching(iterator)

    interpreter(tokenList)


# This function calls interpret, but instead accepts an entire list of tokens. 
def interpreter(tokenList):
    for element in tokenList:
        interpret(element)


# Accepts a single element in a code array, or the list of tokens.
# If a code array is nested, when called, this function 
# recursively calls the parent function interpreter to parse that sub
# list of tokens. Only accepts one element as an argument.
def interpret(element):

    # if element is a list, push to stack
    if type(element) is list:
        opPush(element)
        
    # if element is one of the preset functions, call it
    elif element in functions:
        functions[element]()

    else:
        try:
            # element is a number
            opPush(int(element))
        except:
                
            # element is a variable
            if element[0] == '/':
                opPush(element[1:])

            # element is a string
            elif element[0] == '(':
                opPush(element[1:-1])
                
            # element is in the dictionary stack
            elif lookup(element) != False:

                # get definition of variable in stack
                elementDefinition = lookup(element)

                # element defintion is a code array, recursively run the code array
                if type(elementDefinition) is list:
                    interpreter(elementDefinition)

                # element defition is just a regular variable
                else:
                    opPush(lookup(element))

    
# Various test cases for the parsing functions
def testParsing():

    parse('''(git commit -m "done") length''')
    if opPop() != 20: return False

    parse('''/divmod {
                dup 3 2 roll 
                dup 3 1 roll 
                div 3 1 roll 
                mod
            }def 
            4 6 divmod''')
    if opPop() != 2: return False
    if opPop() != 1.5: return False

    parse('''1 1 5 {10 mul} for''')
    if opPop() != 40: return False

    parse('''clear /test''')
    if opPop() != "test": return False

    parse('''20 5 1 1 roll div''')
    if opPop() != 4: return False

    parse('''/a 1 def 
            0 dict 
                begin 
                    /a 2 def 
                    a 
                end''')
    if opPop() != 2: return False

    parse('''/a 
            {2 2 mul}def    
            a''')
    if opPop() != 4: return False

    parse('''/fact{ 
            0 dict 
                begin 
                    /n exch def 
                    1 
                    n -1 1 {mul} for 
                end 
            }def 
            (factorial function !) 0 9 getinterval 
            5 fact''')
    if opPop() != 120 : return False
    if opPop() != "factorial": return False

    return True


# used for reporting verbose exceptions when they are thrown
def debug(*s): 
    if debugging: 
        print(*s)
    return ""


if __name__ == '__main__':


    print("Postscript Shell")
    print("Type 'quit' to quit")
    while(True):
        print(":> ", end="")
        
        s = input()
        if (s == "quit"):
            break;
        parse(s)


