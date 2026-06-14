# tests/test_leetcode.py
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

class TestLeetCode(unittest.TestCase):

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

    def test_bubble_sort_logic(self):
        """Simula a ordenação de 4 elementos na memória."""
        code = """
        int a = 40; int b = 10; int c = 30; int d = 20;
        int i = 0;
        while (i < 4) {
            if (a > b) { int t = a; a = b; b = t; }
            if (b > c) { int t = b; b = c; c = t; }
            if (c > d) { int t = c; c = d; d = t; }
            i = i + 1;
        }
        print(a); print(b); print(c); print(d);
        """
        output = self._execute_e2e(code)
        self.assertEqual(output, ['10', '20', '30', '40'])

    def test_binary_search_simulation(self):
        """Busca o número 7 em uma sequência 'ordenada' de variáveis."""
        code = """
        int v0 = 1; int v1 = 3; int v2 = 5; int v3 = 7; int v4 = 9;
        int target = 7;
        int result = 0;
        if (v2 == target) { result = 2; }
        if (v3 == target) { result = 3; }
        print(result);
        """
        output = self._execute_e2e(code)
        self.assertEqual(output, ['3'])

    def test_invert_binary_tree_structure(self):
        """
        Simula a inversão de uma árvore binária de 3 nós.
        Original: [1, 2, 3] (Raiz 1, Esq 2, Dir 3)
        Invertida: [1, 3, 2]
        """
        code = """
        int root = 1;
        int left = 2;
        int right = 3;
        
        // Inversão: swap(left, right)
        int temp = left;
        left = right;
        right = temp;
        
        print(root);
        print(left);
        print(right);
        """
        output = self._execute_e2e(code)
        self.assertEqual(output, ['1', '3', '2'])

if __name__ == '__main__':
    unittest.main()
