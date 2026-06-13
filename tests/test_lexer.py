# tests/test_lexer.py
import unittest
import sys
import os

# Adiciona o diretório pai ao sys.path para que possamos importar o lexer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lexer import Lexer, LexerError

class TestLexer(unittest.TestCase):

    def _assert_tokens(self, code, expected_tokens):
        """Função auxiliar para comparar tokens, ignorando linha/coluna para simplicidade."""
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        # Compara tipo e valor, mas ignora linha/coluna
        token_pairs = [(t.type, t.value) for t in tokens]
        
        # Adiciona o EOF esperado no final
        expected_tokens.append(('EOF', ''))
        
        self.assertEqual(token_pairs, expected_tokens)

    def test_keywords(self):
        code = "if else while print read int bool true false"
        expected = [
            ('IF', 'if'), ('ELSE', 'else'), ('WHILE', 'while'),
            ('PRINT', 'print'), ('READ', 'read'), ('INT', 'int'),
            ('BOOL', 'bool'), ('TRUE', 'true'), ('FALSE', 'false')
        ]
        self._assert_tokens(code, expected)

    def test_operators(self):
        code = "+ - * / == != < > = <= >="
        expected = [
            ('MAIS', '+'), ('MENOS', '-'), ('MULT', '*'), ('DIV', '/'),
            ('IGUAL_COMP', '=='), ('DIFERENTE', '!='), ('MENOR', '<'),
            ('MAIOR', '>'), ('IGUAL', '='), ('MENOR_IGUAL', '<='),
            ('MAIOR_IGUAL', '>=')
        ]
        self._assert_tokens(code, expected)

    def test_literals_and_identifiers(self):
        code = 'var1 = 123 "hello" var2'
        expected = [
            ('IDENTIFICADOR', 'var1'), ('IGUAL', '='), ('NUMERO', '123'),
            ('STRING', '"hello"'), ('IDENTIFICADOR', 'var2')
        ]
        self._assert_tokens(code, expected)

    def test_delimiters(self):
        code = "() {} ;"
        expected = [
            ('LPAREN', '('), ('RPAREN', ')'), ('LCHAVE', '{'),
            ('RCHAVE', '}'), ('PONTO_VIRGULA', ';')
        ]
        self._assert_tokens(code, expected)

    def test_ignore_whitespace_and_comments(self):
        code = """
            // isto é um comentário
            if (x > 10) // outro comentário
            {
                print("hello"); // fim
            }
        """
        expected = [
            ('IF', 'if'), ('LPAREN', '('), ('IDENTIFICADOR', 'x'),
            ('MAIOR', '>'), ('NUMERO', '10'), ('RPAREN', ')'),
            ('LCHAVE', '{'), ('PRINT', 'print'), ('LPAREN', '('),
            ('STRING', '"hello"'), ('RPAREN', ')'), ('PONTO_VIRGULA', ';'),
            ('RCHAVE', '}')
        ]
        self._assert_tokens(code, expected)

    def test_combined_expression(self):
        code = "int result = (10 + value) * 2;"
        expected = [
            ('INT', 'int'), ('IDENTIFICADOR', 'result'), ('IGUAL', '='),
            ('LPAREN', '('), ('NUMERO', '10'), ('MAIS', '+'),
            ('IDENTIFICADOR', 'value'), ('RPAREN', ')'), ('MULT', '*'),
            ('NUMERO', '2'), ('PONTO_VIRGULA', ';')
        ]
        self._assert_tokens(code, expected)

    def test_invalid_character(self):
        code = "int a = @;"
        # A asserção aqui verifica se o erro esperado é levantado
        with self.assertRaisesRegex(LexerError, "Caractere inválido '@' na linha 1, coluna 9"):
            lexer = Lexer(code)
            lexer.tokenize()

    def test_unterminated_string(self):
        # O lexer atual aceita qualquer coisa entre aspas.
        # Para detectar strings não terminadas, precisaríamos de uma regra mais complexa
        # ou pós-processamento, o que foge do escopo de um lexer simples baseado em regex.
        # Por enquanto, este teste apenas documenta o comportamento atual.
        code = '"hello'
        # O regex r'"[^"]*"' não vai dar match se não houver aspas de fechamento
        # então o " vai ser pego pela regra de erro
        with self.assertRaisesRegex(LexerError, 'Caractere inválido \'"\' na linha 1, coluna 1'):
            lexer = Lexer(code)
            lexer.tokenize()

if __name__ == '__main__':
    unittest.main()
