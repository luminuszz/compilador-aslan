import unittest
import sys
import os

# Adiciona o diretório pai ao sys.path para que possamos importar o lexer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from lexer_lotr import LexerLotr, LexerError

class TestLexerLotr(unittest.TestCase):

    def test_lotr_keywords(self):
        """Testa se as palavras-chave do Senhor dos Anéis geram os tokens corretos."""
        code = """
        poder_maia chama_de_udun
        fogo_secreto sombras_profundas
        nao_passara fuja_tolos
        queda_em_khazaddum cajado_brilha ouvir_nas_trevas
        """
        lexer = LexerLotr(code)
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

    def test_lotr_simple_program(self):
        """Testa a tokenização de um fragmento de programa em LotR."""
        code = """
        poder_maia balrog = 100;
        nao_passara (balrog > 50) {
            cajado_brilha("You shall not pass!");
        }
        """
        lexer = LexerLotr(code)
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
