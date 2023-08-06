class SimpleParser:

    def __init__(self):
        self.tokens = []
        self.index = 0
        self.look = None
        self.stack = []

    def parse(self, tokens):
        self.tokens = tokens
        self.stack = []
        self.index = 0

        try:
            self.look = self.next_token()
            self.E()
            self.match("null")
            return self.stack.pop()
        except Exception as e:
            raise Exception("Error in parsing: " + e + "  But received: " + self.look["lexeme"])

    def E(self):
        self.E1()
        self.ER()

    def E1(self):
        self.E2()
        self.E1R()

    def ER(self):
        if self.look["type"] == "+" or self.look["type"] == "-":
            self.stack.append(self.look["type"])
            self.OP1()
            self.E1()
            right_operand = self.stack.pop()
            op = self.stack.pop()
            left_operand = self.stack.pop()
            updated_expression = "( " + op + " " + left_operand + " " + right_operand + " )"
            self.stack.append(updated_expression)
            self.ER()

    def E1R(self):
        if self.look["type"] == "*" or self.look["type"] == "/":
            self.stack.append(self.look["type"])
            self.OP2()
            self.E2()
            right_operand = self.stack.pop()
            op = self.stack.pop()
            left_operand = self.stack.pop()

            if op == "/" and right_operand != right_operand or right_operand == '0':
                raise Exception("Can not divide by variable or zero")

            updated_expression = "( " + op + " " + left_operand + " " + right_operand + " )"
            self.stack.append(updated_expression)
            self.E1R()

    def E2(self):
        if self.look["type"] == "id":
            self.stack.append(self.look["lexeme"])
            self.match("id")
        elif self.look["type"] == "nc":
            self.stack.append(self.look["lexeme"])
            self.match("nc")
        elif self.look["type"] == "(":
            self.match("(")
            self.E()
            self.match(")")
        else:
            raise Exception("Expecting variable, numeric_constant, (")

    def OP1(self):
        if self.look["type"] == "+":
            self.match("+")
        elif self.look["type"] == "-":
            self.match("-")
        else:
            raise Exception("Expecting +, -")

    def OP2(self):
        if self.look["type"] == "*":
            self.match("*")
        elif self.look["type"] == "/":
            self.match("/")
        else:
            raise Exception("Expecting *, /")

    def next_token(self):
        if self.index == len(self.tokens):
            return {"type": "null", "lexeme": "null"}
        index = self.index
        self.index = self.index + 1
        return self.tokens[index]

    def match(self, string):
        if self.look["type"] == string:
            self.look = self.next_token()
        else:
            raise Exception("Expecting " + string)
