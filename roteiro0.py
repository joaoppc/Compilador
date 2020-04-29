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
        self.reserved = ["echo","if","else","while","end","readline","or","and"]
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
                self.position += 1
                if self.origin[self.position] == '=':
                    self.actual = Token('EQUALITY','==')
                    self.position+=1
                else:
                    self.position-=1
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
            elif self.origin[self.position] == '>':
                self.actual = Token('BIGGER','>')
                self.position += 1
            elif self.origin[self.position] == '<':
                self.actual = Token('SMALLER','<')
                self.position += 1
            elif self.origin[self.position] == '!':
                self.actual = Token('NOT','!')
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
                    string += self.origin[self.position].lower()
                    self.position += 1
                if string == "echo":
                    self.actual = Token('ECHO',string)
                elif string == "while":
                    self.actual = Token('WHILE',string)
                elif string == "if":
                    self.actual = Token('IF',string)
                elif string == "else":
                    self.actual = Token('ELSE',string)
                elif string == "true":
                    self.actual = Token('TRUE',string)
                elif string == "false":
                    self.actual = Token('FALSE',string)
                elif string == "and":
                    self.actual = Token('AND',string)
                elif string == "or":
                    self.actual = Token('OR',string)
                elif string == "readline":
                    self.actual = Token('READLINE',string)
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
        if self.varient == '<':
            return int(n1 < n2)
        if self.varient == '>':
            return int(n1 > n2)
        if self.varient == '==':
            return int(n1 == n2)
        if self.varient == 'or':
            return int(n1 or n2)
        if self.varient == 'and':
            return int(n1 and n2)
        
        
class UnOp(Node):
    def __init__(self, varient, list_nodes):
        self.varient = varient
        self.list_nodes = list_nodes
    def evaluate(self,stab):
        n1 = self.list_nodes[0].evaluate(stab)
        
        

        if self.varient == '+':
            return n1
        if self.varient == '-':
            return -n1    
        if self.varient == '!':
            return not n1

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

class While(Node):
    def __init__(self,list_nodes):
        self.list_nodes = list_nodes
    def evaluate(self,stab):
        while self.list_nodes[0].evaluate(stab):
            self.list_nodes[1].evaluate(stab)


class If(Node):
    def __init__(self,list_nodes):
        self.list_nodes = list_nodes
    def evaluate(self,stab):
        if self.list_nodes[0].evaluate(stab):
            return self.list_nodes[1].evaluate(stab)
        elif len(self.list_nodes) > 2:
            return self.list_nodes[2].evaluate(stab)

class ReadLine(Node):
    def __init__(self,varient):
        self.varient = varient
    def evaluate(self):
        return int(input())



class SymbolTable():
    def __init__(self):
        self.table = {}

    def getter(self,key):
        if key in self.table:
            return  self.table[key]
        #raise Exception("variável não declarada")

    def setter(self,key,varient):
        if key in self.table:
            self.table[key] = varient
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
                ass = Assignment('=',[Identifier(string_id),Parser.RelExpression()])
                if Parser.tokens.actual.type == 'SC':
                    Parser.tokens.selectNext()
                    return ass
                else:
                    raise Exception("Sintax Error")    
        elif Parser.tokens.actual.type == 'ECHO':
            Parser.tokens.selectNext()
            prt = Print([Parser.RelExpression()])
            if Parser.tokens.actual.type == 'SC':
                Parser.tokens.selectNext()
                return prt
            else:
                raise Exception("Sintax Error")
        elif Parser.tokens.actual.type == 'SC':
            Parser.tokens.selectNext()
        elif Parser.tokens.actual.type == 'WHILE':
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == 'OPEN':
                Parser.tokens.selectNext()
                cond = [Parser.RelExpression()]
                if Parser.tokens.actual.type != "CLOSE":
                    raise Exception("sintax Error")
                Parser.tokens.selectNext()
                cond.append(Parser.command())
                return While(cond)

            else:
                raise Exception("sintax error")
        elif Parser.tokens.actual.type == 'IF':
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == 'OPEN':
                Parser.tokens.selectNext()
                cond = [Parser.RelExpression()]
                if Parser.tokens.actual.type == 'CLOSE':
                    Parser.tokens.selectNext()
                    cond.append(Parser.command())
                    if Parser.tokens.actual.type == 'ELSE':
                        Parser.tokens.selectNext()
                        cond.append(Parser.command())
                        return If(cond)
                    else:
                        return If(cond)

             
        else:
            Parser.block()
                   
        

    @staticmethod
    def factor():
        result = ''
        if Parser.tokens.actual.type == 'INT':
            result = IntVal(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
            return result
        if Parser.tokens.actual.type == 'PLUS':
            Parser.tokens.selectNext()
            result = UnOp('+',[Parser.factor()])#.evaluate()
            return result
        if Parser.tokens.actual.type == 'MINUS':
            Parser.tokens.selectNext()
            result = UnOp('-', [Parser.factor()])#.evaluate()
            return result
        if Parser.tokens.actual.type == 'NOT':
            Parser.tokens.selectNext()
            result = UnOp('!', [Parser.factor()])#.evaluate()
            return result
        if Parser.tokens.actual.type == "OPEN":
            Parser.tokens.selectNext()
            result = Parser.RelExpression()
            if Parser.tokens.actual.type != "CLOSE":
                raise Exception("sintax Error")
            Parser.tokens.selectNext()
            return result
        if Parser.tokens.actual.type == 'IDEN':
            result = Identifier(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
            return result
        if Parser.tokens.actual.type == 'READLINE':
            Parser.tokens.selectNext()
            if  Parser.tokens.actual.type == 'OPEN':
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == 'CLOSE':
                    result = ReadLine(Parser.tokens.actual.value)
                else:
                    raise Exception("Sintax Error")
            else:
                raise Exception("Sintax Error")
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

            elif Parser.tokens.actual.type == "AND":
                Parser.tokens.selectNext()
                result = BinOp('and',[result,Parser.factor()])
                    
               
        return result
         

        

    @staticmethod
    def parseExpression():
        result = Parser.term()
        while Parser.tokens.actual.type in ['PLUS','MINUS']:
            if Parser.tokens.actual.type == "PLUS":
                Parser.tokens.selectNext()
                result = BinOp("+",[result,Parser.term()])
            
            
                    
            elif Parser.tokens.actual.type == "MINUS":
                Parser.tokens.selectNext()
                result = BinOp("-",[result,Parser.term()])

            elif Parser.tokens.actual.type == "OR":
                Parser.tokens.selectNext()
                result = BinOp("or",[result,Parser.term()])
                
        return result

    @staticmethod
    def RelExpression():
        result = Parser.parseExpression()
        if Parser.tokens.actual.value == "==":
            Parser.tokens.selectNext()
            return BinOp("=",[result,Parser.parseExpression()])
        if Parser.tokens.actual.value == ">":
            Parser.tokens.selectNext()
            return BinOp(">",[result,Parser.parseExpression()])
        if Parser.tokens.actual.value == "<":
            Parser.tokens.selectNext()
            return BinOp("<",[result,Parser.parseExpression()])
        return result

        


if __name__ == '__main__':
    code = sys.argv[1]

    Parser.run(code)
 