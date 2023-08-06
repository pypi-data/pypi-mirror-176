from ParserLexicalAnalyzer.SimpleExpressionParser.LexicalAnalyzer import SimpleLexicalAnalyzer
from ParserLexicalAnalyzer.SimpleExpressionParser.Parser import SimpleParser
from ParserLexicalAnalyzer.PropertyParser.LexicalAnalyzer import PropertyLexicalAnalyzer
from ParserLexicalAnalyzer.PropertyParser.Parser import PropertyParser
from ParserLexicalAnalyzer.SystemModesParser.Parser import Parser
from ParserLexicalAnalyzer.SystemModesParser.LexicalAnalyzer import LexicalAnalyzer

def expressionParser(string):
    lex = SimpleLexicalAnalyzer()
    parser = SimpleParser()
    tokens = lex.get_tokens(string)
    parsed_string = parser.parse(tokens)
    return parsed_string

def systemModeParser(string):
    lex = LexicalAnalyzer()
    parser = Parser()
    tokens = lex.get_tokens(string)
    # return tokens
    parsed_string = parser.parse(tokens)
    return parsed_string

def propertyParser(string):
    lex = PropertyLexicalAnalyzer()
    parser = PropertyParser()
    tokens = lex.get_tokens(string)
    parsed_string = parser.parse(tokens)
    return parsed_string

print(expressionParser("a+b-(c*d)"))