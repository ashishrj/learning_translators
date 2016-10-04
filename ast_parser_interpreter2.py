#Source: https://github.com/rspivak/lsbasi/blob/master/part1/calc1.py
# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER_CONST, REAL_CONST, PLUS, MINUS, MULTIPLY, LEFT_PAREN, RIGHT_PAREN, EOF = 'INTEGER_CONST', 'REAL_CONST', 'PLUS', 'MINUS', 'MULTIPLY', 'LEFT_PAREN', 'RIGHT_PAREN', 'EOF'
BEGIN, END, SEMI, ASSIGN, VAR, DOT, INTEGER_DIV, FLOAT_DIV = 'BEGIN', 'END', ';', ':=', 'VAR', '.', 'DIV', '/'
PROGRAM, INTEGER, REAL, COLON, COMMA = 'PROGRAM', 'INTEGER', 'REAL', ':', ','
ID = 'ID'

class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF
        self.type = type
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '+', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.
        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

RESERVED_KEYWORDS = {BEGIN:Token(BEGIN,BEGIN),
                     END:Token(END,END),
                     PROGRAM:Token(PROGRAM,PROGRAM),
                     VAR:Token(VAR,VAR),
                     INTEGER_DIV:Token(INTEGER_DIV,INTEGER_DIV),
                     INTEGER:Token(INTEGER,INTEGER),
                     REAL:Token(REAL,REAL)}

class Lexer(object):
    def __init__(self,text):
        self.text = text
        self.pos = 0

    def error(self):
        raise Exception('Invalid Character')

    def ignore_whitespaces(self):
        if self.pos < len(self.text):
            while self.text[self.pos] == " " or self.text[self.pos] == "\n":
                self.pos += 1
                if self.pos > len(self.text) - 1:
                    break
    def peek(self):
        text = self.text
        if self.pos >= len(text) - 1 or text[self.pos+1] == " " or text[self.pos+1] == "\n":
            return None
        else:
            return text[self.pos+1]

    def num(self):
        value_str = ""
        text = self.text
        current_char = text[self.pos]
        while (current_char.isdigit() or current_char == '.'):
            value_str = value_str + current_char
            self.pos += 1
            if self.pos < len(text):
                current_char = text[self.pos]
            else:
                break
        return value_str

    def _id(self):
        str_in = ""
        text = self.text
        current_char = text[self.pos]
        while (current_char.isalnum() or current_char == '_'):
            str_in = str_in + current_char.upper()
            self.pos += 1
            if self.pos < len(text):
                current_char = text[self.pos]
            else:
                break
        return str_in

    def skip_comment(self):
        text = self.text
        current_char = text[self.pos]
        while current_char != '}':
            if self.pos < len(text):
                self.pos += 1
                current_char = text[self.pos]
        self.pos += 1

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        text = self.text

        # is self.pos index past the end of the self.text ?
        # if so, then return EOF token because there is no more
        # input left to convert into tokens
        self.ignore_whitespaces()
        if self.pos > len(text) - 1:
            return Token(EOF, None)
        #### Logic for ignoring whitespaces and handling multiple
        #### digit input 
        current_char = text[self.pos]
        if current_char == '{':
            self.skip_comment()
            return self.get_next_token()
        elif current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token
        elif current_char == '-':
            token = Token(MINUS, current_char)
            self.pos += 1
            return token
        elif current_char == '*':
            token = Token(MULTIPLY, current_char)
            self.pos += 1
            return token
        elif current_char == '/':
            token = Token(FLOAT_DIV,'/')
            self.pos += 1
            return token
        elif current_char == '(':
            token = Token(LEFT_PAREN, current_char)
            self.pos += 1
            return token
        elif current_char == ')':
            token = Token(RIGHT_PAREN, current_char)
            self.pos += 1
            return token
        elif current_char == ';':
            token = Token(SEMI,';')
            self.pos += 1
            return token
        elif current_char == ':':
            if self.peek() == '=':
                token = Token(ASSIGN,':=')
                self.pos += 2
                return token
            else:
                token = Token(COLON,':')
                self.pos += 1
                return token
        elif current_char == ',':
            token = Token(COMMA,',')
            self.pos += 1
            return token
        elif current_char == '.':
            next_char = self.peek()
            if next_char == None or next_char == ' ':
                token = Token(DOT,'.')
                self.pos += 1
                return token
            elif next_char.isdigit():
                try:
                    value_str = self.num()
                    token = Token(REAL_CONST,float(value_str))
                except ValueError:
                    print "Could not convert {value_str} to a float".format(value_str)
                    self.error()
                return token
        elif current_char.isdigit():
            value_str = self.num()
            if value_str.find('.') > -1:
                try:
                    value = float(value_str)
                except ValueError:
                    print "Could not convert {value_str} to a float".format(value_str)
                    self.error()
                token = Token(REAL_CONST, value)
                return token
            elif value_str[0].isdigit():
                try:
                    value = int(value_str)
                except ValueError:
                    print "Could not convert {value_str} to an Interger".format(value_str)
                    self.error()
                token = Token(INTEGER_CONST,value)
                return token
        elif current_char.isalpha() or current_char == '_':
            value = self._id()
            if value in RESERVED_KEYWORDS.keys():
                return RESERVED_KEYWORDS[value]
            else:
                return Token(ID,value)
        ####
        self.error()

