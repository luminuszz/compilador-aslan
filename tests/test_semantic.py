import unittest
from lexer import Lexer
from parser_ import Parser
from semantic import SemanticAnalyzer, SemanticError

class TestSemantic(unittest.TestCase):
    def test_variavel_nao_declarada(self):
        code = "int x = y + 1;"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        with self.assertRaises(SemanticError):
            analyzer.visit(ast)

    def test_declaracao_duplicada(self):
        code = "int x = 1; int x = 2;"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        with self.assertRaises(SemanticError):
            analyzer.visit(ast)