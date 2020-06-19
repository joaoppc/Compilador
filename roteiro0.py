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
            elif self.origin[self.position] == '\n':
                self.actual = Token('NEWL','\n')
                self.position += 1
            elif self.origin[self.position] == '\t':
                self.actual = Token('TAB','\t')
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
            elif self.origin[self.position] == '$':
                var = "$"
                self.position += 1
                while self.origin[self.position].isalpha() and self.position < len(self.origin):
                    var += self.origin[self.position]
                    self.position += 1
                    self.actual = Token('IDEN',var)


class Assembly():
    assembly = ""
    id_node=0
    @staticmethod
    def write_assembly(ass_code):
        Assembly.assembly += ass_code
    

    @staticmethod
    def flush_code(nasm):

        fr =  open(nasm, "r")
        nasm_template = fr.read()
        fr.close()
        template_split=nasm_template.split("\n")
        above = template_split[:-5]
        above = "\n".join(above)
        bellow = template_split[-5:]
        bellow = "\n".join(bellow)

        
        with open("assembly.asm","w+") as write_file:
                
            write_file.write(above)
            write_file.write(Assembly.assembly)
            write_file.write(bellow)



                    

class PrePro():
    @staticmethod
    def filter(code):
        code = code.replace('\n','')
        code = code.replace('\t','')
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
        Assembly.id_node+=1
        n1 = self.list_nodes[0].evaluate(stab)
        Assembly.write_assembly("  PUSH EBX ; O BinOp guarda o valor na pilha \n")
        n2 = self.list_nodes[1].evaluate(stab)

        if n1[1] == 'string' and (n2[1] == 'bool' or n2[1] == 'int') and self.varient != '.':
            raise Exception ("Incompatible types")
        elif (n1[1] == 'int' or n1[1] =='bool') and n2[1] == 'string' and self.varient != '.':
            raise Exception ("Incompatible types")


        if self.varient == '+':
            Assembly.write_assembly("  POP EAX ; recupera o valor da pilha EAX \n")
            Assembly.write_assembly("  ADD EAX, EBX ; executa a operação \n")
            Assembly.write_assembly("  MOV EBX, EAX ; retorna o valor em EBX \n\n")
            return ((n1[0] + n2[0]),'int')
        if self.varient == '-':
            Assembly.write_assembly("  POP EAX ; recupera o valor da pilha EAX \n")
            Assembly.write_assembly("  SUB EAX, EBX ; executa a operação \n")
            Assembly.write_assembly("  MOV EBX, EAX ; retorna o valor em EBX \n\n")
            return ((n1[0] - n2[0]),'int')
        if self.varient == '*':
            Assembly.write_assembly("  POP EAX ; recupera o valor da pilha EAX \n")
            Assembly.write_assembly("  IMUL EAX, EBX ; executa a operação \n")
            Assembly.write_assembly("  MOV EBX, EAX ; retorna o valor em EBX \n\n")
            return ((n1[0] * n2[0]),'int')
        if self.varient == '/':
            Assembly.write_assembly("  POP EAX ; recupera o valor da pilha EAX \n")
            Assembly.write_assembly("  DIV EAX, EBX ; executa a operação \n")
            Assembly.write_assembly("  MOV EBX, EAX ; retorna o valor em EBX \n\n")
            return ((int(n1[0] / n2[0])),'int')
        if self.varient == '<':
            Assembly.write_assembly("  POP EAX ; recupera o valor da pilha EAX \n")
            Assembly.write_assembly("  CMP EAX, EBX; comparaos valores \n")
            Assembly.write_assembly("  CALL binop_jl ; executa a operação \n")
            #Assembly.write_assembly("MOV EBX, EAX ; retorna o valor em EBX \n\n")
            return ((n1[0] < n2[0]),'bool')
        if self.varient == '>':
            Assembly.write_assembly("  POP EAX ; recupera o valor da pilha EAX \n")
            Assembly.write_assembly("  CMP EAX, EBX; comparaos valores \n")
            Assembly.write_assembly("  CALL binop_jg ; executa a operação \n")
            #Assembly.write_assembly("MOV EBX, EAX ; retorna o valor em EBX \n\n")
            return ((n1[0] > n2[0]),'bool')
        if self.varient == '==':
            Assembly.write_assembly("  POP EAX ; recupera o valor da pilha EAX \n")
            Assembly.write_assembly("  CMP EAX, EBX; comparaos valores \n")
            Assembly.write_assembly("  CALL binop_je ; executa a operação \n")
            #Assembly.write_assembly("MOV EBX, EAX ; retorna o valor em EBX \n\n")
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
        Assembly.id_node+=1
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
        Assembly.id_node+=1
        Assembly.write_assembly("  MOV EBX, "+str(self.varient)+" ; Evaluate do IntVal \n")
        return ((self.varient),'int')

class BoolVal(Node):
    def __init__(self, varient):
        self.varient = varient
    def evaluate(self,stab):
        Assembly.id_node+=1
        return ((self.varient),'bool')
class StringVal(Node):
    def __init__(self, varient):
        self.varient = varient
    def evaluate(self,stab):
        Assembly.id_node+=1
        return ((self.varient),'string')

class NoOp(Node):
    def __init__(self):
        self.varient = None
        self.list_nodes = []
    def evaluate(self):
        Assembly.id_node+=1
        return None

