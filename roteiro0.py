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
        self.reserved = ["echo","if","else","while","end","readline","or","and","function","return"]
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
            elif self.origin[self.position] == '\n':
                self.actual = Token('NEWL','\n')
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
            elif self.origin[self.position] == ',':
                self.actual = Token('COMMA',',')
                self.position += 1
            elif self.origin[self.position] == '.':
                self.actual = Token('CONCAT','.')
                self.position += 1
            elif self.origin[self.position] == '>':
                self.actual = Token('BIGGER','>')
                self.position += 1
            elif self.origin[self.position] == '<':
                
                if self.origin[:self.position+5]=="<?php": 
                    self.actual = Token('BP',"<?php")
                    self.position += 5
                else:
                    self.actual = Token('SMALLER','<')
                    self.position += 1
            elif self.origin[self.position] == '!':
                self.actual = Token('NOT','!')
                self.position += 1
            elif self.origin[self.position] == '?':
                if self.origin[self.position:self.position+2] == "?>":
                    self.actual = Token('EP',"?>")
                    self.position += 2
            elif self.origin[self.position] == '"':
                string =''
                self.position += 1
                while self.origin[self.position] != '"':
                    string += self.origin[self.position]
                    self.position += 1
                self.actual = Token('STR',string)
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
                elif string == "function":
                    self.actual = Token('FUNC',string)
                elif string == "return":
                    self.actual = Token("RETURN",string)
                else:
                    if (string not in self.reserved):

                        self.actual = Token('NAME',string)
                    else:
                        raise Exception("palavra reservada")
            elif self.origin[self.position] == '$':
                var = "$"
                self.position += 1
                if self.origin[self.position].isalpha() and self.position < len(self.origin):
                    while (self.origin[self.position].isalpha() or self.origin[self.position]=='_' or self.origin[self.position].isdigit())and self.position < len(self.origin):
                        var += self.origin[self.position]
                        self.position += 1
                    self.actual = Token('IDEN',var)
                else:
                    raise Exception("definição de variável incorreta")
                    
                    

class PrePro():
    @staticmethod
    def filter(code):
        code = code.replace('\n','')
        p = 0
        comment_start = 0
        comment_end = 0
        while p<len(code)-1:
            if code[p] == '/' and code[p+1] == '*':
                comment_start = p
            if code[p] == '*' and code[p+1] == '/':
                comment_end = p+2
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

        if n1[1] == 'string' and (n2[1] == 'bool' or n2[1] == 'int') and self.varient != '.':
            raise Exception ("Incompatible types")
        elif (n1[1] == 'int' or n1[1] =='bool') and n2[1] == 'string' and self.varient != '.':
            raise Exception ("Incompatible types")


        if self.varient == '+':
            return ((n1[0] + n2[0]),'int')
        if self.varient == '-':
            return ((n1[0] - n2[0]),'int')
        if self.varient == '*':
            return ((n1[0] * n2[0]),'int')
        if self.varient == '/':
            return ((int(n1[0] / n2[0])),'int')
        if self.varient == '<':
            return ((n1[0] < n2[0]),'bool')
        if self.varient == '>':
            return ((n1[0] > n2[0]),'bool')
        if self.varient == '==':
            return ((n1[0] == n2[0]),'bool')
        if self.varient == 'or':
            return ((n1[0] or n2[0]),'bool')
        if self.varient == 'and':
            return ((n1[0] and n2[0]),'bool')
        if self.varient == '.':
            return ((str(n1[0]) + str(n2[0])),'string')
        
class UnOp(Node):
    def __init__(self, varient, list_nodes):
        self.varient = varient
        self.list_nodes = list_nodes
    def evaluate(self,stab):
        n1 = self.list_nodes[0].evaluate(stab)
        
        

        if self.varient == '+':
            return (n1[0],'int')
        if self.varient == '-':
            return (-n1[0],'int')   
        if self.varient == '!':
            return   (not n1[0],'bool')

class IntVal(Node):
    def __init__(self, varient):
        self.varient = varient
    def evaluate(self,stab):
        return ((self.varient),'int')

class BoolVal(Node):
    def __init__(self, varient):
        self.varient = varient
    def evaluate(self,stab):
        return ((self.varient),'bool')
class StringVal(Node):
    def __init__(self, varient):
        self.varient = varient
    def evaluate(self,stab):
        return ((self.varient),'string')

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
        print(x.evaluate(stab)[0])

class Commands(Node):
    def __init__(self,list_nodes):
        self.list_nodes = list_nodes
    def evaluate(self,stab):
        for i in self.list_nodes:
            if i != None:
                for p in i:
                    if p != None:
                        p.evaluate(stab)


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
            
        while self.list_nodes[0].evaluate(stab)[0]:
            for j in self.list_nodes[1]:
                j.evaluate(stab)


class If(Node):
    def __init__(self,list_nodes):
        self.list_nodes = list_nodes
    def evaluate(self,stab):
        cond = self.list_nodes[0].evaluate(stab)
        if type(cond) == tuple:
            cond = cond[0]
        if cond:
            for k in self.list_nodes[1]:
                return k.evaluate(stab) 
        elif len(self.list_nodes) > 2:
             for k in self.list_nodes[2]:
                return k.evaluate(stab)

