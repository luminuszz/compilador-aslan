# tests/test_ir_generator.py
import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from ir_generator import IRGenerator
from lexer import Lexer
from parser_ import Parser
from semantic import SemanticAnalyzer


class TestIRGenerator(unittest.TestCase):
    def _generate_ir(self, code):
        """Helper para rodar o pipeline completo até a geração de IR."""
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        analyzer = SemanticAnalyzer()
        analyzer.visit(ast)

        generator = IRGenerator()
        generator.visit(ast)
        return generator.instructions

    def test_simple_arithmetic_ir(self):
        """Testa a geração de TAC para uma expressão aritmética simples."""
        code = "int x = 10 + 5;"
        ir = self._generate_ir(code)
        expected = [("MAIS", "10", "5", "t1"), ("ASSIGN", "t1", None, "x")]
        self.assertEqual(ir, expected)

    def test_assignment_ir(self):
        """Testa a geração de TAC para uma atribuição simples."""
        code = "int x; x = 20;"
        ir = self._generate_ir(code)
        expected = [("ASSIGN", "20", None, "x")]
        self.assertEqual(ir, expected)

    def test_io_ir(self):
        """Testa a geração de TAC para comandos print e read."""
        code = "int x; read(x); print(x + 1);"
        ir = self._generate_ir(code)
        expected = [
            ("READ", None, None, "x"),
            ("MAIS", "x", "1", "t1"),
            ("PRINT", "t1", None, None),
        ]
        self.assertEqual(ir, expected)

    def test_if_ir(self):
        """Testa a geração de TAC para o comando IF."""
        code = """
        int x = 10;
        if (x > 0) {
            print(1);
        } else {
            print(0);
        }
        """
        ir = self._generate_ir(code)
        expected = [
            ("ASSIGN", "10", None, "x"),
            ("MAIOR", "x", "0", "t1"),
            ("JUMP_IF_FALSE", "t1", None, "L1"),
            ("PRINT", "1", None, None),
            ("JUMP", None, None, "L2"),
            ("LABEL", "L1", None, None),
            ("PRINT", "0", None, None),
            ("LABEL", "L2", None, None),
        ]
        self.assertEqual(ir, expected)

    def test_while_ir(self):
        """Testa a geração de TAC para o comando WHILE."""
        code = """
        int i = 0;
        while (i < 3) {
            print(i);
            i = i + 1;
        }
        """
        ir = self._generate_ir(code)
        expected = [
            ("ASSIGN", "0", None, "i"),
            ("LABEL", "L1", None, None),
            ("MENOR", "i", "3", "t1"),
            ("JUMP_IF_FALSE", "t1", None, "L2"),
            ("PRINT", "i", None, None),
            ("MAIS", "i", "1", "t2"),
            ("ASSIGN", "t2", None, "i"),
            ("JUMP", None, None, "L1"),
            ("LABEL", "L2", None, None),
        ]
        self.assertEqual(ir, expected)

    def test_string_ir(self):
        """Testa se strings literais são preservadas com aspas no TAC."""
        code = 'print("hello");'
        ir = self._generate_ir(code)
        expected = [("PRINT", '"hello"', None, None)]
        self.assertEqual(ir, expected)

    def test_new_comparisons_ir(self):
        """Testa a geração de TAC para os novos operadores de comparação."""
        code = "int x = 1; int y = 2; bool r = (x >= y); int a = 3; int b = 4; bool r2 = (a != b);"
        ir = self._generate_ir(code)
        self.assertEqual(ir[2], ("MAIOR_IGUAL", "x", "y", "t1"))
        self.assertEqual(ir[6], ("DIFERENTE", "a", "b", "t2"))


if __name__ == "__main__":
    unittest.main()
