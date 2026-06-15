# tests/test_e2e_features.py
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from lexer import Lexer
from parser_ import Parser
from semantic import SemanticAnalyzer
from ir_generator import IRGenerator
from code_generator import CodeGenerator
from vm import VirtualMachine

class TestE2EFeatures(unittest.TestCase):

    def _execute_e2e(self, code, inputs=None):
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        analyzer.visit(ast)
        ir_gen = IRGenerator()
        tac = ir_gen.visit(ast)
        cg = CodeGenerator(tac)
        bytecode = cg.generate()
        vm = VirtualMachine(bytecode)
        if inputs: vm.inputs = inputs
        vm.run()
        return vm.output

    def test_e2e_strings_basic(self):
        """Valida a impressão de strings e variáveis integradas."""
        code = """
        int idade = 25;
        print("Minha idade é:");
        print(idade);
        """
        output = self._execute_e2e(code)
        self.assertEqual(output, ["Minha idade é:", "25"])

    def test_e2e_comparison_operators(self):
        """Valida o funcionamento de >=, <= e != em estruturas condicionais."""
        code = """
        int a = 10;
        int b = 10;
        if (a >= b) {
            print("a >= b é verdadeiro");
        }
        
        b = 20;
        if (a <= b) {
            print("a <= b é verdadeiro");
        }
        
        if (a != b) {
            print("a != b é verdadeiro");
        }
        """
        output = self._execute_e2e(code)
        expected = [
            "a >= b é verdadeiro",
            "a <= b é verdadeiro",
            "a != b é verdadeiro"
        ]
        self.assertEqual(output, expected)

    def test_e2e_mixed_string_and_logic(self):
        """Um teste completo integrando strings, variáveis e lógica complexa."""
        code = """
        int cavalo = 10;
        int cavalo2 = 20;
        if (cavalo > cavalo2) {
            print("cavalo é maior");
        } else {
            print("cavalo2 é maior ou igual");
        }
        
        if (cavalo2 != cavalo) {
            print("são diferentes");
        }
        """
        output = self._execute_e2e(code)
        self.assertEqual(output, ["cavalo2 é maior ou igual", "são diferentes"])

if __name__ == '__main__':
    unittest.main()
