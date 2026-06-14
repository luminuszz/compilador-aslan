# test_runner.py
import unittest
import sys
import os

def run_tests():
    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.insert(0, src_dir)
    
    # Adiciona o diretório atual ao path para encontrar os módulos de teste
    test_dir = os.path.join(os.path.dirname(__file__), 'tests')
    
    # Carrega todos os arquivos de teste do diretório 'tests'
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=test_dir, pattern='test_*.py')
    
    # Roda os testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Encerra com código de erro se algum teste falhar
    if not result.wasSuccessful():
        sys.exit(1)

if __name__ == '__main__':
    # Cria o diretório de testes se ele não existir
    test_dir = os.path.join(os.path.dirname(__file__), 'tests')
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
        # Cria um __init__.py para tratar o diretório como um pacote
        with open(os.path.join(test_dir, '__init__.py'), 'w') as f:
            pass

    run_tests()
