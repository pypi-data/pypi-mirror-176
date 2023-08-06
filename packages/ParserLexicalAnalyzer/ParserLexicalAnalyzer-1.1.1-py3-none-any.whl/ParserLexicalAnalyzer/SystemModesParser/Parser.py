
class Parser:

    def __init__(self):
        self.tokens = []
        self.index = 0
        self.look = None
        self.updatedTokens = []

    def parse(self, tokens):
        self.tokens = tokens
        self.updatedTokens = []
        self.index = 0

        try:

            self.look = self.next_token()
            self.E()
            self.match("null")
            return self.updatedTokens
        except Exception as e:
            raise Exception("Error in parsing: " + e + "  But received: " + self.look["lexeme"])

    def E(self):
        self.E1()
        self.ER()

    def E1(self):
        self.E2()
        self.E1R()

    def ER(self):
        if self.look["type"] == "|":
            orToken = self.look
            self.match("|")
            self.E1()
            self.updatedTokens.append(orToken)
            self.ER()

    def E1R(self):
        if self.look["type"] == "&":
            andToken = self.look
            self.match("&")
            self.E2()
            self.updatedTokens.append(andToken)
            self.E1R()

    def E2(self):
        if self.look["type"] == "id":
            self.updatedTokens.append(self.look)
            self.match("id")
        elif self.look["type"] == "!":
            notToken = self.look
            self.match("!")
            self.E();
            self.updatedTokens.append(notToken)
        elif self.look["type"] == "(":
            self.match("(")
            self.E()
            self.match(")")
        else:
            raise Exception("Expecting variable, numeric_constant, (")

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
