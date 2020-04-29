import sys
class Token:
    def __init__(self,type,value):
        self.type = type
        self.value = value
class Tokenizer:
    def __init__(self,origin):
        self.origin = origin
        self.position = 0
        self.actual = None
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
            elif self.origin[self.position] == '(':
                self.actual = Token('OPEN','(')
                self.position += 1
            elif self.origin[self.position] == ')':
                self.actual = Token('CLOSE',')')
                self.position += 1
            elif self.origin[self.position] == '=':
                self.actual = Token('EQUAL','=')
                self.position += 1
            elif self.origin[self.position] == '{':
                self.actual = Token('OB','{')
                self.position += 1
            elif self.origin[self.position] == '}':
                self.actual = Token('CB','}')
                self.position += 1
            elif self.origin[self.position] == ';':
                self.actual = Token('SC',';')
                self.position += 1
            elif self.origin[self.position].isdigit():
                num = ""
                while (self.position < len(self.origin)) and (self.origin[self.position].isdigit()):
                    num += self.origin[self.position]
                    self.position += 1
                self.actual = Token('INT',int(num))
            elif self.origin[self.position].isalpha():
                string = ""
                while self.origin[self.position].isalpha() and (self.position < len(self.origin)):
                    string += self.origin[self.position]
                    self.position += 1
                if string.lower() == "echo":
                    self.actual = Token('ECHO',string)
            elif self.origin[self.position] == '$':
                var = "$"
                self.position += 1
                while self.origin[self.position].isalpha() and self.position < len(self.origin):
                    var += self.origin[self.position]
                    self.position += 1
                    self.actual = Token('IDEN',var)
                    
                    

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

class Node():
    def __init__(self, varient, list_nodes):
        self.varient = varient
        self.list_nodes = list_nodes
    def evaluate(self,stab):
        return self.varient

class BinOp(Node):
    def __init__(self, varient, list_nodes):
        self.varient = varient
        self.list_nodes = list_nodes
    def evaluate(self,stab):
        n1 = self.list_nodes[0].evaluate(stab)
        n2 = self.list_nodes[1].evaluate(stab)

        if self.varient == '+':
            return n1 + n2
        if self.varient == '-':
            return n1 - n2
        if self.varient == '*':
            return n1 * n2
        if self.varient == '/':
            return int(n1 / n2)
        
        
class UnOp(Node):
    def __init__(self, varient, list_nodes):
        self.varient = varient
        self.list_nodes = list_nodes
    def evaluate(self):
        n1 = self.list_nodes[0]

        if self.varient == '+':
            return n1
        if self.varient == '-':
            return -n1    

class IntVal(Node):
    def __init__(self, varient):
        self.varient = varient
    def evaluate(self,stab):
        return self.varient

class NoOp(Node):
    def __init__(self):
        self.varient = None
        self.list_nodes = []
    def evaluate(self):
        return None

class Identifier(Node):
    def __init__(self, varient):
        self.varient = varient
    def evaluate(self,stab):
        return SymbolTable.getter(stab,self.varient)

class Print(Node):
    def __init__(self, list_nodes):
        self.list_nodes = list_nodes
    def evaluate(self,stab):
        x = self.list_nodes[0]
        if type(x) is tuple:
            x = x[0]
        print(x.evaluate(stab))

class Commands(Node):
    def __init__(self,list_nodes):
        self.list_nodes = list_nodes
    def evaluate(self,stab):
        for i in self.list_nodes:
            if i != None:
                i.evaluate(stab)


class Assignment(Node):
    def __init__(self,varient, list_nodes):
        self.list_nodes = list_nodes
        self.varient = varient
    def evaluate(self,stab):
        SymbolTable.setter(stab ,self.list_nodes[0].varient,self.list_nodes[1].evaluate(stab))
        



class SymbolTable():
    def __init__(self):
        self.table = {}

    def getter(self,key):
        if key in self.table:
            return  self.table[key]
        print("variável não declarada")

    def setter(self,key,varient):
        if key in self.table:
            self.table[key][0] = varient
        self.table[key] = varient
        Parser.table = self.table
    
        


class Parser:
    tokens = None
    table = None
    @staticmethod
    def run(code):
        code = PrePro.filter(code)
        Parser.tokens = Tokenizer(code)
        Parser.table = SymbolTable()
        Parser.block()
       

    @staticmethod
    def block():
        list_childs=[]
        if Parser.tokens.actual.type == "OB":
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "CB":
                return NoOp().evaluate()
            else:
                while Parser.tokens.actual.type != "CB":
                    child = Parser.command()
                    if child != None:

                        list_childs.append(child)

                    
        
        Commands(list_childs).evaluate(Parser.table)

        
    
    @staticmethod
    def command():
        
        if Parser.tokens.actual.type == 'IDEN':
            string_id = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == 'EQUAL':
                Parser.tokens.selectNext()
                return Assignment('=',[Identifier(string_id),Parser.parseExpression()])
        elif Parser.tokens.actual.type == 'ECHO':
            Parser.tokens.selectNext()
            return Print([Parser.parseExpression()])
        elif Parser.tokens.actual.type == 'SC':
            Parser.tokens.selectNext()
             
        else:
            Parser.block()
                   
        

    @staticmethod
    def factor():
        result = ''
        if Parser.tokens.actual.type == 'INT':
            result = IntVal(Parser.tokens.actual.value)#.evaluate()
            Parser.tokens.selectNext()
            return result
        if Parser.tokens.actual.type == 'PLUS':
            Parser.tokens.selectNext()
            result = UnOp('+',[Parser.factor()]).evaluate()
            return result
        if Parser.tokens.actual.type == 'MINUS':
            Parser.tokens.selectNext()
            result = UnOp('-', [Parser.factor()]).evaluate()
            return result
        if Parser.tokens.actual.type == 'OPEN':
            Parser.tokens.selectNext()
            result = Parser.parseExpression()
            return result
        if Parser.tokens.actual.type == 'IDEN':
            result = Identifier(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
            return result
         

    @staticmethod
    def term():
        result = Parser.factor()    
        while Parser.tokens.actual.type in ['MULT','DIV']:

            if Parser.tokens.actual.type == "MULT":
                Parser.tokens.selectNext()
                
                result = BinOp('*',[result,Parser.factor()])
                    
            elif Parser.tokens.actual.type == "DIV":
                Parser.tokens.selectNext()
                
                result = BinOp('/',[result,Parser.factor()])
                    
               
        return result
         

        

    @staticmethod
    def parseExpression():
        result = Parser.term()
        while Parser.tokens.actual.type in ['PLUS','MINUS']:
            if Parser.tokens.actual.type == "PLUS":
                Parser.tokens.selectNext()
                result = BinOp("+",[result,Parser.term()])
            #    continue
            
                    
            elif Parser.tokens.actual.type == "MINUS":
                Parser.tokens.selectNext()
                result = BinOp("-",[result,Parser.term()])
                
        return result
        


if __name__ == '__main__':
    code = sys.argv[1]

    Parser.run(code)
 