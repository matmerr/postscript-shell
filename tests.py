from postscriptshell import *
import sys



if __name__ == '__main__':

    passedMsg = "%s passed"
    failedMsg = "%s failed"

    testCases = [("Arithmetic Operators", testArithmeticOperators()), 
                 ("String Operators", testStringOperators()),
                 ("Stack Manipulation",testStackManipulationOperators()),
                 ("Dictionary Manipulation",testDictionaryManipulationOperators()),
                 ("PostScript Parsing", testParsing())]
    
    

    for func in range(len(testCases)):
        if testCases[func][1]:
            print(passedMsg % testCases[func][0])
        else:
            print(failedMsg % testCases[func][0])
            sys.exit(1)

