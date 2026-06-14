# tests/test_semantic.py
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lexer import Lexer
from parser_ import Parser
from semantic import SemanticAnalyzer, SemanticError

class TestSemanticAnalyzer(unittest.TestCase):

    def _build_ast(self, code):
        """Constrói a AST a partir do código para uso nos testes."""
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        return parser.parse()

    def test_undeclared_variable_assignment(self):
        """Verifica se o uso de uma variável não declarada em uma atribuição levanta um erro."""
        # A Fase 2 (Parser) ainda não sabe analisar uma atribuição solta,
        # então vamos começar com um caso que o parser já entende.
        # Por exemplo, usar uma variável não declarada em uma declaração.
        code = "int a = x;"
        ast = self._build_ast(code)
        
        analyzer = SemanticAnalyzer()
        
        # Esperamos que a análise levante um SemanticError
        with self.assertRaisesRegex(SemanticError, "Erro: Variável 'x' não declarada."):
            analyzer.visit(ast)

    def test_variable_redeclaration(self):
        """Verifica se declarar a mesma variável duas vezes no mesmo escopo levanta um erro."""
        code = "int x = 1; int x = 2;"
        ast = self._build_ast(code)
        
        analyzer = SemanticAnalyzer()
        
        with self.assertRaisesRegex(SemanticError, "Erro: Variável 'x' já declarada neste escopo."):
            analyzer.visit(ast)

    def test_variable_scope(self):
        """Verifica se variáveis declaradas dentro de um bloco não são acessíveis fora dele."""
        code = """
        int x = 10;
        if (x > 0) {
            int y = 5;
        }
        int z = y; // Erro: y está fora de escopo
        """
        ast = self._build_ast(code)
        
        analyzer = SemanticAnalyzer()
        
        with self.assertRaisesRegex(SemanticError, "Erro: Variável 'y' não declarada."):
            analyzer.visit(ast)

    def test_type_mismatch_assignment(self):
        """Verifica se a atribuição de um tipo incompatível levanta um erro."""
        code = "int x = true;"
        ast = self._build_ast(code)
        
        analyzer = SemanticAnalyzer()
        
        with self.assertRaisesRegex(SemanticError, "Erro: Tipo incompatível para a variável 'x'. Esperado 'INT', mas recebeu 'BOOL'."):
            analyzer.visit(ast)

if __name__ == '__main__':
    unittest.main()
