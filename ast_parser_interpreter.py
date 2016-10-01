#Source: https://github.com/rspivak/lsbasi/blob/master/part1/calc1.py
# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, FLOAT, PLUS, MINUS, MULTIPLY, DIVIDE, LEFT_PAREN, RIGHT_PAREN, EOF = 'INTEGER', 'FLOAT', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'LEFT_PAREN', 'RIGHT_PAREN', 'EOF'


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

class Lexer(object):
    def __init__(self,text):
        self.text = text
        self.pos = 0

    def error(self):
        raise Exception('Invalid Character')

    def ignore_whitespaces(self):
        if self.pos < len(self.text):
            while self.text[self.pos] == " ":
                self.pos += 1
                if self.pos > len(self.text) - 1:
                    break

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

        if current_char == '+':
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
            token = Token(DIVIDE, current_char)
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

        value_str = ""
        while (current_char.isdigit() or current_char == '.'):
            value_str = value_str + current_char
            self.pos += 1
            if self.pos < len(text):
                current_char = text[self.pos]
            else:
                break

        if value_str.find('.') > -1:
            try:
                value = float(value_str)
            except ValueError:
                print "Could not convert {value_str} to a float".format(value_str)
                self.error()
            token = Token(FLOAT, value)
            return token
        elif value_str[0].isdigit():
            try:
                value = int(value_str)
            except ValueError:
                print "Could not convert {value_str} to an Interger".format(value_str)
                self.error()
            token = Token(INTEGER,value)
            return token


        ####
        self.error()

class AST(object):
    pass

class BinOp(AST):
    def __init__(self,left,op,right):
        self.left = left
        self.op = op
        self.right = right

class Num(AST):
    def __init__(self,value):
        self.value = value

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
        if self.current_token.type in token_type:
            if token_type is not EOF:
                self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        self.current_token = self.lexer.get_next_token()
        if self.current_token.type == LEFT_PAREN:
            node = self.expr()
            self.eat(RIGHT_PAREN)
        else:
            node = Num(self.current_token.value)
            self.eat([INTEGER,FLOAT])
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in [MULTIPLY,DIVIDE]:
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

    def build_ast(self):
        return self.expr()

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

    def visit_BinOp(self,node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if node.op == PLUS:
            return left + right
        elif node.op == MINUS:
            return left - right
        elif node.op == MULTIPLY:
            return left * right
        elif node.op == DIVIDE:
            return left / right

    def visit_Num(self,node):
        return node.value

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
        result = interpreter.evaluate()
        print(result)


if __name__ == '__main__':
    main()
