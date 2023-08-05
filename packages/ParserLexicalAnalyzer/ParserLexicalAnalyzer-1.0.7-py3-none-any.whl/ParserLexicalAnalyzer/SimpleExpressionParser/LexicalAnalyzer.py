
class SimpleLexicalAnalyzer():

    def __init__(self):
        self.tokens = []
        self.original_string = ""
        self.key_words = ["and", "or", "not", "xor", "ite", "as", "let", "exists", "forall", "par"]

    def get_tokens(self, string):

        self.tokens = []
        self.original_string = string

        string = string.replace('\n', ' ').strip()
        string = string.replace('\t', ' ').strip()
        string = string + ' '  # to check other for last token

        i = 0
        j = 1

        while i < len(string) and j <= len(string):

            temp = string[i: j]

            if  self.is_arithmatic_operator(temp) or self.is_symbol(temp):
                temp = temp[0: -1]
                self.tokens.append({"type": temp, "lexeme": temp})
                i = j- 1
                j = j - 1
            elif self.is_numeric_constant(temp):
                temp = temp[0: -1]
                self.tokens.append({"type": "nc", "lexeme": temp})
                i = j - 1
                j = j - 1
            elif self.is_identifier(temp):
                temp = temp[0: -1]
                if temp in self.key_words:
                    raise Exception(
                        "Error in parsing tokens: " + self.original_string + " Identifier: " + temp + "is from keywords list")
                else:
                    self.tokens.append({"type": "id", "lexeme": temp})
                i = j - 1
                j = j - 1

            if i == j and string[i] == ' ':
                i = i + 1

            j = j + 1

        if i < j - 2:
            raise Exception(
                "Error in parsing tokens: " + self.original_string + " Unexpected character received :" + temp)

        return self.tokens

    def is_arithmatic_operator(self, string):
        # +, -, *, /,
        st = 0
        for i in range(0, len(string)):
            if st == 0:
                if string[i] == "+" or string[i] == "-" or string[i] == "*" or string[i] == "/":
                    st = 1
                else:
                    return False
            elif st == 1:
                return True
        return False

    def is_symbol(self, string):
        # (, )
        st = 0
        for i in range(0, len(string)):
            if st == 0:
                if string[i] == "(" or string[i] == ")":
                    st = 1
                else:
                    return False
            elif st == 1:
                return True
        return False

    def is_numeric_constant(self, string):
        # 123, 123.123, 123e+1, 123e-1, 123e1, 123.123e+1, 123.123e-1, 123.123e1, 123.123E1
        st = 0
        for i in range(0, len(string)):
            if st == 0:
                # here ord() returns the unicode point against a single character
                if 48 <= ord(string[i]) <= 57:
                    st = 1
                else:
                    return False

            elif st == 1:
                if 48 <= ord(string[i]) <= 57:
                    st = 1
                elif string[i] == '.':
                    st = 2
                elif string[i] == 'e' or string[i] == 'E':
                    st = 4
                else:
                    return True

            elif st == 2:
                if 48 <= ord(string[i]) <= 57:
                    st = 3
                else:
                    return False

            elif st == 3:
                if 48 <= ord(string[i]) <= 57:
                    st = 3
                elif string[i] == 'e' or string[i] == 'E':
                    st = 4
                else:
                    return True

            elif st == 4:
                if string[i] == '+' or string[i] == '-':
                    st = 5
                elif 48 <= ord(string[i]) <= 57:
                    st = 6
                else:
                    return False

            elif st == 5:
                if 48 <= ord(string[i]) <= 57:
                    st = 6
                else:
                    return False

            elif st == 6:
                if 48 <= ord(string[i]) <= 57:
                    st = 6
                else:
                    return True

        return False

    def is_identifier(self, string):
        # check for identifier [ 48_57: 0-9     65_90: A_Z     97_122: a_z  underscore '_' ]
        st = 0
        for i in range(0, len(string)):
            if st == 0:
                if 65 <= ord(string[i]) <= 90 or 97 <= ord(string[i]) <= 122 or string[i] == '_':
                    st = 1
                else:
                    return False
            elif st == 1:
                if 48 <= ord(string[i]) <= 57 or 65 <= ord(string[i]) <= 90 or 97 <= ord(string[i]) <= 122 or string[
                    i] == '_':
                    st = 1
                else:
                    return True
        return False
