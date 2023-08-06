
class PropertyParser:

    def __init__(self):
        self.tokens = []
        self.index = 0
        self.look = None

    def parse(self, tokens):
        print(tokens)
        self.tokens = tokens
        self.index = 0
        try:
            self.look = self.next_token()
            self.PROP()
            self.match("null")
            return True
        except Exception as e:
            raise Exception("Error in parsing: " + e + "  But received: " + self.look["lexeme"])

    def E(self):
        self.E1()
        self.ER()

    def ER(self):
        if self.look["type"] in ["=>", "|", "&", "=", "!=", "<=", ">=", ">", "<", "+", "-", "*", "/", "%"]:
            self.stack.append(self.look["type"])
            self.OP()
            self.E1()
            self.ER()

    def E1(self):
        if self.look["type"] in ["id", "true", "false", "nc"]:
            self.match(self.look["type"])
        elif self.look["type"] == "!":
            self.match("!")
            self.E2()
        elif self.look["type"] == "(":
            self.match("(")
            self.E3()
        else:
            raise Exception("Expecting variable, boolean_value, numeric_constant, (")

    def E2(self):
        if self.look["type"] == "(":
            self.match("(")
            self.E()
            self.match(")")
        elif self.look["type"] in ["id", "true", "false"]:
            self.match(self.look["type"])
        else:
            raise Exception("Expecting variable,boolean_values, (")

    def E3(self):
        if self.look["type"] in ["+", "-"]:
            self.OP1()
            self.match("nc")
            self.match(")")
        elif self.look["type"] in ["id", "true", "false", "nc", "!", "("]:
            self.E()
            self.match(")")

    def PROP(self):
        if self.look["type"] == "nc" and self.look["lexeme"] == "1":
            self.match("nc")
            self.match("-")
            self.match("P")
            self.OP2()
            self.TYPE()
            self.match("[")
            self.PF()
            self.match("]")
        elif self.look["type"] == "P":
            self.match("P")
            self.OP2()
            self.TYPE()
            self.match("[")
            self.PF()
            self.match("]")
        elif self.look["type"] == "T":
            self.match("T")
            self.OP2()
            self.TYPE()
            self.match("[")
            self.RF()
            self.match("]")
        elif self.look["type"] in ["LRA", "S"]:
            self.LR()
            self.OP2()
            self.TYPE()
            self.match("[")
            self.SF()
            self.match("]")
        else:
            raise Exception("Expecting numeric_constant, 1, P, T, LRA, S")

    def TYPE(self):
        if self.look["type"] == "=":
            self.match("=")
            self.match("?")
        elif self.look["type"] in ["<=", ">=", ">", "<"]:
            self.OP3()
            self.E()
        else:
            raise Exception("Expecting =,<=,>=,>,<")

    def LR(self):
        if self.look["type"] in ["LRA", "S"]:
            self.match(self.look["type"])
        else:
            raise Exception("Expecting LRA, S")

    def PF(self):
        if self.look["type"] in ["G", "F"]:
            self.OP4()
            self.BE()
            self.SF()
        elif self.look["type"] in ["P", "LRA", "S", "!", "id", "true", "false", "nc", "("]:
            self.SF()
            self.OP5()
            self.BE()
            self.SF()
        else:
            raise Exception("Expecting variable, boolean_values, numeric_constant, F, G, P, S, LRA, !, (")

    def BE(self):
        if self.look["type"] == "^":
            self.match("^")
            self.match("{")
            self.B()
            self.match("}")
        elif self.look["type"] == "{":
            self.match("{")
            self.B()
            self.match("}")
        elif self.look["type"] in ["[", "<=", ">=", "<", ">"]:
            self.B()

    def B(self):
        if self.look["type"] == "[":
            self.match("[")
            self.E()
            self.match(",")
            self.E()
            self.match("]")
        elif self.look["type"] in ["<=", ">=", "<", ">"]:
            self.OP3()
            self.TIME()
        else:
            raise Exception("Expecting [, ',' ,[, ], <=,>=,<,>")

    def TIME(self):

        if self.look["type"] == "(":
            self.match("(")
            self.E()
            self.match(")")
        elif self.look["type"] == "nc":
            self.match("nc")
        else:
            raise Exception("Expecting numeric_constant, (")

    def RF(self):
        if self.look["type"] == "I":
            self.match("I")
            self.match("=")
            self.E()
        elif self.look["type"] == "C":
            self.match("C")
            self.match("<=")
            self.E()
        elif self.look["type"] == "F":
            self.match("F")
            self.SF()
        elif self.look["type"] in ["LRA", "S"]:
            self.LR()
        else:
            raise Exception("Expecting C,F,I,S,LRA")

    def SF(self):
        self.SF1()
        self.SFR()

    def SFR(self):
        if self.look["type"] in ["|", "&"]:
            self.OP6()
            self.SF1()
            self.SFR()

    def SF1(self):
        if self.look["type"] == "P":
            self.match("P")
            self.OP2()
            self.OP3()
            self.E()
            self.match("[")
            self.PF()
            self.match("]")
        elif self.look["type"] == "LRA" or self.look["type"] == "S":
            self.LR()
            self.OP2()
            self.OP3()
            self.E()
            self.match("[")
            self.SF()
            self.match("]")
        elif self.look["type"] == "!":
            self.match("!")
            self.exception()
        elif self.look["type"] in ["id", "true", "false", "nc", "("]:
            self.E()
        else:
            raise Exception("Expecting variable, boolean_value, numeric_constant,!,S,P,LRA")

    def exception(self):
        if self.look["type"] == "P":
            self.match("P")
            self.OP2()
            self.OP3()
            self.E()
            self.match("[")
            self.PF()
            self.match("]")
        elif self.look["type"] == "LRA" or self.look["type"] == "S":
            self.LR()
            self.OP2()
            self.OP3()
            self.E()
            self.match("[")
            self.SF()
            self.match("]")
        elif self.look["type"] in ["id", "true", "false", "("]:
            self.E2()
        else:
            raise Exception("Expecting variable, boolean_value, (,P,S,LRA")

    def OP(self):
        if self.look["type"] in ["=>", "|", "&", "=", "!=", "<=", ">=", ">", "<", "+", "-", "*", "/", "%"]:
            self.match(self.look["type"])
        else:
            raise Exception("Expecting =>, |, &, =, !=, <=, >=, >, <, +, -, *, /, %")

    def OP1(self):
        if self.look["type"] in ["+", "-"]:
            self.match(self.look["type"])
        else:
            raise Exception("Expecting +, -")

    def OP2(self):
        if self.look["type"] in ["min", "max"]:
            self.match(self.look["type"])

    def OP3(self):
        if self.look["type"] in [">", "<", ">=", "<="]:
            self.match(self.look["type"])
        else:
            raise Exception("Expecting  >, <, >=, <=")

    def OP4(self):
        if self.look["type"] in ["G", "F"]:
            self.match(self.look["type"])
        else:
            raise Exception("Expecting G,F")

    def OP5(self):
        if self.look["type"] in ["U", "W", "R"]:
            self.match(self.look["type"])
        else:
            raise Exception("Expecting U, W, R")

    def OP6(self):
        if self.look["type"] in ["&", "|"]:
            self.match(self.look["type"])
        else:
            raise Exception("Expecting & , |")

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
