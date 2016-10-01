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
        """
        # get a character at the position self.pos and decide
        # what token to create based on the single character
        current_char = text[self.pos]

        # if the character is a digit then convert it to
        # integer, create an INTEGER token, increment self.pos
        # index to point to the next character after the digit,
        # and return the INTEGER token
        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        if current_char == '-':
            token = Token(MINUS, current_char)
            self.pos += 1
            return token

        if current_char == '*':
            token = Token(MULTIPLY, current_char)
            self.pos += 1
            return token

        if current_char == '/':
            token = Token(DIVIDE, current_char)
            self.pos += 1
            return token
        """
        self.error()

class Interpreter(object):
    def __init__(self, text):
        ## client string input, e.g. "3+5"
        #self.text = text
        ## self.pos is an index into self.text
        #self.pos = 0
        self.lexer = Lexer(text)
        # current token instance
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
    """
    def expr(self):
        operators = []
        operands = []
        operands.append(self.factor())
        while self.current_token.type in [MULTIPLY,DIVIDE,PLUS,MINUS]:
            #if self.current_token.type == MULTIPLY:
            #    result = result*self.factor()
            #elif self.current_token.type == DIVIDE:
            #    result = result/self.factor()
            operators.append(self.current_token.type)
            operands.append(self.factor())
        self.eat(EOF)

        result = self.interp(operators,operands)
        return result

    def interp(self,ops,operands):
        while len(ops) > 0:
            if DIVIDE in ops:
                idx = ops.index(DIVIDE)
                ops.pop(idx)
                operands.insert(idx,operands[idx]/operands[idx+1])
                operands.pop(idx+1)
                operands.pop(idx+1)
                continue
            if MULTIPLY in ops:
                idx = ops.index(MULTIPLY)
                ops.pop(idx)
                operands.insert(idx,operands[idx]*operands[idx+1])
                operands.pop(idx+1)
                operands.pop(idx+1)
                continue
            if MINUS in ops:
                idx = ops.index(MINUS)
                ops.pop(idx)
                operands.insert(idx,operands[idx]-operands[idx+1])
                operands.pop(idx+1)
                operands.pop(idx+1)
                continue
            if PLUS in ops:
                idx = ops.index(PLUS)
                ops.pop(idx)
                operands.insert(idx,operands[idx]+operands[idx+1])
                operands.pop(idx+1)
                operands.pop(idx+1)
                continue

        return operands[0]
    """

    def factor(self):
        self.current_token = self.lexer.get_next_token()
        if self.current_token.type == LEFT_PAREN:
            result = self.expr()
            self.eat(RIGHT_PAREN)
        else:
            result = self.current_token.value
            self.eat([INTEGER,FLOAT])
        return result

    def term(self):
        result = self.factor()
        while self.current_token.type in [MULTIPLY,DIVIDE]:
            if self.current_token.type == DIVIDE:
                result = result/self.factor()
            else:
                result = result*self.factor()
        return result

    def expr(self):
        """
        CFG(Context-Free-Grammer) followed by this parser:
            expr : term ((PLUS|MINUS) term)*
            term : factor ((MULTIPLY|DIVIDE) factor)*
            factor : NUMBER{FLOAT|INTEGER}|expr
        """
        result = self.term()
        while self.current_token.type in [PLUS,MINUS]:
            if self.current_token.type == MINUS:
                result -= self.term()
            else:
                result += self.term()
        #self.eat(EOF)
        return result

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
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
