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

        # Esperado:
        # t1 = 10 + 5
        # x = t1
        expected = [("MAIS", "10", "5", "t1"), ("ASSIGN", "t1", None, "x")]
        self.assertEqual(ir, expected)

    def test_assignment_ir(self):
        """Testa a geração de TAC para uma atribuição simples."""
        code = "int x; x = 20;"
        ir = self._generate_ir(code)

        # Esperado: x = 20
        expected = [("ASSIGN", "20", None, "x")]
        self.assertEqual(ir, expected)

    def test_io_ir(self):
        """Testa a geração de TAC para comandos print e read."""
        code = "int x; read(x); print(x + 1);"
        ir = self._generate_ir(code)

        # Esperado:
        # read x
        # t1 = x + 1
        # print t1
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

        # Esperado (exemplo):
        # x = 10
        # t1 = x > 0
        # jump_if_false t1 L1
        # print 1
        # jump L2
        # label L1
        # print 0
        # label L2
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

        # Esperado (exemplo):
        # i = 0
        # label L1
        # t1 = i < 3
        # jump_if_false t1 L2
        # print i
        # t2 = i + 1
        # i = t2
        # jump L1
        # label L2
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


if __name__ == "__main__":
    unittest.main()