class ReadLine(Node):
    def __init__(self,varient):
        self.varient = varient
    def evaluate(self):
        return (int(input()))

class FuncDec(Node):
    def __init__( self,varient,list_nodes):
        self.varient = varient
        self.list_nodes = list_nodes

    def evaluate(self, stab):
        SymbolTable.setter_func(self)

class FuncCall(Node):
    
    def __init__(self, varient, list_nodes):
        self.varient = varient
        self.list_nodes = list_nodes
        self.temp_st=SymbolTable()
    def evaluate(self,stab):
        func = SymbolTable.getter_func(self.varient)
        for i in range(len(self.list_nodes)):
            if self.list_nodes[i] in Parser.table.table:
                self.temp_st.table[func.list_nodes[i]]=Identifier(self.list_nodes[i]).evaluate(stab)
            else:
                self.temp_st.table[func.list_nodes[i]]=IntVal(self.list_nodes[i]).evaluate(stab)
        if len(func.list_nodes)>1:
            for f in range(len(func.list_nodes[-1])):
                if f < (len(func.list_nodes[-1])):
                    fn = func.list_nodes[-1][f]
                    if fn != None:
                        fn.evaluate(self.temp_st)
            if type(func.list_nodes[-1][-1]) == type(Return([])):
                if len(func.list_nodes) != len(self.list_nodes)+1:
                    raise Exception("argumentos não coincidem")
                for iy in range(len(func.list_nodes[-1])):
                    if type(func.list_nodes[-1][iy]) == type(If([])):
                        ret = func.list_nodes[-1][0].evaluate(self.temp_st)
                        return ret
                    else:
                        ret = func.list_nodes[-1][-1].evaluate(self.temp_st)
                return ret
        else:
            func.list_nodes[0].evaluate(self.temp_st)
        
        if type(func.list_nodes[-1]) == type(Return([])):
            if len(func.list_nodes) != len(self.list_nodes)+1:
                raise Exception("argumentos não coincidem")

            ret = func.list_nodes[-1].evaluate(self.temp_st)
            
            return ret

            

class Return(Node):
    def __init__(self,list_nodes):
        self.list_nodes = list_nodes
    def evaluate(self,stab):
        if self.list_nodes[0].varient in stab.table:
            return stab.table[self.list_nodes[0].varient]
        elif type(self.list_nodes[0].varient)== int:
            return (self.list_nodes[0].varient,int)
        elif type(self.list_nodes[0].varient)== bool :
            return (self.list_nodes[0].varient,bool)
        else:
            raise Exception("variável não é parametro")

class SymbolTable():
    func_tb = {}
    def __init__(self):
        self.table = {}

    def getter(self,key):
        if key in self.table:
            return  self.table[key]
        

    def setter(self,key,varient):
        self.table[key] = varient
        Parser.table = self

    @staticmethod
    def getter_func(key):
        if key in SymbolTable.func_tb:
            return  SymbolTable.func_tb[key]
        else:
            raise Exception("função não declarada")

    @staticmethod
    def setter_func(func):
        if func.varient.varient not in SymbolTable.func_tb:
            SymbolTable.func_tb[func.varient.varient] = func
        else:
            raise Exception("Tentativa de definição de uma função mais de uma vez")
        






