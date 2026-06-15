# tests/test_code_generator.py
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from code_generator import CodeGenerator

class TestCodeGenerator(unittest.TestCase):

    def test_simple_assignment_translation(self):
        """TAC: ('ASSIGN', '10', None, 'x') -> Bytecode: PUSH 10, STORE x"""
        tac = [('ASSIGN', '10', None, 'x')]
        cg = CodeGenerator(tac)
        bytecode = cg.generate()
        
        expected = [
            ('PUSH', 10),
            ('STORE', 'x')
        ]
        self.assertEqual(bytecode, expected)

    def test_arithmetic_translation(self):
        """TAC: ('MAIS', 'x', '1', 't1') -> Bytecode: LOAD x, PUSH 1, ADD, STORE t1"""
        tac = [('MAIS', 'x', '1', 't1')]
        cg = CodeGenerator(tac)
        bytecode = cg.generate()
        
        expected = [
            ('LOAD', 'x'),
            ('PUSH', 1),
            ('ADD',),
            ('STORE', 't1')
        ]
        self.assertEqual(bytecode, expected)

    def test_label_resolution(self):
        """Testa se os labels textuais são convertidos em endereços numéricos."""
        tac = [
            ('JUMP', None, None, 'L1'),
            ('LABEL', 'L1', None, None),
            ('PRINT', '10', None, None)
        ]
        cg = CodeGenerator(tac)
        bytecode = cg.generate()
        
        # O LABEL L1 está na posição do PRINT. 
        # No bytecode resultante:
        # 0: JUMP 1
        # 1: PUSH 10
        # 2: PRINT
        expected = [
            ('JUMP', 1),
            ('PUSH', 10),
            ('PRINT',)
        ]
        self.assertEqual(bytecode, expected)

    def test_string_translation(self):
        """Testa a tradução de strings (TAC com aspas -> Bytecode PUSH puro)."""
        tac = [('PRINT', '"ola"', None, None)]
        cg = CodeGenerator(tac)
        bytecode = cg.generate()
        expected = [('PUSH', 'ola'), ('PRINT',)]
        self.assertEqual(bytecode, expected)

    def test_new_comparisons_translation(self):
        """Testa se os novos operadores de comparação são traduzidos para as instruções corretas."""
        tac = [
            ('MAIOR_IGUAL', 'a', 'b', 't1'),
            ('MENOR_IGUAL', 'c', 'd', 't2'),
            ('DIFERENTE', 'e', 'f', 't3')
        ]
        cg = CodeGenerator(tac)
        bytecode = cg.generate()
        
        # Cada operação binária gera: LOAD arg1, LOAD arg2, OP, STORE res
        self.assertEqual(bytecode[2], ('CMP_GE',))
        self.assertEqual(bytecode[6], ('CMP_LE',))
        self.assertEqual(bytecode[10], ('CMP_NE',))

if __name__ == '__main__':
    unittest.main()
