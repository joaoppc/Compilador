import sys

op = ['+','-','*','/']
white_space = ' '
lexeme = ''
lexeme2 = ''
number1 = ''
number2 = ''
posop = ''
numlist = []
for param  in sys.argv[1:] :
    for i, char in enumerate(param):
        if char != white_space:     
            lexeme += char
        if (i+1 < len(param)):
            if param[i+1] != white_space or param[i+1] in op or lexeme in op: # if next char == ' ':
                if char in op :
                    number1 = int(lexeme[:-1])
                    lexeme =''
                    numlist.append(number1)
                    print(number1)
    print(number1)