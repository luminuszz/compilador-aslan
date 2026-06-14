# tests/test_optimizer.py
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lexer import Lexer
from parser_ import Parser, Numero, Booleano
from optimizer import Optimizer

class TestOptimizer(unittest.TestCase):

    def _get_optimized_ast(self, code):
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        optimizer = Optimizer()
        return optimizer.visit(ast)

    def test_constant_folding_arithmetic(self):
        """Verifica se 10 + 5 * 2 é simplificado para 20 durante a compilação."""
        code = "int x = 10 + 5 * 2;"
        ast = self._get_optimized_ast(code)
        
        # A declaração deve ter um Numero(20) como expressão, não uma OperacaoBinaria
        expr = ast.declaracoes[0].expressao
        self.assertIsInstance(expr, Numero)
        self.assertEqual(expr.valor, 20)

    def test_constant_folding_comparison(self):
        """Verifica se 10 > 5 é simplificado para True durante a compilação."""
        code = "bool res = 10 > 5;"
        ast = self._get_optimized_ast(code)
        
        expr = ast.declaracoes[0].expressao
        self.assertIsInstance(expr, Booleano)
        self.assertEqual(expr.valor, True)

    def test_nested_optimization(self):
        """Verifica otimização dentro de blocos e condicionais."""
        code = "if (10 == 10) { int y = 2 + 2; }"
        ast = self._get_optimized_ast(code)
        
        # Condição do IF deve ser True
        self.assertIsInstance(ast.declaracoes[0].condicao, Booleano)
        self.assertEqual(ast.declaracoes[0].condicao.valor, True)
        
        # Declaração interna deve ser 4
        inner_expr = ast.declaracoes[0].bloco_then.declaracoes[0].expressao
        self.assertIsInstance(inner_expr, Numero)
        self.assertEqual(inner_expr.valor, 4)

if __name__ == '__main__':
    unittest.main()
