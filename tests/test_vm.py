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
        # if (false) { print(1) } print(0)
        # 0: PUSH false
        # 1: JUMP_IF_FALSE 4
        # 2: PUSH 1
        # 3: PRINT
        # 4: PUSH 0
        # 5: PRINT
        bytecode = [
            ('PUSH', False),
            ('JUMP_IF_FALSE', 4),
            ('PUSH', 1),
            ('PRINT',),
            ('PUSH', 0),
            ('PRINT',)
        ]
        vm = VirtualMachine(bytecode)
        vm.run()
        self.assertEqual(vm.output, ['0'])

if __name__ == '__main__':
    unittest.main()