class Parser:
    tokens = None
    table = {}
    func_table = None
    list_childs = []
    @staticmethod
    def run(code):
        code = PrePro.filter(code)
        Parser.tokens = Tokenizer(code)
        Parser.table = SymbolTable()
        Parser.func_table = SymbolTable()
        
        Parser.Program()
       
    @staticmethod
    def Program():

        if Parser.tokens.actual.type == "BP":
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "EP":
                return NoOp().evaluate()
            else:   
                while Parser.tokens.actual.type != "EP": 
                    
                    Parser.list_childs.append(Parser.command())
                   
                Commands(Parser.list_childs).evaluate(Parser.table)
        
                    
    @staticmethod
    def block():
        list_block_child=[]
        obs = 0
        if Parser.tokens.actual.type == "OB":
            Parser.tokens.selectNext()
            obs+=1
            while Parser.tokens.actual.type == "OB":
                Parser.tokens.selectNext()
                obs+=1
            else:
                if Parser.tokens.actual.type == "CB":
                    return NoOp().evaluate()
                else:
                    while Parser.tokens.actual.type != "CB":
                        child = Parser.command()
                        list_block_child.append(child) 
                    for i in range(obs):   
                        Parser.tokens.selectNext()    
                    return list_block_child                             
        else:
            raise Exception("Sintax Error")
    
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

        elif Parser.tokens.actual.type == 'FUNC':
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == 'NAME':
                func_name = Identifier(Parser.tokens.actual.value)
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == 'OPEN':
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == 'CLOSE':
                        Parser.tokens.selectNext()
                        return FuncDec(func_name,Parser.command())
                    else:
                        func = [Parser.tokens.actual.value]                     
                        Parser.tokens.selectNext()
                        while(Parser.tokens.actual.type == 'COMMA'):
                            Parser.tokens.selectNext()
                            func.append(Parser.tokens.actual.value)  
                            Parser.tokens.selectNext()
                        if Parser.tokens.actual.type != "CLOSE":  
                            raise Exception("sintax Error")                     
                        Parser.tokens.selectNext()
                        func.append(Parser.command())   
                        return FuncDec(func_name,func)
                    

                else:
                    raise Exception("sintax error")
            else: raise Exception("Function name not defined")

        elif Parser.tokens.actual.type == 'RETURN':
            Parser.tokens.selectNext()
            ret = Return([Parser.RelExpression()])
            if Parser.tokens.actual.type == 'SC':
                Parser.tokens.selectNext()
                return ret
            else:
                raise Exception("Sintax Error")

        elif Parser.tokens.actual.type == 'NAME':
            func = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == 'OPEN':
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == 'CLOSE':
                    Parser.tokens.selectNext()
                    return FuncCall(func,[])
                else:
                    args = [Parser.tokens.actual.value]
                    Parser.tokens.selectNext()
                    while(Parser.tokens.actual.type == 'COMMA'):
                        Parser.tokens.selectNext()
                        args.append(Parser.tokens.actual.value)  
                        Parser.tokens.selectNext()
                    #if Parser.tokens.actual.type != "CLOSE":  
                    #    raise Exception("sintax Error")
                    Parser.tokens.selectNext()
                    return FuncCall(func,args)

        else:
            return Parser.block()
                   
        

    @staticmethod
    def factor():
        result = ''
        if Parser.tokens.actual.type == 'INT':
            result = IntVal(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
            return result
        if Parser.tokens.actual.type == 'STR':
            result = StringVal(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
            return result
        if Parser.tokens.actual.type == 'TRUE':
            result = BoolVal(True)
            Parser.tokens.selectNext()
            return result
        if Parser.tokens.actual.type == 'FALSE':
            result = BoolVal(False)
            Parser.tokens.selectNext()
            return result
        if Parser.tokens.actual.type == 'PLUS':
            Parser.tokens.selectNext()
            result = UnOp('+',[Parser.factor()])
            return result
        if Parser.tokens.actual.type == 'MINUS':
            Parser.tokens.selectNext()
            result = UnOp('-', [Parser.factor()])
            return result
        if Parser.tokens.actual.type == 'NOT':
            Parser.tokens.selectNext()
            result = UnOp('!', [Parser.factor()])
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
                    result = IntVal(ReadLine(Parser.tokens.actual.value).evaluate())  
                else:
                    raise Exception("Sintax Error")
            else:
                raise Exception("Sintax Error")
            Parser.tokens.selectNext()
            return result
        elif Parser.tokens.actual.type == 'NAME':
            func = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == 'OPEN':
                Parser.tokens.selectNext()
                args = [Parser.tokens.actual.value]
                Parser.tokens.selectNext()
                while(Parser.tokens.actual.type == 'COMMA'):
                    Parser.tokens.selectNext()
                    args.append(Parser.tokens.actual.value)  
                    Parser.tokens.selectNext()
                if Parser.tokens.actual.type != "CLOSE":  
                    raise Exception("sintax Error")
                Parser.tokens.selectNext()
                return FuncCall(func,args)
                

            else:
                raise Exception("sintax error")

    @staticmethod
    def term():
        result = Parser.factor()    
        while Parser.tokens.actual.type in ['MULT','DIV','AND']:

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
        while Parser.tokens.actual.type in ['PLUS','MINUS','OR','CONCAT']:
            if Parser.tokens.actual.type == "PLUS":
                Parser.tokens.selectNext()
                result = BinOp("+",[result,Parser.term()])
            elif Parser.tokens.actual.type == "MINUS":
                Parser.tokens.selectNext()
                result = BinOp("-",[result,Parser.term()])

            elif Parser.tokens.actual.type == "OR":
                Parser.tokens.selectNext()
                result = BinOp("or",[result,Parser.term()])
            elif Parser.tokens.actual.type == "CONCAT":
                Parser.tokens.selectNext()
                result = BinOp(".",[result,Parser.term()])
                
        return result

    @staticmethod
    def RelExpression():
        result = Parser.parseExpression()
        if Parser.tokens.actual.type == "EQUALITY":
            Parser.tokens.selectNext()
            return BinOp("==",[result,Parser.parseExpression()])
        if Parser.tokens.actual.type == "BIGGER":
            Parser.tokens.selectNext()
            return BinOp(">",[result,Parser.parseExpression()])
        if Parser.tokens.actual.type == "SMALLER":
            Parser.tokens.selectNext()
            return BinOp("<",[result,Parser.parseExpression()])
        return result

        


if __name__ == '__main__':
    code = sys.argv[1]
    with open(code, "r") as in_file:
            code = in_file.read()
    

    Parser.run(code)
 