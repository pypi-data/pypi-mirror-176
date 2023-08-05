from LexicalAnalyzer import LexicalAnalyzer
from Parser import Parser

def parse(string):
    lex = LexicalAnalyzer()
    parser = Parser()
    tokens = lex.get_tokens(string)
    parsed_string = parser.parse(tokens)
    return parsed_string


print(parse("a+b-c"))