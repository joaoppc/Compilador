import sys

op = ['+','-','*','/']
white_space = ' '
lexeme = ''
number1 = ''
aspa ="'"
numlist = []
opseq=[]
for param  in sys.argv[1:] :
    for i, char in enumerate(param):
        if char != white_space: 
            lexeme += char
            if char in op or char == aspa:
                if char == aspa:
                    pass
                else:
                    opseq.append(char)
                number1 = lexeme[:-1]
                lexeme =''
                numlist.append(number1)
    
numlist = numlist[1:]
numlist.reverse()
opseq.reverse()
while len(opseq)> 0:
    #print(len(numlist))
    operand = opseq.pop()
    if operand == '+':
        num1 = numlist.pop()
        num2 = numlist.pop()
        #print(num1)
        #print(num2)
        result = int(num1)+int(num2)
        #print(result)
        numlist.append(result)
    elif operand == '-':
        num1 = numlist.pop()
        num2 = numlist.pop()
        #print(num1)
        #print(num2)
        result = int(num1)-int(num2)
        #print(result)
        numlist.append(result)
    elif operand == '/':
        result = int(numlist.pop())/int(numlist.pop())
        #print(result)
        numlist.append(result)
    elif operand == '*':
        result = int(numlist.pop())*int(numlist.pop())
        #print(result)
        numlist.append(result)
print(result)

 