class AST(object):
    pass

class BinOp(AST):
    def __init__(self,left,op,right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class Num(AST):
    def __init__(self,value):
        self.value = value

class Assign(AST):
    def __init__(self,var,expr):
        self.var = var
        self.expr = expr

class Var(AST):
    def __init__(self,token):
        self.token = token
        self.name = token.value
        self.type = None

class CompoundStatement(AST):
    def __init__(self):
        self.statement_list = []

class Declarations(AST):
    def __init__(self):
        self.variable_list = []

class Block(AST):
    def __init__(self,declaration,compound):
        self.declaration = declaration
        self.compound = compound

class Empty(AST):
    pass

class Parser(object):
    def __init__(self, text):
        self.lexer = Lexer(text)
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        #print self.current_token, token_type
        if self.current_token.type in token_type:
            if token_type is not EOF:
                self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        self.current_token = self.lexer.get_next_token()
        if self.current_token.type in [PLUS,MINUS]:
            node = UnaryOp(self.current_token.type,self.factor())
        elif self.current_token.type == LEFT_PAREN:
            node = self.expr()
            self.eat(RIGHT_PAREN)
        elif self.current_token.type == ID:
            node = Var(self.current_token)
            self.eat(ID)
        else:
            node = Num(self.current_token.value)
            self.eat([INTEGER_CONST,REAL_CONST])
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in [MULTIPLY,INTEGER_DIV,FLOAT_DIV]:
            #if self.current_token.type == DIVIDE:
            #    result = result/self.factor()
            #else:
            #    result = result*self.factor()
            node = BinOp(node,self.current_token.type,self.factor())
        return node

    def expr(self):
        """
        CFG(Context-Free-Grammer) followed by this parser:
            expr : term ((PLUS|MINUS) term)*
            term : factor ((MULTIPLY|DIVIDE) factor)*
            factor : NUMBER{FLOAT|INTEGER}|expr
        """
        node = self.term()
        while self.current_token.type in [PLUS,MINUS]:
            #if self.current_token.type == MINUS:
            #    result -= self.term()
            #else:
            #    result += self.term()
            node = BinOp(node,self.current_token.type,self.term())
        #self.eat(EOF)
        return node

    def variable(self):
        token = self.current_token
        self.eat(ID)
        return Var(token)

    def assign(self):
        var = self.variable()
        expr = self.expr()
        return Assign(var,expr)

    def statement(self):
        if self.current_token.type == END:
            return Empty()
        elif self.current_token.type == BEGIN:
            return self.compound_statement()
        else:
            return self.assign()

    def statement_list(self):
        statements = []
        statements.append(self.statement())
        if self.current_token.type == SEMI:
            self.eat(SEMI)
            statements.extend(self.statement_list())
        return statements

    def compound_statement(self):
        self.eat(BEGIN)
        node = CompoundStatement()
        node.statement_list = self.statement_list()
        self.eat(END)
        return node

    def variable_declaration(self):
        variable_list = []
        variable_list.append(self.variable())
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            variable_list.append(self.variable())
        self.eat(COLON)
        type_spec = self.current_token.value
        self.eat([INTEGER,REAL])
        for i in range(len(variable_list)):
            variable_list[i].type = type_spec
        return variable_list

    def declaration(self):
        node = Declarations()
        if self.current_token.type == VAR:
            self.eat(VAR)
            while self.current_token.type == ID:
                node.variable_list.extend(self.variable_declaration())
                self.eat(SEMI)
        return node

    def block(self):
        declaration = self.declaration()
        return Block(declaration,self.compound_statement())

    def program(self):
        self.current_token = self.lexer.get_next_token()
        self.eat(PROGRAM)
        self.variable()
        self.eat(SEMI)
        node = self.block()
        self.eat(DOT)
        return node

    def build_ast(self):
        return self.program()

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
    def __init__(self, node):
        self.node = node
        self.GLOBAL_SCOPE = {}
        self.GLOBAL_TYPE_SPEC = {}

    def visit_BinOp(self,node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if node.op == PLUS:
            return left + right
        elif node.op == MINUS:
            return left - right
        elif node.op == MULTIPLY:
            return left * right
        elif node.op == INTEGER_DIV:
            assert type(left)==int,"Type Mismatch, Expected Integer"
            assert type(right) == int, "Type Mismatch, Expected Integer"
            return left / right
        elif node.op == FLOAT_DIV:
            return left*1.0/ right

    def visit_UnaryOp(self,node):
        expr = self.visit(node.expr)
        if node.op == PLUS:
            return expr
        else:
            return -(expr)

    def visit_Declarations(self,node):
        for variable in node.variable_list:
            self.GLOBAL_TYPE_SPEC[variable.name] = variable.type

    def visit_Block(self,node):
        self.visit(node.declaration)
        self.visit(node.compound)

    def visit_Num(self,node):
        return node.value

    def visit_CompoundStatement(self,node):
        for i in range(len(node.statement_list)):
            self.visit(node.statement_list[i])

    def visit_Assign(self,node):
        value = self.visit(node.expr)
        if type(value) == int:
            expr_type = INTEGER
        else:
            expr_type = REAL
        assert self.GLOBAL_TYPE_SPEC[node.var.name] == expr_type, "Type Mismatch for variable {name}".format(name = node.var.name)
        #type_spec = self.GLOBAL_TYPE_SPEC[node.var.name]
        #if type_spec == INTEGER:
        #    assert type(value)==int,"Type Mismatch"
        #else:
        #    assert type(value)==float,"Type Mismatch"
        self.GLOBAL_SCOPE[node.var.name] = value

    def visit_Var(self,node):
        val = self.GLOBAL_SCOPE.get(node.name)
        if val is None:
            raise NameError(repr(node.name))
        else:
            return val

    def visit_Empty(self,node):
        pass

    def evaluate(self):
        return self.visit(self.node)

def main():
    while True:
        try:
            try:
                text = raw_input('calc> ')
            except NameError:  # Python3
                text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        parser = Parser(text)
        interpreter = Interpreter(parser.build_ast())
        interpreter.evaluate()
        print interpreter.GLOBAL_SCOPE
        print interpreter.GLOBAL_TYPE_SPEC


if __name__ == '__main__':
    main()
