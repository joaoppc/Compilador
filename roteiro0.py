import sys
class Token:
    def __init__(self,type,value):
        self.type = type
        self.value = value
class Tokenizer:
    def __init__(self,origin):
        self.origin = origin
        self.position = 0
        self.actual = 0
        self.selectNext()
    def selectNext(self):
        while (self.position < len(self.origin)) and (self.origin[self.position] == " "):
            self.position += 1
        if self.position <len(self.origin):
            self.actual = self.origin[self.position]
            if self.origin[self.position] == '+':
                self.actual = Token('PLUS','+')
                self.position += 1
            elif self.origin[self.position] == '-':
                self.actual = Token('MINUS','-')
                self.position += 1
            elif self.origin[self.position] == '*':
                self.actual = Token('MULT','*')
                self.position += 1
            elif self.origin[self.position] == '/':
                self.actual = Token('DIV','/')
                self.position += 1
            elif self.origin[self.position].isdigit():
                num = ""
                while (self.position < len(self.origin)) and (self.origin[self.position].isdigit()):
                    num += self.origin[self.position]
                    self.position += 1
                self.actual = Token('INT',int(num))

class PrePro():
    @staticmethod
    def filter(code):
        p = 0
        comment_start = 0
        comment_end = 0
        while p<len(code)-1:
            if code[p] == '/' and code[p+1] == '*':
                comment_start = p
                p
            if code[p] == '*' and code[p+1] == '/':
                comment_end == p+1
            p+=1
        code = code[:comment_start]+code[comment_end:]
        return code
        
class Parser:
    tokens = None
    @staticmethod
    def run(code):
        code = PrePro.filter(code)
        Parser.tokens = Tokenizer(code)
        print(Parser.parseExpression())

    @staticmethod
    def term():
        result = ""
        if Parser.tokens.actual.type == 'INT':
            result = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            while Parser.tokens.actual.type in ['MULT','DIV']:

                if Parser.tokens.actual.type == "MULT":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == 'INT':
                        result *= Parser.tokens.actual.value
                        Parser.tokens.selectNext()
                    else:
                        print('erro')
                    
                elif Parser.tokens.actual.type == "DIV":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == 'INT':
                        result /= Parser.tokens.actual.value
                        Parser.tokens.selectNext()
                    else:
                        print('erro')
            return result
        else:
            print('erro') 

        

    @staticmethod
    def parseExpression():
        result = Parser.term()
        while Parser.tokens.actual.type in ['PLUS','MINUS']:
            if Parser.tokens.actual.type == "PLUS":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == 'INT':
                        result += Parser.term()
                        Parser.tokens.selectNext()
                else:
                    print('erro')
                    
            elif Parser.tokens.actual.type == "MINUS":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == 'INT':
                        result -= Parser.term()
                        Parser.tokens.selectNext()
                else:
                    print('erro')
        return result
        


if __name__ == '__main__':
    code = sys.argv[1]

    Parser.run(code)
 