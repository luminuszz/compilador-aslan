# tests/test_vm.py
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from vm import VirtualMachine

class TestVM(unittest.TestCase):

    def test_basic_arithmetic(self):
        """Testa uma soma simples: push 10, push 5, add, print."""
        bytecode = [
            ('PUSH', 10),
            ('PUSH', 5),
            ('ADD',),
            ('PRINT',)
        ]
        vm = VirtualMachine(bytecode)
        vm.run()
        self.assertEqual(vm.output, ['15'])

    def test_memory_load_store(self):
        """Testa salvar e carregar da memória: push 10, store x, push 5, load x, mul, print."""
        bytecode = [
            ('PUSH', 10),
            ('STORE', 'x'),
            ('PUSH', 5),
            ('LOAD', 'x'),
            ('MUL',),
            ('PRINT',)
        ]
        vm = VirtualMachine(bytecode)
        vm.run()
        self.assertEqual(vm.output, ['50'])
        self.assertEqual(vm.memory['x'], 10)

    def test_jump_if_false(self):
        """Testa o salto condicional."""
        bytecode = [
            ('PUSH', False),
            ('JUMP_IF_FALSE', 4),
            ('PUSH', 1),
            ('PRINT',),
            ('PUSH', 0),
            ('PRINT',),
        ]
        vm = VirtualMachine(bytecode)
        vm.run()
        self.assertEqual(vm.output, ['0'])

    def test_vm_string_support(self):
        """Testa se a VM imprime strings corretamente."""
        bytecode = [('PUSH', 'Olá Mundo'), ('PRINT',)]
        vm = VirtualMachine(bytecode)
        vm.run()
        self.assertEqual(vm.output, ['Olá Mundo'])

    def test_vm_new_comparisons(self):
        """Testa as instruções CMP_GE, CMP_LE e CMP_NE na VM."""
        test_cases = [
            (10, 10, 'CMP_GE', True),
            (10, 5, 'CMP_GE', True),
            (5, 10, 'CMP_GE', False),
            (5, 10, 'CMP_LE', True),
            (10, 10, 'CMP_LE', True),
            (10, 5, 'CMP_LE', False),
            (5, 10, 'CMP_NE', True),
            (10, 10, 'CMP_NE', False),
        ]
        for a, b, op, expected in test_cases:
            bytecode = [('PUSH', a), ('PUSH', b), (op,), ('PRINT',)]
            vm = VirtualMachine(bytecode)
            vm.run()
            self.assertEqual(vm.output[-1], str(expected))

if __name__ == '__main__':
    unittest.main()
