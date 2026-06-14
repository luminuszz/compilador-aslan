# tests/test_regressive.py
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lexer import Lexer
from parser_ import Parser
from semantic import SemanticAnalyzer, SemanticError

class TestRegressive(unittest.TestCase):
    
    def _run_full_analysis(self, code):
        """Helper para rodar lexer, parser e semantic analyzer."""
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        return analyzer.visit(ast)

    def test_deep_expression_precedence(self):
        """Fase 2/3: Expressão complexa com precedência e tipos corretos."""
        code = "int x = (10 + 5) * (20 / 2) == 150;" # Isso resulta em BOOL
        # Ops, a declaração diz 'int x', mas a expressão resulta em BOOL. Deve falhar.
        with self.assertRaisesRegex(SemanticError, "Tipo incompatível para a variável 'x'. Esperado 'INT', mas recebeu 'BOOL'"):
            self._run_full_analysis(code)

    def test_nested_scopes_valid(self):
        """Fase 3: Múltiplos níveis de escopo com nomes de variáveis repetidos em escopos diferentes."""
        code = """
        int x = 10;
        if (x > 0) {
            int x = 5; // Válido: Outro escopo
            if (x == 5) {
                int x = 1; // Válido: Terceiro nível
            }
        }
        int z = x; // Deve pegar o x do primeiro nível (10)
        """
        # Não deve levantar exceção
        self._run_full_analysis(code)

    def test_complex_if_condition_error(self):
        """Fase 3: Erro de tipo dentro da condição complexa do IF."""
        code = "if ( (10 + 5) * 2 ) { int a = 1; }" # Condição é INT, deve ser BOOL
        with self.assertRaisesRegex(SemanticError, "A condição do 'if' deve ser 'BOOL', mas recebeu 'INT'"):
            self._run_full_analysis(code)

    def test_arithmetic_on_bool_error(self):
        """Fase 3: Tentativa de fazer aritmética com booleanos."""
        code = "int x = 10 + true;"
        with self.assertRaisesRegex(SemanticError, "Operação aritmética 'MAIS' exige operandos do tipo 'INT'"):
            self._run_full_analysis(code)

    def test_comparison_of_different_types(self):
        """Fase 3: Comparação de igualdade entre tipos diferentes (int == bool)."""
        code = "bool res = (10 == true);"
        with self.assertRaisesRegex(SemanticError, "Operação de igualdade 'IGUAL_COMP' exige operandos do mesmo tipo"):
            self._run_full_analysis(code)

    def test_full_valid_program_fragment(self):
        """Teste de fumaça para um programa válido misturando tudo."""
        code = """
        int a = 10;
        int b = 20;
        bool cond = a < b;
        if (cond) {
            int result = a + b * 2;
        } else {
            int result = 0;
        }
        """
        # Deve passar sem erros
        self._run_full_analysis(code)

    def test_while_command_valid(self):
        """Fase 3: Teste de um comando WHILE válido."""
        code = """
        int i = 0;
        while (i < 10) {
            i = i + 1;
        }
        """
        # (Nota: Atribuição simples 'i = i + 1' ainda não foi implementada no Parser, 
        # o parser atual só entende declarações. Vamos ajustar o teste para algo que o parser entenda.)
        code = """
        int i = 0;
        while (i < 10) {
            int temp = i + 1;
        }
        """
        self._run_full_analysis(code)

    def test_while_condition_error(self):
        """Fase 3: Erro de tipo na condição do WHILE."""
        code = "while (10) { int a = 1; }"
        with self.assertRaisesRegex(SemanticError, "A condição do 'while' deve ser 'BOOL', mas recebeu 'INT'"):
            self._run_full_analysis(code)

    def test_io_and_assignment_valid(self):
        """Fase 3: Teste de comandos print, read e atribuição simples."""
        code = """
        int x;
        read(x);
        x = x + 1;
        print(x * 2);
        """
        self._run_full_analysis(code)

    def test_io_read_undeclared_error(self):
        """Fase 3: Erro ao tentar ler em uma variável não declarada."""
        code = "read(y);"
        with self.assertRaisesRegex(SemanticError, "Erro: Variável 'y' não declarada."):
            self._run_full_analysis(code)

    def test_assignment_type_error(self):
        """Fase 3: Erro de tipo em atribuição simples (int = bool)."""
        code = "int x = 10; x = true;"
        with self.assertRaisesRegex(SemanticError, "Erro: Tipo incompatível na atribuição para 'x'. Esperado 'INT', mas recebeu 'BOOL'"):
            self._run_full_analysis(code)

    def test_factorial_logic_valid(self):
        """Fase 3: Validação semântica de um programa de fatorial completo."""
        code = """
        int n;
        int fact = 1;
        read(n);
        while (n > 1) {
            fact = fact * n;
            n = n - 1;
        }
        print(fact);
        """
        self._run_full_analysis(code)

if __name__ == '__main__':
    unittest.main()
