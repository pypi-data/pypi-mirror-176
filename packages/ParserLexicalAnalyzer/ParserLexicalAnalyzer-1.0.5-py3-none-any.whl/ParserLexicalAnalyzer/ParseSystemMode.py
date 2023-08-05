# from LexicalAnalyzer import LexicalAnalyzer
# from Parser import Parser
#
#
# class ParseSimpleExpression():
#     __instance = None
#
#     def __init__(self):
#         if ParseSimpleExpression.__instance is not None:
#             raise Exception("ParseSimpleExpression is instantiated")
#
#         self.lexical_analyzer = LexicalAnalyzer()
#         self.parser = Parser()
#         ParseSimpleExpression.__instance = self
#
#     @staticmethod
#     def parse(string):
#         assert ParseSimpleExpression.__instance is not None
#         tokens = ParseSimpleExpression.__instance.lexical_analyzer.get_tokens(string)
#         parsed_string = ParseSimpleExpression.__instance.parser.parse(tokens)
#         return parsed_string
#
#
# def parse(string):
#     lex = LexicalAnalyzer()
#     parser = Parser()
#     tokens = lex.get_tokens(string)
#     parsed_string = parser.parse(tokens)
#     return parsed_string