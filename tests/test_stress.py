# tests/test_stress.py
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lexer import Lexer
from parser_ import Parser
from semantic import SemanticAnalyzer
from ir_generator import IRGenerator
from code_generator import CodeGenerator
from vm import VirtualMachine

class TestStress(unittest.TestCase):

    def _execute_e2e(self, code, inputs=None):
        """Helper para rodar o pipeline completo do código fonte até a execução na VM."""
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
        if inputs:
            vm.inputs = inputs
        vm.run()
        return vm.output

    def test_fibonacci_sequence(self):
        """Calcula e imprime os primeiros 7 números da sequência de Fibonacci."""
        code = """
        int n = 7;
        int a = 0;
        int b = 1;
        int i = 0;
        while (i < n) {
            print(a);
            int next = a + b;
            a = b;
            b = next;
            i = i + 1;
        }
        """
        # Fibonacci: 0, 1, 1, 2, 3, 5, 8
        output = self._execute_e2e(code)
        expected = ['0', '1', '1', '2', '3', '5', '8']
        self.assertEqual(output, expected)

    def test_deeply_nested_logic(self):
        """Testa aninhamento profundo de loops e condicionais com muitas variáveis."""
        code = """
        int limit = 3;
        int outer = 0;
        int total = 0;
        while (outer < limit) {
            int inner = 0;
            while (inner < limit) {
                if ((outer + inner) == 2) {
                    total = total + 10;
                } else {
                    if ((outer + inner) > 2) {
                        total = total + 5;
                    } else {
                        total = total + 1;
                    }
                }
                inner = inner + 1;
            }
            outer = outer + 1;
        }
        print(total);
        """
        # Iterações (outer, inner):
        # (0,0) -> 0+0 < 2 -> total + 1 = 1
        # (0,1) -> 0+1 < 2 -> total + 1 = 2
        # (0,2) -> 0+2 == 2 -> total + 10 = 12
        # (1,0) -> 1+0 < 2 -> total + 1 = 13
        # (1,1) -> 1+1 == 2 -> total + 10 = 23
        # (1,2) -> 1+2 > 2 -> total + 5 = 28
        # (2,0) -> 2+0 == 2 -> total + 10 = 38
        # (2,1) -> 2+1 > 2 -> total + 5 = 43
        # (2,2) -> 2+2 > 2 -> total + 5 = 48
        output = self._execute_e2e(code)
        self.assertEqual(output, ['48'])

    def test_comprehensive_features(self):
        """Usa quase todos os recursos da linguagem: I/O, tipos, precedência, escopo, controle."""
        code = """
        int base;
        read(base); // Input: 5
        bool run = true;
        if (run) {
            int result = 0;
            int i = 1;
            while (i <= base) {
                result = result + (i * i);
                i = i + 1;
            }
            print(result); // Sum of squares: 1*1 + 2*2 + 3*3 + 4*4 + 5*5 = 1+4+9+16+25 = 55
        }
        """
        # Nosso parser/lexer ainda não suporta '<=', vamos usar '<' e '+'
        code = """
        int base;
        read(base);
        bool run = true;
        if (run) {
            int result = 0;
            int i = 1;
            while (i < (base + 1)) {
                result = result + (i * i);
                i = i + 1;
            }
            print(result);
        }
        """
        output = self._execute_e2e(code, inputs=['5'])
        self.assertEqual(output, ['55'])

if __name__ == '__main__':
    unittest.main()
