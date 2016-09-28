#Source: https://github.com/rspivak/lsbasi/blob/master/part1/calc1.py
# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, MULTIPLY, DIVIDE, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'EOF'


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, MINUS, MULTIPLY, DIVIDE, or EOF
        self.type = type
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '+', '-', '*', '/', or None
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


class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        text = self.text

        # is self.pos index past the end of the self.text ?
        # if so, then return EOF token because there is no more
        # input left to convert into tokens
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        # get a character at the position self.pos and decide
        # what token to create based on the single character
        current_char = text[self.pos]
	integer_value = 0
	integer_flag = 0
	while current_char is " ":
	    self.pos += 1
	    if self.pos > len(text) - 1:
                return Token(EOF, None)
	    current_char = text[self.pos]
        while (current_char is not " " and current_char.isdigit()):
	    integer_value = integer_value*10+int(current_char)
	    integer_flag = 1
	    self.pos += 1
	    if self.pos >  len(text) - 1:
		break
	    current_char = text[self.pos]
	# if the character is a digit then convert it to
        # integer, create an INTEGER token, increment self.pos
        # index to point to the next character after the digit,
        # and return the INTEGER token
        #if current_char.isdigit():
        if integer_flag == 1:
	    token = Token(INTEGER, integer_value)
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
        
	self.error()

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type in token_type:
            if self.current_token.type is not EOF:
	        self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()
        """
        # we expect the current token to be a single-digit integer
        left = self.current_token
        self.eat(INTEGER)
	## we expect the current token to be a '+' token
        #op = self.current_token
        #self.eat(PLUS)
	# we expect the current token to be either of '+', '-', '*', '/' tokens
	op = self.current_token
	self.eat([MINUS,PLUS,MULTIPLY,DIVIDE])	

        # we expect the current token to be a single-digit integer
        right = self.current_token
        self.eat(INTEGER)

	#we expect the current token to be EOF
	self.eat(EOF)

        # at this point INTEGER PLUS INTEGER sequence of tokens
        # has been successfully found and the method can just
        # return the result of adding two integers, thus
        # effectively interpreting client input
        if op.type == PLUS:
		result = left.value + right.value
	if op.type == MINUS:
		result = left.value - right.value
	if op.type == MULTIPLY:
		result = left.value*right.value
	if op.type == DIVIDE:
		result = left.value*1.0/right.value
        # EOF token
        """
        next_token_type = INTEGER
        operands = []
        operators = []
        ops_list = [MINUS,PLUS,MULTIPLY,DIVIDE,EOF]
        while 1:
            token_type = next_token_type
            if self.current_token.type == INTEGER:
                next_token_type = ops_list
                operands.append(self.current_token)
            elif self.current_token.type in ops_list:
                if self.current_token.type == EOF:
                    self.eat(token_type)
                    break
                next_token_type = INTEGER
                operators.append(self.current_token.type)
            self.eat(token_type)

        while len(operators) > 0:
            if DIVIDE in operators:
                idx = operators.index(DIVIDE)
                operators.pop(idx)
                operands.insert(idx,Token(INTEGER,operands[idx].value*1.0/operands[idx+1].value))
                operands.pop(idx+1)
                operands.pop(idx+1)
                continue
            if MULTIPLY in operators:
                idx = operators.index(MULTIPLY)
                operators.pop(idx)
                operands.insert(idx,Token(INTEGER,operands[idx].value*operands[idx+1].value))
                operands.pop(idx+1)
                operands.pop(idx+1)
                continue
            if MINUS in operators:
                idx = operators.index(MINUS)
                operators.pop(idx)
                operands.insert(idx,Token(INTEGER,operands[idx].value-operands[idx+1].value))
                operands.pop(idx+1)
                operands.pop(idx+1)
                continue
            if PLUS in operators:
                idx = operators.index(PLUS)
                operators.pop(idx)
                operands.insert(idx,Token(INTEGER,operands[idx].value+operands[idx+1].value))
                operands.pop(idx+1)
                operands.pop(idx+1)
                continue

        result = operands[0].value
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
