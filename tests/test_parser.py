# tests/test_parser.py
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lexer import Lexer
from parser_ import Parser, DeclaracaoVariavel, Numero, Identificador, OperacaoBinaria, ComandoIf, Bloco

class TestParser(unittest.TestCase):

    def test_declaracao_variavel(self):
        # Passo 1: Código fonte de exemplo
        code = "int x = 10;"

        # Passo 2: Obter os tokens
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        # Passo 3: Criar o parser e analisar
        parser = Parser(tokens)
        ast = parser.parse() # Isso vai retornar None, fazendo o teste falhar.
        
        # Passo 4: Definir a AST esperada
        # O programa deve conter uma única declaração.
        self.assertIsNotNone(ast)
        self.assertEqual(len(ast.declaracoes), 1)
        
        # A declaração deve ser uma Declaração de Variável
        decl = ast.declaracoes[0]
        self.assertIsInstance(decl, DeclaracaoVariavel)
        
        # O tipo deve ser 'int'
        self.assertEqual(decl.tipo.type, 'INT')
        
        # O nome da variável deve ser 'x'
        self.assertEqual(decl.nome_variavel.nome, 'x')
        
        # A expressão deve ser o número 10
        self.assertIsInstance(decl.expressao, Numero)
        self.assertEqual(decl.expressao.valor, 10)

    def test_expressao_binaria_simples(self):
        code = "int result = 10 + 5;"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # A AST deve ter uma declaração
        self.assertEqual(len(ast.declaracoes), 1)
        decl = ast.declaracoes[0]
        self.assertIsInstance(decl, DeclaracaoVariavel)

        # A expressão da declaração deve ser uma OperacaoBinaria
        expr = decl.expressao
        self.assertIsInstance(expr, OperacaoBinaria)

        # Verifica os componentes da operação
        self.assertIsInstance(expr.esquerda, Numero)
        self.assertEqual(expr.esquerda.valor, 10)
        self.assertEqual(expr.op.type, 'MAIS')
        self.assertIsInstance(expr.direita, Numero)
        self.assertEqual(expr.direita.valor, 5)

    def test_precedencia_operadores(self):
        code = "int result = 10 + 5 * 2;"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # A expressão principal deve ser uma operação de adição
        decl = ast.declaracoes[0]
        expr = decl.expressao
        self.assertIsInstance(expr, OperacaoBinaria)
        self.assertEqual(expr.op.type, 'MAIS')

        # O operando esquerdo da adição deve ser o número 10
        self.assertIsInstance(expr.esquerda, Numero)
        self.assertEqual(expr.esquerda.valor, 10)

        # O operando direito da adição deve ser OUTRA operação (a multiplicação)
        expr_mult = expr.direita
        self.assertIsInstance(expr_mult, OperacaoBinaria)
        self.assertEqual(expr_mult.op.type, 'MULT')
        
        # Verificando a sub-expressão de multiplicação
        self.assertIsInstance(expr_mult.esquerda, Numero)
        self.assertEqual(expr_mult.esquerda.valor, 5)
        self.assertIsInstance(expr_mult.direita, Numero)
        self.assertEqual(expr_mult.direita.valor, 2)

    def test_expressao_com_parenteses(self):
        code = "int result = (10 + 5) * 2;"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # A expressão principal deve ser uma operação de multiplicação
        decl = ast.declaracoes[0]
        expr = decl.expressao
        self.assertIsInstance(expr, OperacaoBinaria)
        self.assertEqual(expr.op.type, 'MULT')

        # O operando direito da multiplicação deve ser o número 2
        self.assertIsInstance(expr.direita, Numero)
        self.assertEqual(expr.direita.valor, 2)

        # O operando esquerdo da multiplicação deve ser OUTRA operação (a adição)
        expr_add = expr.esquerda
        self.assertIsInstance(expr_add, OperacaoBinaria)
        self.assertEqual(expr_add.op.type, 'MAIS')
        
        # Verificando a sub-expressão de adição
        self.assertIsInstance(expr_add.esquerda, Numero)
        self.assertEqual(expr_add.esquerda.valor, 10)
        self.assertIsInstance(expr_add.direita, Numero)
        self.assertEqual(expr_add.direita.valor, 5)

    def test_expressao_comparacao(self):
        code = "bool result = 10 > 5;"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        decl = ast.declaracoes[0]
        expr = decl.expressao

        self.assertIsInstance(expr, OperacaoBinaria)
        self.assertEqual(expr.op.type, 'MAIOR')
        self.assertIsInstance(expr.esquerda, Numero)
        self.assertEqual(expr.esquerda.valor, 10)
        self.assertIsInstance(expr.direita, Numero)
        self.assertEqual(expr.direita.valor, 5)

    def test_comando_if_simples(self):
        code = "if (x > 0) { int y = 1; }"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # A AST deve conter um único comando
        self.assertEqual(len(ast.declaracoes), 1)
        comando = ast.declaracoes[0]
        self.assertIsInstance(comando, ComandoIf)

        # Verifica a condição
        self.assertIsInstance(comando.condicao, OperacaoBinaria)
        self.assertEqual(comando.condicao.op.type, 'MAIOR')

        # Verifica o bloco 'then'
        bloco_then = comando.bloco_then
        self.assertIsInstance(bloco_then, Bloco)
        self.assertEqual(len(bloco_then.declaracoes), 1)

        # Verifica a declaração dentro do bloco
        decl_interna = bloco_then.declaracoes[0]
        self.assertIsInstance(decl_interna, DeclaracaoVariavel)
        self.assertEqual(decl_interna.nome_variavel.nome, 'y')
        self.assertEqual(decl_interna.expressao.valor, 1)

if __name__ == '__main__':
    unittest.main()