class Identifier(Node):
    def __init__(self, varient):
        self.varient = varient
    def evaluate(self,stab):
        Assembly.id_node+=1
        Assembly.write_assembly("  MOV EBX, [EBP-"+str(stab.table[self.varient][1])+"] ; evaluate do identifier à esquerda do binop \n\n")
        return SymbolTable.getter(stab,self.varient)

class Print(Node):
    def __init__(self, list_nodes):
        self.list_nodes = list_nodes
    def evaluate(self,stab):
        x = self.list_nodes[0]
        if type(x) is tuple:
            x = x[0]
        print(x.evaluate(stab)[0])
        Assembly.id_node+=1
        Assembly.write_assembly("  PUSH EBX ; empilha os argumentos \n")
        Assembly.write_assembly("  CALL print ; chamada da função \n")
        Assembly.write_assembly("  POP EBX ; desempilha argumento \n\n")

class Commands(Node):
    def __init__(self,list_nodes):
        self.list_nodes = list_nodes
    def evaluate(self,stab):
        Assembly.id_node+=1
        for i in self.list_nodes:
            if i != None:
                for p in i:
                    if p!= None:
                        p.evaluate(stab)
                


class Assignment(Node):
    def __init__(self,varient, list_nodes):
        self.list_nodes = list_nodes
        self.varient = varient
    def evaluate(self,stab):
        Assembly.id_node+=1
        if self.list_nodes[0].varient not in stab.table:
            Assembly.write_assembly("  PUSH DWORD 0 ; alocação na primeira atribuição\n")
        SymbolTable.setter(stab ,self.list_nodes[0].varient,self.list_nodes[1].evaluate(stab))
        

class While(Node):
    def __init__(self,list_nodes):
        self.list_nodes = list_nodes
    def evaluate(self,stab):
        Assembly.id_node+=1
        id_node=Assembly.id_node
        Assembly.write_assembly("LOOP_"+str(id_node)+": ; unique identifier do while\n")
        node_left = self.list_nodes[0].evaluate(stab)
        Assembly.write_assembly("  CMP EBX, False ; verifica se o teste deu falso\n")
        Assembly.write_assembly("  JE EXIT_"+str(id_node)+" ; se falso sai do while\n")
        for j in self.list_nodes[1]:
            j.evaluate(stab)
        #while self.list_nodes[0].evaluate(stab):
        #    for j in self.list_nodes[1]:
        #        j.evaluate(stab)
        Assembly.write_assembly("  JMP LOOP_"+str(id_node)+" ; testa novamente\n")
        Assembly.write_assembly("EXIT_"+str(id_node)+": ; saida\n\n")
    



class If(Node):
    def __init__(self,list_nodes):
        self.list_nodes = list_nodes
    def evaluate(self,stab):
        Assembly.id_node+=1
        id_node=Assembly.id_node
        Assembly.write_assembly("LOOP_"+str(id_node)+": ; unique identifier do if\n")
        node_left = self.list_nodes[0].evaluate(stab)
        Assembly.write_assembly("  CMP EBX, False ; verifica se o teste deu falso\n")
        Assembly.write_assembly("  JE ELSE_"+str(id_node)+" ; se falso vai para else\n")
        for k in self.list_nodes[1]:
                k.evaluate(stab) 
        #if self.list_nodes[0].evaluate(stab):
        #    for k in self.list_nodes[1]:
        #        k.evaluate(stab) 
        #elif len(self.list_nodes) > 2:
        #     for k in self.list_nodes[2]:
        #        k.evaluate(stab)
        Assembly.write_assembly("ELSE_"+str(id_node)+": ; unique identifier do if\n")
        if len(self.list_nodes) > 2:
            for k in self.list_nodes[2]:
                k.evaluate(stab)
        Assembly.write_assembly("EXIT_"+str(id_node)+": ; saida\n\n")

class ReadLine(Node):
    def __init__(self,varient):
        self.varient = varient
    def evaluate(self):
        Assembly.id_node+=1
        return ((int(input())),'int')



class SymbolTable():
    def __init__(self):
        self.table = {}

    def getter(self,key):
        if key in self.table:
            
            return  self.table[key][0]
        
        

    def setter(self,key,varient):
        if key in self.table:
            deslocamento = self.table[key][1]
        else:
            deslocamento = (len(self.table.keys())+1)*4
        Assembly.write_assembly("  MOV [EBP-"+str(deslocamento)+"], EBX ; resultado da atribuição \n\n")
        
        self.table[key] = (varient,deslocamento)
        Parser.table = self.table
    
        


class Parser:
    tokens = None
    table = None
    list_childs = []
    @staticmethod
    def run(code):
        code = PrePro.filter(code)
        Parser.tokens = Tokenizer(code)
        Parser.table = SymbolTable()
        
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
        if Parser.tokens.actual.type == "OB":
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "CB":
                return NoOp().evaluate()
            else:
                while Parser.tokens.actual.type != "CB":
                    child = Parser.command()
                    list_block_child.append(child) 
                     
                Parser.tokens.selectNext()    
                return list_block_child                             

    
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
    nasm = "modelo.asm"
    with open(code, "r") as in_file:
            code = in_file.read()


    

    Parser.run(code)
    Assembly.flush_code(nasm)
 