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
            elif self.origin[self.position].isdigit():
                num = ""
                
                num += self.origin[self.position]
                self.actual = Token('INT',int(num))
                self.position += 1
            
class Parser:
    tokens = None
    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        print(Parser.parseExpression())
        

    @staticmethod
    def parseExpression():
        result = ""
        if Parser.tokens.actual.type == 'INT':
            result = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            while Parser.tokens.actual.type in ['PLUS','MINUS']:

                if Parser.tokens.actual.type == "PLUS":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == 'INT':
                        result += Parser.tokens.actual.value
                        Parser.tokens.selectNext()
                    else:
                        print('erro')
                    
                elif Parser.tokens.actual.type == "MINUS":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == 'INT':
                        result -= Parser.tokens.actual.value
                        Parser.tokens.selectNext()
                    else:
                        print('erro') 
            return result
        else:
            print('erro') 

        


if __name__ == '__main__':
    code = sys.argv[1]
    Parser.run(code)
 