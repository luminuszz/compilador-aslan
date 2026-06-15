import unittest
import sys
import os

# Adiciona o diretório pai ao sys.path para que possamos importar o lexer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from lexer_narnia import LexerNarnia, LexerError

class TestLexerNarnia(unittest.TestCase):

    def test_narnia_keywords(self):
        """Testa se as palavras-chave de Nárnia geram os tokens corretos."""
        code = """
        rei_pedro rainha_lucia
        verdade_de_aslan mentira_de_edmundo
        pela_juba_do_leao pelo_rei_caspian
        durante_o_reinado proclamar ouvir_conselho
        """
        lexer = LexerNarnia(code)
        tokens = lexer.tokenize()
        
        expected_types = [
            'INT', 'BOOL', 
            'TRUE', 'FALSE', 
            'IF', 'ELSE', 
            'WHILE', 'PRINT', 'READ',
            'EOF'
        ]
        
        token_types = [t.type for t in tokens]
        self.assertEqual(token_types, expected_types)

    def test_narnia_simple_program(self):
        """Testa a tokenização de um fragmento de programa em Nárnia."""
        code = """
        rei_pedro x = 10;
        pela_juba_do_leao (x > 5) {
            proclamar("Narnia!");
        }
        """
        lexer = LexerNarnia(code)
        tokens = lexer.tokenize()
        
        # Tipos esperados na ordem
        expected_types = [
            'INT', 'IDENTIFICADOR', 'IGUAL', 'NUMERO', 'PONTO_VIRGULA',
            'IF', 'LPAREN', 'IDENTIFICADOR', 'MAIOR', 'NUMERO', 'RPAREN', 'LCHAVE',
            'PRINT', 'LPAREN', 'STRING', 'RPAREN', 'PONTO_VIRGULA',
            'RCHAVE',
            'EOF'
        ]
        token_types = [t.type for t in tokens]
        self.assertEqual(token_types, expected_types)

if __name__ == '__main__':
    unittest.main()
